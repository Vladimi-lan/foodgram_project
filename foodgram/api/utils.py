from django.db.models import Sum

from recipes.models import IngredientRecipe


def get_wishlist(user):
    shopping_list = {}
    ingredients = IngredientRecipe.objects.filter(
        recipe__shopping_cart__user=user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    for ingredient in ingredients:
        amount = ingredient['amount']
        name = ingredient['ingredient__name']
        measurement_unit = ingredient['ingredient__measurement_unit']
        if name not in shopping_list:
            shopping_list[name] = {
                'measurement_unit': measurement_unit,
                'amount': amount
            }
        else:
            shopping_list[name]['amount'] += ingredient.amount__sum
    wishlist = ([f'{item} - {value["amount"]} '
                 f'{value["measurement_unit"]} \n'
                 for item, value in shopping_list.items()])
    return wishlist
