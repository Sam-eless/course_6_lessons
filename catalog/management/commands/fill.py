import json

from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        with open('catalog_data.json', 'r', encoding='UTF8') as file:
            data = json.load(file)
            category_objects = []
            product_objects = []
            for i in data:
                if i['model'] == 'catalog.category':
                    category_objects.append(Category(i['pk'], **i['fields']))

            Category.objects.bulk_create(category_objects)

            for i in data:
                if i['model'] == 'catalog.product':
                    name = Category.objects.get(pk=i["fields"]["category"])
                    i["fields"]["category"] = name
                    product_objects.append(Product(**i['fields']))

            Product.objects.bulk_create(product_objects)

        # python -Xutf8 manage.py dumpdata catalog -o catalog_data.json
        # python manage.py migrate catalog zero
        # python manage.py makemigrations
        # python manage.py migrate
        # python manage.py fill
