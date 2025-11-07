from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Загружает тестовые данные для моделей Category и Product'

    def handle(self, *args, **options):
        # Удаляем все существующие данные
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Путь к фикстурам
        fixtures_dir = os.path.join(settings.BASE_DIR, 'catalog', 'fixtures')

        # Загружаем категории
        with open(os.path.join(fixtures_dir, 'categories.json'), 'r', encoding='utf-8') as f:
            categories = json.load(f)
            for category in categories:
                Category.objects.create(
                    id=category['pk'],
                    name=category['fields']['name'],
                    description=category['fields']['description'],
                    created_at=category['fields']['created_at'],
                    updated_at=category['fields']['updated_at']
                )

        # Загружаем продукты
        with open(os.path.join(fixtures_dir, 'products.json'), 'r', encoding='utf-8') as f:
            products = json.load(f)
            for product in products:
                Product.objects.create(
                    id=product['pk'],
                    name=product['fields']['name'],
                    description=product['fields']['description'],
                    image=product['fields']['image'],
                    price=product['fields']['price'],
                    category_id=product['fields']['category'],
                    created_at=product['fields']['created_at'],
                    updated_at=product['fields']['updated_at']
                )

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))
