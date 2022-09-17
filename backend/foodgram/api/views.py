from rest_framework import viewsets
from recipes.models import Tag, Ingredient, Recipe
from .serializers import (
    IngredientSerializer, RecipePostSerializer,
    RecipeReadSerializer, TagSerializer,
)
from rest_framework.permissions import SAFE_METHODS


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipePostSerializer
