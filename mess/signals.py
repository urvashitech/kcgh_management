from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MessBill
from .utils import generate_monthly_summary

@receiver(post_save, sender=MessBill)
@receiver(post_delete, sender=MessBill)
def update_summary_on_bill_change(sender, instance, **kwargs):
    if instance.month_year:
        generate_monthly_summary(instance.month_year)
