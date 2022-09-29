import json

from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):

    def handle(self, *args, **options):

        if Tag.objects.exists():
            print('Данные уже были загружены.')
            return

        print('Начинается загрузка тегов из базы.')

        data = json.load(open('data/tags.json', encoding='utf-8'))
        for row in data:
            tag = Tag(
                name=row['name'],
                color=row['color'],
                slug=row['slug']
            )
            tag.save()
        print('Данные были успешно загружены.')
