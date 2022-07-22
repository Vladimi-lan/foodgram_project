from django.contrib import admin
from users.models import CustomUser, Follow

from .models import (Favorites, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag, TagRecipe)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    min_num = 1
    extra = 0


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 0


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
    list_filter = ('id',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline, TagRecipeInline,)
    list_display = ('name', 'author', 'cooking_time',
                    'id', 'count_favorite', 'pub_date')
    search_fields = ('author__username', 'name', 'tags__slug')
    empty_value_display = '-пусто-'
    list_filter = ('author', 'name', 'tags')

    def count_favorite(self, obj):
        return Favorites.objects.filter(recipe=obj).count()
    count_favorite.short_description = 'Количество добавлений в избранное'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'id')
    search_fields = ('user',)
    empty_value_display = '-пусто-'
    list_filter = ('user',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', )
    empty_value_display = '-пусто-'
    list_filter = ('name',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
    list_filter = ('user',)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'
    list_filter = ('username', 'email')


admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
