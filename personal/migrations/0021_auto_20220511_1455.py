# Generated by Django 3.2.6 on 2022-05-11 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0020_userlinks_link_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sub_date',
            field=models.DateField(null=True, verbose_name='Дата подписки'),
        ),
        migrations.AddField(
            model_name='user',
            name='sub_end_date',
            field=models.DateField(null=True, verbose_name='Дата окончания подписки'),
        ),
        migrations.AddField(
            model_name='user',
            name='sub_month',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество купленных месяцев'),
        ),
    ]