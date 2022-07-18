# Generated by Django 4.0.5 on 2022-07-16 11:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_favorites_delete_favourites_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0, message='Убедитесь, что количество больше 0.')], verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Введите время приготовления в минутах', validators=[django.core.validators.MinValueValidator(1, message='Убедитесь, что время приготовления больше 0.')], verbose_name='Время приготовления'),
        ),
    ]
