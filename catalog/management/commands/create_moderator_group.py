from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создает группу модераторов с необходимыми правами'

    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем разрешения на удаление и отмену публикации
        can_delete = Permission.objects.get(codename='delete_product', content_type=content_type)
        can_unpublish, created = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            content_type=content_type
        )

        # Добавляем разрешения группе
        moderator_group.permissions.add(can_delete, can_unpublish)

        self.stdout.write(self.style.SUCCESS('Группа модераторов успешно создана с необходимыми правами'))
