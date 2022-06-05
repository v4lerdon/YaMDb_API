from django.contrib.auth.models import AbstractUser
from django.db import models


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
