from tkinter import CASCADE
from django.db import models
from ..users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        related_name='ingredient',
        verbose_name='Ингредиент'
    )
    quantity = models.FloatField(
        verbose_name='Количество'
    )
    measurement_unit = models.CharField(
        max_length=100,
        related_name='ingredient',
        verbose_name='Единица измерения'
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        related_name='recipes',
        verbose_name='Блюдо'
    )
    image = models.ImageField(
        blank=True
    )
    text = models.TextField(
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredients = models.
