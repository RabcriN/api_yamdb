from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

CHOICES = (
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
)

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=False)
    email = models.EmailField(
        'email',
        uniwue=True,
        max_length=254,
    ),
    first_name = models.CharField(max_length=150, blank=True)
    second_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField()
    role = models.CharField(
        'Статус',
        choices = CHOICE
    )

