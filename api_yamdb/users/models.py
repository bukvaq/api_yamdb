from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('USER', 'user'),
        ('MODERATOR', 'moderator'),
        ('ADMIN', 'admin'),)

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    username = models.CharField(
        max_length=50, unique=True,
        blank=True, verbose_name='Ник-нейм пользователя')
    role = models.CharField(
        max_length=20, choices=USER_ROLES,
        default='user', verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=100, editable=False, blank=True,
        null=True, unique=True, verbose_name='Код подтверждения')
    email = models.EmailField(blank=False, unique=True,
                              verbose_name='Электронная почта')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

