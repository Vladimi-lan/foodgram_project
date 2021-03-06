import django_filters
from rest_framework import filters

from recipes.models import Recipe
from users.models import CustomUser


class IngredientSearchFilter(filters.SearchFilter):
    search_param = 'name'


class RecipeFilters(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all())
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset.all()
