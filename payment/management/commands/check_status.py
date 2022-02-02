from django.core.management.base import BaseCommand
from account.models import AccountTransaction


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Status check")