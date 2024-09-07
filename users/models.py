from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, verbose_name='Имя ', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', **NULLABLE)
    email = models.EmailField(max_length=150, verbose_name='Почта', unique=True)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    token = models.CharField(max_length=100, verbose_name='Токен', unique=True, editable=False, **NULLABLE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} - {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('email', 'first_name', 'last_name',)
        permissions = [
            ('view_users', 'Can view all users'),
            ('block_users', 'Can block all users'),
        ]
