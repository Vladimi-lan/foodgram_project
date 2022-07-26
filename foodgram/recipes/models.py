from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
        max_length=256
    )
    measurement_unit = models.CharField(
        max_length=14,
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    COLORS = [
        ('HOTPINK', '#FF69B4'),
        ('SALMON', '#FA8072'),
        ('GREEN', '#32CD32'),
        ('BLUE', '#87CEFA'),
        ('BROWN', '#F4A460'),
    ]
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название"
    )
    color = models.CharField(
        max_length=7,
        choices=COLORS,
        unique=True,
        verbose_name="Цвет в HEX"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Краткое название"
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author_recipes',
        verbose_name='Автор',
        help_text='Автор'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='foodgram/'
    )
    text = models.TextField(
        help_text='Введите описание рецепта',
        max_length=500
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes',
        verbose_name='Теги рецепта',
        help_text='Выберите подходящие теги'
    )
    incredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='ingredients',
        verbose_name='Необходимые ингредиенты',
        help_text='Выберите нужные продукты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовления в минутах',
        validators=[
            MinValueValidator(
                1,
                message='Убедитесь, что время приготовления больше 0.'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тэги',
        help_text='Выберите теги рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_recipe'
            ),
        ]

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Ингредиенты',
        help_text='Добавьте продукты, необходимые по рецепту'
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='количество',
        validators=[
            MinValueValidator(
                0.00001,
                message="Убедитесь, что количество больше 0."
            ),
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_recipe'
            ),
        ]

    def __str__(self):
        return f"{self.ingredient} {self.recipe}"


class Favorites(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Выберите рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            ),
        ]

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
        help_text='Выберите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
        help_text='Выберите рецепты для добавления в корзину'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            ),
        ]
