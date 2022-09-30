import json

from django.core.management.base import BaseCommand
from recipes.models import Recipe


class Command(BaseCommand):

    def handle(self, *args, **options):

        if Recipe.objects.exists():
            print('Данные уже были загружены.')
            return

        print('Начинается загрузка базовых рецептов из базы.')

        data = json.load(open('data/recipes.json', encoding='utf-8'))
        for row in data:
            recipe = Recipe(
                name=row['name'],
                tags=row['tags'],
                image=row['image'],
                text=row['text'],
                cooking_time=row['cooking_time'],
                author=row['author'],
                ingredients=row['ingredients']
            )
            recipe.save()
        print('Данные были успешно загружены.')
