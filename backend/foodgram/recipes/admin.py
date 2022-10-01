from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'tags'
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
