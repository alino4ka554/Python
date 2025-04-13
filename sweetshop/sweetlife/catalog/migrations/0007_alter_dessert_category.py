# Generated by Django 4.2.1 on 2025-04-13 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_dessert_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dessert',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='desserts', to='catalog.category'),
        ),
    ]
