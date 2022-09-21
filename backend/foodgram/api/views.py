from rest_framework import viewsets, permissions
from recipes.models import Tag, Ingredient, Recipe
from users.models import User
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipePostSerializer,
    RecipeReadSerializer, TagSerializer,
    CustomUserSerializer
)
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status


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


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
