# Generated by Django 4.2.1 on 2025-05-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_alter_dessert_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dessert',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Цена'),
        ),
    ]
