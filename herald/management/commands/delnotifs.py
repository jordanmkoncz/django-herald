import datetime
import argparse

from django.utils import timezone
from django.core.management.base import BaseCommand

from ...models import SentNotification


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


class Command(BaseCommand):
    help = 'Deletes notifications between the date ranges specified.'

    def add_arguments(self, parser):
        parser.add_argument('--start', help="includes this date, format YYYY-MM-DD", type=valid_date)
        parser.add_argument('--end', help="up to this date, format YYYY-MM-DD", type=valid_date)

    def handle(self, *args, **options):
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = options['start'].date() if options['start'] else today
        end_date = options['end'].date() if options['end'] else today + datetime.timedelta(days=1)
        deleted_notifications = SentNotification.objects.filter(date_sent__range=[start_date, end_date]).delete()
        deleted_num = deleted_notifications[0] if deleted_notifications is not None else SentNotification.objects.filter(date_sent__range=[start_date, end_date]).count()
        self.stdout.write('Successfully deleted {num} notification(s)'.format(num=deleted_num))
