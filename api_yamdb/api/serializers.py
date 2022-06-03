from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """
    #token = serializers.CharField(max_length=255, read_only=True)
    #date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['email', 'username']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
