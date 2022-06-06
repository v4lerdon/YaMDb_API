from django.db import models

from django.contrib.auth.models import AbstractUser

ADMIN_ROLE = [
    ('user', 'user'),
    ('admin', 'admin'),
    ('moderator', 'moderator'),
]


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=15,choices=ADMIN_ROLE,default='user')

    def __str__(self):
        return self.email


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Title(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    # rating = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.text
