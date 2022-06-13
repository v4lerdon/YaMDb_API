from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """Расширенная модель User."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ADMIN_ROLE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=254,
        verbose_name='Email пользователя',
        help_text='Укажите email пользователя'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография пользователя',
        help_text='Напишите биографию пользователя'
    )
    role = models.CharField(
        max_length=15,
        choices=ADMIN_ROLE,
        default=USER,
        verbose_name='Роль пользователя',
        help_text='Укажите роль пользователя'
    )

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.email


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
        help_text='Укажите название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='слаг/slug',
        help_text='Укажите слаг/slug'
    )

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название жанра',
        help_text='Укажите название жанра'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='слаг/slug',
        help_text='Укажите слаг/slug'
    )

    class Meta:
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для произведений/тайтлов."""
    name = models.CharField(
        max_length=100,
        verbose_name='Название тайтла',
        help_text='Укажите название тайтла'
    )
    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Год тайтла',
        help_text='Укажите год тайтла'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Описание тайтла',
        help_text='Укажите описание тайтла'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанр тайтла',
        help_text='Укажите жанр тайтла'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория тайтла',
        help_text='Укажите категорию тайтла'
    )

    class Meta:
        verbose_name = 'Тайтлы'
        verbose_name_plural = 'Тайтлы'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов для тайтлов."""
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
    score = models.PositiveSmallIntegerField(
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
    """Модель комментариев по отзывам."""
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
