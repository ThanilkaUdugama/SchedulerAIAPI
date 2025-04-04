# notifications/management/commands/schedule_notifications.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from datetime import datetime
from django.core.mail import send_mail
import pytz

# Function to send notifications
def send_notifications(timezone):
    # Current time in the specified timezone
    now = datetime.now(pytz.timezone(timezone))
    print(f"Sending notifications at {now.strftime('%Y-%m-%d %H:%M:%S')} in {timezone}")

    

class Command(BaseCommand):
    help = 'Schedules notifications for all timezones at 12:00 PM'

    def handle(self, *args, **kwargs):
        # Create scheduler instance
        scheduler = BackgroundScheduler()

        # Get all timezones from pytz
        timezones = pytz.all_timezones
        
        for tz in timezones:
            # Create a cron trigger for 12:00 PM (noon) in each timezone
            trigger = CronTrigger(hour=21, minute=55, timezone=pytz.timezone(tz))
            scheduler.add_job(send_notifications, trigger, args=[tz])
            

        # Start the scheduler
        scheduler.start()

        try:
            # Keep the scheduler running until the server shuts down
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
