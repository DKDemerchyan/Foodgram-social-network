from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сокращенный сериализатор рецепта для представления списка."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели, связывающей ингредиенты с рецептом при чтении."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецепта."""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientReadSerializer(ingredients, many=True).data

    def get_is_in(self, obj, model):
        request = self.context.get('request')
        return (
            (request or not request.user.is_anonymous)
            and model.objects.filter(user=request.user, recipe=obj).exists()
        )

    def get_is_favorited(self, obj):
        return self.get_is_in(obj=obj, model=Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.get_is_in(obj=obj, model=ShoppingCart)


class IngredientPostSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели, связывающей ингредиенты с рецептом при публикации.
    """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор публикации рецепта."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientPostSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Без ингредиентов блюд быть не может!'
            })
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты не могут повторяться!'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Ингредиента в блюде должно быть больше ноля!'
                })

        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': (
                    'Добавьте хотя бы один тег, тогда остальным '
                    'пользователям будет проще найти ваш рецепт.'
                )
            })
        tag_list = []
        for tag in tags:
            if tag in tag_list:
                raise serializers.ValidationError({
                    'tags': 'Теги нельзя использовать несколько раз!'
                })
            tag_list.append(tag)

        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'Готовить нужно минимум 1 минуту!'
            })

        return data

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            IngredientInRecipe.objects.create(
                recipe=recipe, ingredient=ingredient_id, amount=amount
            )

    def create_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags = validated_data.get('tags')
        self.create_tags(tags, instance)

        IngredientInRecipe.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.get('ingredients')
        self.create_ingredients(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class BasicSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для моделей избранного и списка покупок."""

    class Meta:
        fields = ('user', 'recipe')

    def validate(self, data, model, status):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if model.objects.filter(
                user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': status
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(instance.recipe, context=context).data


class FavoriteSerializer(BasicSerializer):
    """Сериализатор модели избранного."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    model = Favorite
    status = 'Рецепт ранее добавлен в избранное.'

    def validate_favorite(self, data, model=model, status=status):
        return self.validate(data=data, model=model, status=status)


class ShoppingCartSerializer(BasicSerializer):
    """Сериализатор модели списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    model = ShoppingCart
    status = 'Рецепт уже есть в списке покупок!'

    def validate_shopping_cart(self, data, model=model, status=status):
        return self.validate(data=data, model=model, status=status)
