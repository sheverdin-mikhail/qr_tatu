# Generated by Django 3.2.6 on 2022-04-25 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0010_alter_user_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=255, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Ссылка пользователя',
                'verbose_name_plural': 'Ссылки пользователей',
            },
        ),
        migrations.CreateModel(
            name='QrCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_link', models.CharField(blank=True, max_length=255, unique=True, verbose_name='Ссылка qr кода')),
                ('link_active', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='link_active', to='personal.userlinks', verbose_name='Активная ссылка')),
                ('link_list', models.ManyToManyField(blank=True, related_name='link_list', to='personal.UserLinks', verbose_name='Список подключенных ссылок')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'QR код',
                'verbose_name_plural': 'QR коды',
            },
        ),
    ]
