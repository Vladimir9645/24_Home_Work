from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Product

class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write('Группа "Модератор продуктов" создана.')
        else:
            self.stdout.write('Группа уже существует.')


        content_type = ContentType.objects.get_for_model(Product)
        perm_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            content_type=content_type,
        )
        group.permissions.add(perm_unpublish)


        perm_delete, _ = Permission.objects.get_or_create(
            codename='delete_product',
            content_type=content_type,
        )

        group.permissions.add(perm_delete)

        self.stdout.write('Права для группы "Модератор продуктов" назначены.')
