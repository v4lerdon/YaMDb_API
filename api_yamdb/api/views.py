from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Title, User
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer, UserSerializer, TokenSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModerator
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg


#регистрация нового пользователя
class UserSignupViewset(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['username'] == 'me':
            return Response(
                {'Использовать имя "me" в качестве username запрещено.'}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        user = get_object_or_404(User, username=request.data['username'])
        token = default_token_generator.make_token(user)
        send_mail(
                'confirmation_code',
                token,
                'admin@yamdb.ru',
                [serializer.validated_data['email']]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


#получение токена по confirmation_code
class UserTokenViewset(APIView):
    permission_classes = (AllowAny,)   

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data['username'])

        if default_token_generator.check_token(user, request.data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return Response({'Не удалось сформировать токен'}, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'title', 'year')
    permission_classes = (
        IsAdminOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    permission_classes = (
        IsAdminOrReadOnly,
    )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    permission_classes = (
        IsAdminOrReadOnly,
    )
