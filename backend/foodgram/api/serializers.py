from rest_framework import serializers

from recipes.models import IngredientRecipe, Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'quantity')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецепта."""

    tags = TagSerializer(many=True, read_only=True)
    #  author = UserSerializer - надо написать
    ingredients = serializers.SerializerMethodField()
    is_in_favorites = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_in_favorites(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_list(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_list.filter(recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'text', 'is_in_favorites', 'is_in_shopping_list',
            'name', 'image', 'text', 'cooking_time'
        )
