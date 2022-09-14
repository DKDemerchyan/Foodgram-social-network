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
    #  Нужно добавить разрешение только для хекс кода через регулярки
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

    name = models.CharField(
        max_length=200,
        verbose_name='Блюдо'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        blank=True
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
        verbose_name='Автор рецепта',
        related_name='recipes'
    )

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Рецепт блюда'
        verbose_name_plural = 'Рецепты блюд'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Модель для связи ингредиентов и рецепта, а также указания количества."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    quantity = models.FloatField(
        verbose_name='Количество'
    )


#  Модель избранного


#  Модель продуктовой тележки
