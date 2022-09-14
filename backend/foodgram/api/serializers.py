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
    """Сериализатор для списка рецептов."""

    author = serializers.StringRelatedField(read_only=True)
    #  Должна быть кнопка добавления покупки

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'author', 'cooking_time')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецепта."""

    tag = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tag', 'image', 'author',
                  'cooking_time', 'ingredients', 'text')


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор публикации нового рецепта."""

    tag = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'tag', 'image', 'author',
                  'cooking_time', 'ingredients', 'text')
