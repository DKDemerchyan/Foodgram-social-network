from django.core.management.base import BaseCommand
from recipes.models import Ingredient
from csv import DictReader


ALREADY_LOADED_ERROR_MESSAGE = 'Данные уже были загружены.'


class Command(BaseCommand):

    def handle(self, *args, **options):

        if Ingredient.objects.exists():
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return

        print('Started loading ingredients database.')

        for row in DictReader(open('./ingredients.csv')):
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            ingredient.save()
