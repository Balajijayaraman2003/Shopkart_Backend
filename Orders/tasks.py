from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Orders

@shared_task
def delete_pending_orders():
    try: 
        cutoff_time = timezone.now() - timedelta(minutes=1)
        deleted_count, _ = Orders.objects.filter(
        status="Pending",created_at__lte = cutoff_time
        ).delete()
        return f"Deleted {deleted_count} old pending orders"
    except Exception as e:
        return f"Error: {e}"