from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from products.models import Product
from stock.models import ProjectStock, StockMovement, StockSlip
from orders.models import Order
from assets.models import Asset
from assignments.models import Assignment
from parameters.models import Project


@login_required
def dashboard(request):
    today = timezone.now().date()
    last_30 = today - timedelta(days=30)
    last_7 = today - timedelta(days=7)

    # Ozet kartlar
    total_products = Product.objects.filter(is_active=True).count()
    total_stock_value = 0
    critical_count = 0
    for p in Product.objects.filter(is_active=True):
        total = p.get_total_stock()
        total_stock_value += total * p.price
        if total <= p.critical_stock_level:
            critical_count += 1

    total_projects = Project.objects.filter(is_active=True).count()
    pending_orders = Order.objects.filter(status='pending').count()
    active_assignments = Assignment.objects.filter(status='active').count()
    total_assets = Asset.objects.count()

    # Son stok hareketleri
    recent_movements = StockMovement.objects.select_related(
        'product', 'project', 'created_by'
    ).order_by('-created_at')[:10]

    # Son siparisler
    recent_orders = Order.objects.select_related(
        'project', 'requested_by'
    ).order_by('-created_at')[:5]

    # Son 30 gun giris/cikis ozeti
    movements_30d = StockMovement.objects.filter(date__date__gte=last_30)
    total_in = movements_30d.filter(movement_type='in').aggregate(
        total=Sum('quantity'))['total'] or 0
    total_out = movements_30d.filter(movement_type='out').aggregate(
        total=Sum('quantity'))['total'] or 0

    # Bakim gereken demirbaslar
    maintenance_needed = Asset.objects.filter(
        next_maintenance_date__lte=today,
        status='active'
    ).count()

    # Garanti biten demirbaslar (30 gun icinde)
    warranty_expiring = 0
    for a in Asset.objects.filter(status='active'):
        end = a.warranty_end
        if end and today <= end <= today + timedelta(days=30):
            warranty_expiring += 1

    # Gunluk hareket grafigi icin veri (son 7 gun)
    daily_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_in = StockMovement.objects.filter(
            date__date=d, movement_type='in'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        day_out = StockMovement.objects.filter(
            date__date=d, movement_type='out'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        daily_data.append({
            'date': d.strftime('%d/%m'),
            'in': float(day_in),
            'out': float(day_out),
        })

    context = {
        'total_products': total_products,
        'total_stock_value': total_stock_value,
        'critical_count': critical_count,
        'total_projects': total_projects,
        'pending_orders': pending_orders,
        'active_assignments': active_assignments,
        'total_assets': total_assets,
        'recent_movements': recent_movements,
        'recent_orders': recent_orders,
        'total_in': total_in,
        'total_out': total_out,
        'maintenance_needed': maintenance_needed,
        'warranty_expiring': warranty_expiring,
        'daily_data': daily_data,
    }
    return render(request, 'core/dashboard.html', context)
