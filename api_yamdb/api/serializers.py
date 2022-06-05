from rest_framework import serializers

from reviews.models import User

#селитизатор модели user при регистрации пользователя
class UserSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    class Meta:
        model = User
        fields = ['email', 'username']

        
#селитизатор для токена
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField()
