from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('id',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('id',)


# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ('tags', 'author', 'ingredients', 'name',
#                     'image', 'text', 'cooking_time'
#                 )
#     list_filter = ('id',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(Recipe, RecipeAdmin)