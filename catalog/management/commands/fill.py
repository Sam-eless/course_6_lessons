from django.core.management import BaseCommand
from catalog.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()
        category_list = [
            {'name': 'Рыба', 'description': 'Замороженное'},
            {'name': 'Птица', 'description': 'Охлажденное'},
            {'name': 'Морепродукты', 'description': 'Замороженное'},
            {'name': 'Фрукты', 'description': 'Свежее, скоропортящееся'},
            {'name': 'Овощи', 'description': 'Свежее, скоропортящееся'},
        ]

        category_objects = []
        for item in category_list:
            category_objects.append(Category(**item))

        Category.objects.bulk_create(category_objects)
