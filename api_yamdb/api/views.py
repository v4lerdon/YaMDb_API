from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import UserSerializer


class CreateUserAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)

    @csrf_exempt
    @action(detail=True, methods=['post'])
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()        
        #создаем токен  и отпраляем его на почту
        #confirmation_code = default_token_generator.make_token(user)
        send_mail('Token api_yamdb', 'your token:', 'admin@yamdb.ru', ['baem-festa@yandex.ru'])
        return Response(serializer.data, status=status.HTTP_200_OK)
                         