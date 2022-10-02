from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERS_ROLES_CHOICES = [
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
        ('moderator', 'Модератор')
    ]

    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=USERS_ROLES_CHOICES,
        default='user'
    )
    confirmation_code = models.TextField(
        'Код рeгистрации',
        max_length=256,
        blank=True
    )
