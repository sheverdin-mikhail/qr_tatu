# Generated by Django 3.2.6 on 2022-04-27 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0012_qrcode_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='enabled',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Активность qr кода'),
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='link_active',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='link_active', to='personal.userlinks', verbose_name='Активная ссылка'),
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='link_list',
            field=models.ManyToManyField(blank=True, null=True, related_name='link_list', to='personal.UserLinks', verbose_name='Список подключенных ссылок'),
        ),
    ]