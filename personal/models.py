import calendar
import re
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse

from .utils import get_icon_template


class Subscription(models.Model):
    # subscription model
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
    link_count = models.PositiveIntegerField(
        verbose_name='Количество доступных ссылок для QR (0 если не ограничено) ',
        default=1,
        blank=True
    )
    present = models.BooleanField(
        verbose_name=("Подарок вкл/выкл"),
        default=False,
        blank=True
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
    # user model
    username_validator = UnicodeUsernameValidator
    sub_date = models.DateField(verbose_name='Дата подписки', null=True, blank=True)
    sub_end_date = models.DateField(verbose_name='Дата окончания подписки', null=True, blank=True)
    sub_month = models.PositiveIntegerField(verbose_name="Количество купленных месяцев", default=1)
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

    def save_sub(self, sub_id):
        sub = Subscription.objects.get(pk=sub_id)
        self.subscription = sub
        self.sub_date = datetime.now()
        days = calendar.monthrange(self.sub_date.year, self.sub_date.month)[1]
        self.sub_end_date = self.sub_date + timedelta(days=days * self.sub_month)
        return super().save()


class UserLinks(models.Model):
    # qr link model
    link = models.CharField(
        verbose_name='Ссылка',
        max_length=255,
        blank=True
    )
    button_text = models.CharField(
        verbose_name='Текст кнопки',
        max_length=255,
        blank=True
    )
    link_icon = models.CharField(
        verbose_name='Иконка кнопки',
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = ('Ссылка пользователя')
        verbose_name_plural = ("Ссылки пользователей")

    def __str__(self):
        return self.link

    def save(self):
        url = self.link
        self.link_icon = get_icon_template(url)
        return super().save()


class QrCode(models.Model):
    # qr code model
    qr_link = models.CharField(
        verbose_name='Ссылка qr кода',
        max_length=255,
        unique=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        blank=True,
        on_delete=models.CASCADE

    )
    link_list = models.ManyToManyField(
        UserLinks,
        verbose_name='Список подключенных ссылок',
        blank=True,
        related_name='link_list',
        null=True
    )
    link_active = models.OneToOneField(
        UserLinks,
        verbose_name='Активная ссылка',
        on_delete=models.CASCADE,
        blank=True,
        related_name='link_active',
        null=True
    )

    enabled = models.BooleanField(
        verbose_name='Активность qr кода',
        default=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = ('QR код')
        verbose_name_plural = ("QR коды")

    def __str__(self):
        return f'{self.user.email}: {self.qr_link}'

    def get_absolute_url(self):
        return reverse('qr_redirect', kwargs={'slug': self.qr_link})

    def get_full_absolute_url(self):
        domain = Site.objects.get_current().domain
        return 'http://%s%s' % (domain, self.get_absolute_url())
