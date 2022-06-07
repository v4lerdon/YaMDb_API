from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    class Meta:
        model = User
        fields = ['email', 'username']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        # fields = '__all__'
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

