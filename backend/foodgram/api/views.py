from rest_framework import viewsets, permissions
from recipes.models import Tag, Ingredient, Recipe, Favorite
from django.shortcuts import get_object_or_404
from .pagination import RecipePagination
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipePostSerializer,
    RecipeReadSerializer, TagSerializer,
)
from .filters import IngredientSearchFilter, RecipeFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .permissions import AuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipePostSerializer

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = FavoriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(
            Favorite, user=user, recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
