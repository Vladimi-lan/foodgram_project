from api.pagination import LimitPageNumberPagination
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorites, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import CustomUser, Follow

from .filters import IngredientSearchFilter, RecipeFilters
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSerializerPost,
                          ShoppingCartSerializer, TagSerializer,
                          UserFollowSerializer)
from .utils import get_wishlist


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_backends = (DjangoFilterBackend, IngredientSearchFilter)
    search_fields = ['^name', ]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_class = RecipeFilters
    filter_backends = [DjangoFilterBackend, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeSerializerPost


class BaseFavoriteCartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if self.model.objects.filter(user=request.user,
                                     recipe=recipe).exists():
            message = {'errors': 'Вы уже добавили этот рецепт'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipe_id']
        user_id = request.user.id
        object = get_object_or_404(
            self.model, user__id=user_id, recipe__id=recipe_id)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(BaseFavoriteCartViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoriteSerializer
    model = Favorites


class ShoppingCartViewSet(BaseFavoriteCartViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    model = ShoppingCart


class DownloadShoppingCartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=('get',), url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        wishlist = get_wishlist(request.user)
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
        return response


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        return get_list_or_404(CustomUser, following__user=self.request.user)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        author = get_object_or_404(CustomUser, id=user_id)
        data = {
            'user': request.user.id,
            'author': user_id
        }
        serializer = UserFollowSerializer(data=data,
                                          context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.get_or_create(
            user=request.user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        user_id = request.user.id
        Follow.objects.filter(
            user__id=user_id, author__id=author_id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
