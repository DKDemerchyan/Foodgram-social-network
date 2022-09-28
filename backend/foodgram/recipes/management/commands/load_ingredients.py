import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):

        if Ingredient.objects.exists():
            print('Данные уже были загружены.')
            return

        print('Начинается загрузка ингредиентов из базы.')

        data = json.load(open('data/ingredients.json', encoding='utf-8'))
        for row in data:
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            ingredient.save()
        print('Данные были успешно загружены.')
