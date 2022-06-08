from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User

from api.permissions import IsAdmin
from api.serializers import (TokenSerializer, UserMeSerializer,
                             UserSignupSerializer, UsersSettingsSerializer)


class UserMeRetrieveUpdate(APIView):
    """Получние/изменение своей учетной записи."""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, email=request.user)
        serializer = UsersSettingsSerializer(user)
        return Response(serializer.data , status=status.HTTP_200_OK)

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
    
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data['username'] == 'me':
            return Response(
                {'Использовать имя "me" в качестве username запрещено.'},
                status=status.HTTP_400_BAD_REQUEST
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
