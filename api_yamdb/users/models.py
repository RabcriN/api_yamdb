from django.db import models
# from django.contrib import admin <--- Зачем этот импорт?
from django.contrib.auth.models import AbstractUser

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

CHOICES = (
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
)


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=False, unique=True)
    email = models.EmailField(
        'email',
        unique=True,
        max_length=254,
    ),
    first_name = models.CharField(max_length=150, blank=True)
    second_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField()
    role = models.CharField(
        'Статус',
        choices=CHOICES,
        default=USER,
        max_length=50,
    )
    confirmation_code = models.CharField(max_length=255)

    @property
    def is_admin(self):
        """Is the user an admin?"""
        return (
            self.role == ADMIN or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
