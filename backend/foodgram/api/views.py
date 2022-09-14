from rest_framework import viewsets
from recipes.models import Recipe
from .serializers import RecipeListSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
