from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from recipes.models import (Favorites, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag, TagRecipe)
from users.models import CustomUser, Follow


class CommonSubscribed(metaclass=serializers.SerializerMetaclass):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class CustomUserSerializer(UserSerializer, CommonSubscribed):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'password')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('password', None)
        return result


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class CommonRecipe(metaclass=serializers.SerializerMetaclass):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        return Favorites.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(
                            user=request.user, recipe=obj).exists()


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer, CommonRecipe):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountSerializer(source='ingredient_recipes',
                                             many=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time')


class RecipeSerializerPost(serializers.ModelSerializer, CommonRecipe):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientAmountRecipeSerializer(source='ingredient_recipes',
                                                   many=True)
    image = Base64ImageField(max_length=None, use_url=False,)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time')

    def validate_ingredients(self, value):
        ingredients_list = []
        ingredients = value
        for ingredient in ingredients:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError('Количество должно быть'
                                                  'равным или больше 1!')
            id_to_check = ingredient['ingredient']['id']
            ingredient_to_check = Ingredient.objects.filter(id=id_to_check)
            if not ingredient_to_check.exists():
                raise serializers.ValidationError('Данного продукта'
                                                  'нет в базе!')
            if ingredient_to_check in ingredients_list:
                raise serializers.ValidationError('Эти продукты уже были'
                                                  'в рецепте!')
            ingredients_list.append(ingredient_to_check)
        return value

    def add_tags_ingredients(self, tags, ingredients, recipe):
        recipe.tags.set(tags)
        data = [IngredientRecipe(ingredient_id=ingredient['ingredient']['id'],
                                 recipe=recipe, amount=ingredient['amount'])
                for ingredient in ingredients]
        IngredientRecipe.objects.bulk_create(data)
        return recipe

    def create(self, validated_data):
        author = validated_data.get('author')
        ingredients = validated_data.pop('ingredient_recipes')
        tags = validated_data.pop('tags')
        name = validated_data.get('name')
        image = validated_data.get('image')
        text = validated_data.get('text')
        cooking_time = validated_data.get('cooking_time')
        recipe = Recipe.objects.create(
            author=author,
            name=name,
            image=image,
            text=text,
            cooking_time=cooking_time,
        )
        recipe = self.add_tags_ingredients(tags, ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_recipes')
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        instance = self.add_tags_ingredients(tags, ingredients, instance)
        super().update(instance, validated_data)
        instance.save()
        return instance


class FavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = Base64ImageField(max_length=None, use_url=False,)
    cooking_time = serializers.IntegerField()


class ShoppingCartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = Base64ImageField(max_length=None, use_url=False,)
    cooking_time = serializers.IntegerField()


class RecipesCountSerializer(metaclass=serializers.SerializerMetaclass):
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author__id=obj.id).count()


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        user_id = data['user']
        author_id = data['author']
        is_following = Follow.objects.filter(
            user=user_id, author=author_id
        ).exists()
        if is_following:
            raise serializers.ValidationError(
                {'errors': 'Вы уже подписаны.'}
            )
        if (data['user'] == data['author']
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на самого себя'}
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        obj = instance
        if request.method == 'POST':
            obj = instance.get('author')
        return FollowRepresentSerializer(
            obj,
            context={'request': request}
            ).data


class FollowRepresentSerializer(serializers.ModelSerializer,
                                RecipesCountSerializer, CommonSubscribed):
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = Recipe.objects.filter(
                        author__id=obj.id).order_by('id')[:recipes_limit]
        else:
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return ShortRecipeSerializer(queryset, many=True).data
