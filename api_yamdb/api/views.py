from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User

from api.serializers import UserSerializer, TokenSerializer

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
    
