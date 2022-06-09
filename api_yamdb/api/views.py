from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title, User

from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, TokenSerializer, UserMeSerializer, UserSignupSerializer, UsersSettingsSerializer

from rest_framework.response import Response


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
                'admin@yamdb.ru',
                [email]
        )

    def post(self, request):
        try:
            username = request.data['username']
            email = request.data['email']
            user = User.objects.get(username=username, email=email)
            self.tokensend(user, username, email)
        except (KeyError, User.DoesNotExist):
            serializer = UserSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = request.data['username']
            email = request.data['email']
            if username == 'me':
                return Response(
                    {'Использовать имя "me" в качестве username запрещено.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = serializer.save()
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
            user, request.data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response(
            {'Не удалось сформировать токен'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (
        IsAdminOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(ListCreateDestroyViewSet):
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
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (
        IsAdminOrReadOnly,
    )
