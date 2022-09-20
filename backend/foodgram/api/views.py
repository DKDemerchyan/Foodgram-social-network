from rest_framework import viewsets, permissions
from recipes.models import Tag, Ingredient, Recipe
from users.models import User
from .serializers import (
    IngredientSerializer, RecipePostSerializer,
    RecipeReadSerializer, TagSerializer,
    CustomUserSerializer
)
from djoser.views import UserViewSet


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeReadSerializer
        return RecipePostSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
