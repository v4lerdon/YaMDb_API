from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

ADMIN_ROLE = [
    ('user', 'user'),
    ('admin', 'admin'),
    ('moderator', 'moderator'),
]


class User(AbstractUser):
    """Расширенная модель User."""
    username = models.CharField(db_index=True, max_length=150, unique=True)
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=15,
        choices=ADMIN_ROLE,
        default='user'
    )

    def __str__(self):
        return self.email


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для произведений/тайтлов."""
    name = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        help_text='Укажите автора отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение, к которому относится отзыв',
        help_text='Укажите произведение, к которому относятся отзыв')
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва')
    score = models.IntegerField(
        verbose_name='Оценка произведения от 1 до 10',
        help_text='Оцените произведение по шкале от 1 до 10',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True)
    
    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('author', 'title'),
                                    name='unique_review'),)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор публикации',
        help_text='Укажите автора публикации')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор, к которому относятся комментарий',
        help_text='Укажите обзор, к которому относятся комментарии')
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
