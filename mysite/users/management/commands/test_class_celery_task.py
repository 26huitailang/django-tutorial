from django.core.management.base import BaseCommand
from users.tasks import add_two_nums


class Command(BaseCommand):
    help = 'test class based celery task'

    def handle(self, *args, **options):
        add_two_nums.delay(1, 2)
