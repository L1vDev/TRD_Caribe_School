import json
from django.utils.translation import gettext_lazy as _
from app_statistics.models import SaleStatistics
from app_store.models import InvoiceProducts
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from calendar import monthrange

def dashboard_callback(request, context):
    today = timezone.now().date()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    years = SaleStatistics.objects.dates('date', 'year', order='ASC').values_list('date__year', flat=True).distinct()
    years = sorted(set(years))

    context.update(statistics_by_month(month,year))
    context.update(statistics_top_products())
    context["selected_year"]=year
    context["selected_month"]=f"{month:02d}"
    context["years"]=years
    return context

def get_top_products():
    since = timezone.now() - timedelta(days=15)
    amount_expr = ExpressionWrapper(
        F('product_price') * (1 - F('product_discount') / 100) * F('quantity'),
        output_field=FloatField()
    )
    top_products = (
        InvoiceProducts.objects
        .filter(invoice__status='completed', invoice__created_at__gte=since)
        .values('product_id', 'product_name')
        .annotate(
            total_quantity=Sum('quantity'),
            total_amount=Sum(amount_expr)
        )
        .order_by('-total_quantity')[:10]
    )
    return list(top_products)

def statistics_top_products():
    top_products=get_top_products()
    total_revenue = sum(p['total_amount'] for p in top_products)
    data = {
        "top_products": [
            {
                'title': product['product_name'],
                'description': f"${product['total_amount']:.2f}",
                'value': int((product['total_amount']*100 / total_revenue))
            }
            for product in top_products
        ],
        "total_revenue": total_revenue
    }
    return data

def statistics_by_month(month, year):
    days_in_month = monthrange(year, month)[1]
    days = [timezone.datetime(year, month, day).date() for day in range(1, days_in_month + 1)]
    
    stats = SaleStatistics.objects.filter(date__year=year, date__month=month).values_list('date', 'amount')
    stats_dict = dict(stats)
    daily_data = [float(stats_dict.get(day, 0)) for day in days]

    data={
        "chart":json.dumps(
            {
                "labels": [day for day in range(1, days_in_month+1)],
                "datasets":[
                   {
                        "label": "Ventas",
                        "data": daily_data,
                        "backgroundColor": "var(--color-primary-700)",
                    }, 
                ]
            }
        ),
        "chart_options":json.dumps({
                "scales": {
                    "y": {
                        "title": {
                            "display": True,
                            "text": "Ventas MLC"
                        }
                    }
                }
        }),
        
    }
    return data