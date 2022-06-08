from rest_framework import serializers

from reviews.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """
    class Meta:
        model = User
        fields = ['email', 'username']

class TokenSerializer(serializers.Serializer):
    """Сериализация токена."""
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField()


class UsersSettingsSerializer(serializers.ModelSerializer):
    """Сериализация изменение/создание user администратором."""
    first_name = serializers.CharField(
        required=False, max_length=150, allow_null=True
    )
    last_name = serializers.CharField(
        required=False, max_length=150, allow_null=True
    )
    role = serializers.ChoiceField(
        choices=['user', 'moderator', 'admin'], default='user'
    )
    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализация запроса/измения своей учетной записи."""
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(
        required=False, max_length=150, allow_null=True
    )
    last_name = serializers.CharField(
        required=False, max_length=150, allow_null=True
    )
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
