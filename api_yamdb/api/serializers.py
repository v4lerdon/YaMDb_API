from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    class Meta:
        model = User
        fields = ['email', 'username']

        
#селитизатор для токена
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField()


class TitleSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
