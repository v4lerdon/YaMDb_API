from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, User


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов к тайтлам."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('К этому произведению'
                                      'уже оставлен отзыв')
        return data


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация категорий."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    """Сериализация тайтлов/произведений. Создание."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализация тайтлов/произведений. Только просмотр."""
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя и создания нового."""
    username = serializers.SlugField(
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if User.objects.filter(
                username=data['username'],
                email=data['email']).exists():
            return data
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем существует.'
            )
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email существует.'
            )
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return data


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
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
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
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
