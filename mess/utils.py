from .models import MessBill, MonthlyMessSummary
from django.db.models import Sum, Count
from datetime import datetime

def generate_monthly_summary(month_year):
    bills = MessBill.objects.filter(month_year=month_year)
    if not bills.exists():
        return None

    total_spent = bills.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_days = bills.aggregate(Sum('number_of_days'))['number_of_days__sum'] or 0
    number_of_girls = bills.values('user').distinct().count()
    per_day_charge = round(total_spent / total_days, 2) if total_days > 0 else 0

    summary, created = MonthlyMessSummary.objects.update_or_create(
        month_year=month_year,
        defaults={
            'total_spent': total_spent,
            'total_days': total_days,
            'number_of_girls': number_of_girls,
            'per_day_charge': per_day_charge
        }
    )
    return summary
