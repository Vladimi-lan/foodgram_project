from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCartViewSet, FavoriteViewSet,
                    FollowViewSet, IngredientViewSet, RecipeViewSet,
                    ShoppingCartViewSet, TagViewSet)
from users.views import CustomUserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartViewSet.as_view(
          {'get': 'download_shopping_cart'}), name='download'),
    path('users/subscriptions/',
         FollowViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('users/<user_id>/subscribe/',
         FollowViewSet.as_view({'post': 'create',
                                'delete': 'delete'}), name='subscribe'),
    path('', include(router.urls)),
    path('recipes/<recipe_id>/favorites/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}, name='favorite')),
    path('recipes/<recipe_id>/shopping_cart/',
         ShoppingCartViewSet.as_view(
          {'post': 'create', 'delete': 'delete'}, name='shoppingcart')),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
