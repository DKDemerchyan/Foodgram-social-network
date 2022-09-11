from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        max_length=200,
        unique=True
    )
    #  Пока не понял, как пользователь выберет цвет, не вводить же HEX-код.
    #  Наверно сделаю CHOICES
    color = models.CharField(
        max_length=7,
        unique=True
    )
    #  Нужно добавить разрешение только этих символов ^[-a-zA-Z0-9_]+$
    slug = models.SlugField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=200,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

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
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Блюдо'
    )
    text = models.TextField(
        verbose_name='Рецепт'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, message='Минимальное время приготовления одна минута.'
        )],
        verbose_name='Время приготовления'
    )
    author = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор рецепта'
    )
