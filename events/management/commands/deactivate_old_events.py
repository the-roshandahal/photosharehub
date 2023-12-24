# your_app/management/commands/deactivate_old_events.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event

class Command(BaseCommand):
    help = 'Deactivate old events'

    def handle(self, *args, **options):
        seven_days_ago = timezone.now() - timezone.timedelta(days=1)
        Event.objects.filter(status=True, created__lte=seven_days_ago).update(status=False)
        self.stdout.write(self.style.SUCCESS('Successfully deactivated old events.'))


