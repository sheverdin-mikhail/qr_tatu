from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models


class Subscription(models.Model):
    name = models.CharField(('Название подписки'), max_length=255)
    change_link = models.BooleanField(
        verbose_name=('Смена ссылки вкл/выкл'),
        default=False,
        blank=True
    )
    change_link_count = models.PositiveIntegerField(
        verbose_name=('Кол-во смен ссылки в год (0 если не ограничено)'),
        default=1,
        blank=True
    )
    support = models.BooleanField(
        verbose_name=('Обращение в тех поддержку вкл/выкл'),
        default=False,
        blank=True
    )
    support_count = models.PositiveIntegerField(
        verbose_name=('Кол-во обращений в тех поддержку в год (0 если не ограничено)'),
        default=1,
        blank=True
    )
    discount = models.BooleanField(
        verbose_name=('Скидка на услуги партнеров вкл/выкл'),
        default=False,
        blank=True
    )
    discount_count = models.PositiveIntegerField(
        verbose_name=('Величина скидки %'),
        default=10,
        blank=True
    )
    personal_site = models.BooleanField(
        verbose_name=('Персональный сайт вкл/выкл'),
        default=False,
        blank=True
    )
    lock_password = models.BooleanField(
        verbose_name=('Пароль блокировки вкл/выкл'),
        default=False,
        blank=True
    )
    qr_count = models.PositiveIntegerField(
        verbose_name=('Кол-во QR кодов '),
        default=1,
        blank=True
    )
    present = models.BooleanField(
        verbose_name=("Подарок вкл/выкл"),
        default=False,
        blank = True
    )
    present_name = models.CharField(
        verbose_name=("Название подарка"),
        max_length=255,
        blank=True,
        null=True
    )
    free_sub = models.BooleanField(
        verbose_name=('Бесплатная подписка'),
        default=False,
        blank=True
    )

    class Meta:
        verbose_name = ('Подписка')
        verbose_name_plural = ("Подписки")

    def __str__(self):
        return self.name


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
    subscription = models.ForeignKey(
        Subscription,
        verbose_name=('Подписка'),
        related_name="subscription",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    email_verify = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
