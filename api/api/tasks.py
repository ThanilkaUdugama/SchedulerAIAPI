from celery import shared_task
from django.utils.timezone import now

@shared_task
def generate_notifications():
    message = f"Daily Notification at {now()}!"
    print(message)
    # Notification.objects.create(message=message)
