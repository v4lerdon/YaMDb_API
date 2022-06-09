from django.contrib.auth.models import AbstractUser
from django.db import models


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
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
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
