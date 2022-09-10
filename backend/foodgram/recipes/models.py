from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
    )
    color = models.CharField(
        max_length=7,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Ингредиент'
    )
    quantity = models.FloatField(
        verbose_name='Количество'
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Блюдо'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True
    )
    text = models.TextField(
        verbose_name='Рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты'
    )
    tags = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Теги'
    )
