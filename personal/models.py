from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models


class User(AbstractUser):

    username_validator = UnicodeUsernameValidator
    surname = models.CharField(('Отчество'), max_length=100, null=True, blank=True)
    phone = models.CharField(('Номер телефона'), max_length=16, null=True, blank=True)
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        ('email address'),
        unique=True,
        )
    email_verify = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



