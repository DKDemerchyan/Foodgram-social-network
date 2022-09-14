from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeListSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tag', 'image', 'author', 'cooking_time')


class RecipeDetailSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tag', 'image', 'author',
                  'cooking_time', 'ingredients', 'text')
