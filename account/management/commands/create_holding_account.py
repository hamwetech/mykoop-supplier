from django.core.management.base import BaseCommand
from django.utils import timezone
from account.models import Account


class Command(BaseCommand):
    help = 'Create holding Account'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        try:
            Account.objects.create(
                name="Holding Account",
                reference="H000001",
                is_holding=True,
                balance=0
            )
            self.stdout.write("Holding Account created %s" % time)
        except Exception as e:
            self.stdout.write("Error:  %s" % e)