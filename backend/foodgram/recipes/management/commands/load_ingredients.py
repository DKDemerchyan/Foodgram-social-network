from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import json


class Command(BaseCommand):

    def handle(self, *args, **options):

        if Ingredient.objects.exists():
            print('Данные уже были загружены.')
            return

        print('Started loading ingredients database.')

        data = json.load(open('ingredients.json', encoding='utf-8'))
        for row in data:
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            ingredient.save()
        print('Successfully imported')
