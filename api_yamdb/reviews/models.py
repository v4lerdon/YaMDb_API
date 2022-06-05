from django.db import models

from django.db import models
from django.contrib.auth import get_user_model


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
    rating = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name="posts", blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles", blank=True, null=True
    )


    def __str__(self):
        return self.text

