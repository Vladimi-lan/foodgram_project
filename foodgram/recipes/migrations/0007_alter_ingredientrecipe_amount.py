# Generated by Django 4.0.5 on 2022-07-19 07:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_ingredient_measurement_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(1e-05, message='Убедитесь, что количество больше 0.')], verbose_name='количество'),
        ),
    ]
