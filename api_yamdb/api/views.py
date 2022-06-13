from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReadOnlyTitleSerializer,
                          ReviewSerializer, TitleSerializer, TokenSerializer,
                          UserMeSerializer, UserSignupSerializer,
                          UsersSettingsSerializer)
from api_yamdb.settings import DEFAULT_FROM_EMAIL


class UserMeRetrieveUpdate(APIView):
    """Получние/изменение своей учетной записи."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, email=request.user)
        serializer = UsersSettingsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersSettingsViewset(viewsets.ModelViewSet):
    """Администратор: получение/изменение списка пользователей.
    добавление пользователя администратором."""
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UsersSettingsSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserSignupViewset(APIView):
    """Регистрация нового пользователя, получение кода."""
    permission_classes = (AllowAny,)

    def tokensend(self, user, username, email):
        token = default_token_generator.make_token(user)
        send_mail(
            'confirmation_code',
            token,
            DEFAULT_FROM_EMAIL,
            (email,)
        )

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, create = User.objects.get_or_create(
            username=username,
            email=email,
        )
        if create:
            user.save()
        self.tokensend(user, username, email)
        return Response(
            {'username': username, 'email': email},
            status=status.HTTP_200_OK
        )


class UserTokenViewset(APIView):
    """Получение токена по коду."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data['username'])

        if default_token_generator.check_token(
            user,
            request.data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response(
            {'Не удалось сформировать токен'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведения/тайтла."""
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (
        IsAdminOrReadOnly,
    )

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (
        IsAdminOrReadOnly,
    )


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (
        IsAdminOrReadOnly,
    )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if self.request.user.reviews.filter(title=title_id).exists():
            raise ValidationError('К этому произведению уже оставлен отзыв.')
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrAdminOrModerator,)

    def get_queryset(self):
        queryset = Comment.objects.filter(
            review_id=self.kwargs.get('review_id')
        )
        return queryset

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        if get_object_or_404(Review, id=self.kwargs.get('review_id')):
            serializer.save(
                author=self.request.user,
                review_id=self.kwargs.get('review_id')
            )
