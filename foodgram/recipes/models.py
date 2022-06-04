from django.db import models

from django.core.validators import MinValueValidator

from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    MEASURMENTS = [
        ("г", "г"),
        ("кг", "кг"),
        ("мл", "мл"),
        ("л", "л"),
        ("ст. л.", "ст. л."),
        ("ч. л.", "ч. л."),
        ("банка", "банка"),
        ("батон", "батон"),
        ("бутылка", "бутылка"),
        ("веточка", "веточка"),
        ("горсть", "горсть"),
        ("долька", "долька"),
        ("звездочка", "звездочка"),
        ("зубчик", "зубчик"),
        ("капля", "капля"),
        ("кусок", "кусок"),
        ("лист", "лист"),
        ("пакет", "пакет"),
        ("пакетик", "пакетик"),
        ("пачка", "пачка"),
        ("пласт", "пласт"),
        ("по вкусу", "по вкусу"),
        ("пучок", "пучок"),
        ("стакан", "стакан"),
        ("стебель", "стебель"),
        ("стручок", "стручок"),
        ("тушка", "тушка"),
        ("упаковка", "упаковка"),
        ("шт.", "шт."),
        ("щепотка", "щепотка"),
    ]
    name = models.CharField(
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
        max_length=256
    )
    units = models.CharField(
        max_length=14,
        choices=MEASURMENTS
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    COLORS = [
        ('#FF69B4', '#FF69B4'),
        ('#FA8072', '#FA8072'),
        ('#32CD32', '#32CD32'),
        ('#87CEFA', '#87CEFA'),
        ('#F4A460', '#F4A460'),
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
        User,
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
        related_name='tag_recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовления в минутах',
        validators=[
            MinValueValidator(
                1,
                message='Убедитесь, что значение больше 0.'
            ),
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='incredient_recipe'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_recipes'
    )
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='количество',
        validators=[
            MinValueValidator(
                0,
                message="Убедитесь, что значение больше 0."
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


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
        ]


class Favourites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            ),
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_cart',
        verbose_name='Корзина пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            ),
        ]