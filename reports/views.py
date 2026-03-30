from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Q
from django.http import HttpResponse
from django.core.paginator import Paginator
import openpyxl

from stock.models import StockMovement, StockSlip, ProjectStock
from products.models import Product, MainCategory
from parameters.models import Project


@login_required
def stock_report(request):
    movements = StockMovement.objects.select_related(
        'product', 'project', 'created_by'
    ).all()
    project = request.GET.get('project')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    q = request.GET.get('q', '')

    if project:
        movements = movements.filter(project_id=project)
    if start:
        movements = movements.filter(date__date__gte=start)
    if end:
        movements = movements.filter(date__date__lte=end)
    if q:
        movements = movements.filter(
            Q(product__name__icontains=q) | Q(product__barcode__icontains=q)
        )

    paginator = Paginator(movements, 20)
    page = request.GET.get('page')
    movements = paginator.get_page(page)
    projects = Project.objects.filter(is_active=True)
    return render(request, 'reports/stock_report.html', {
        'movements': movements, 'projects': projects, 'q': q
    })


@login_required
def transfer_report(request):
    transfers = StockSlip.objects.filter(slip_type='transfer').select_related(
        'project', 'target_project', 'created_by'
    ).prefetch_related('items__product')
    project = request.GET.get('project')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    if project:
        transfers = transfers.filter(Q(project_id=project) | Q(target_project_id=project))
    if start:
        transfers = transfers.filter(date__gte=start)
    if end:
        transfers = transfers.filter(date__lte=end)

    paginator = Paginator(transfers, 20)
    page = request.GET.get('page')
    transfers = paginator.get_page(page)
    projects = Project.objects.filter(is_active=True)
    return render(request, 'reports/transfer_report.html', {
        'transfers': transfers, 'projects': projects
    })


@login_required
def transfer_cost_report(request):
    transfers = StockSlip.objects.filter(slip_type='transfer').select_related(
        'project', 'target_project'
    ).prefetch_related('items__product')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    staff = request.GET.get('staff')

    if start:
        transfers = transfers.filter(date__gte=start)
    if end:
        transfers = transfers.filter(date__lte=end)
    if staff:
        transfers = transfers.filter(created_by_id=staff)

    cost_data = []
    for t in transfers:
        for item in t.items.all():
            cost_data.append({
                'barcode': item.product.barcode,
                'name': item.product.name,
                'quantity': item.quantity,
                'cost': item.quantity * item.unit_price,
                'date': t.date,
                'project': t.project.name,
                'target': t.target_project.name if t.target_project else '-',
            })
    return render(request, 'reports/transfer_cost_report.html', {'cost_data': cost_data})


@login_required
def group_report(request):
    category = request.GET.get('category')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    data = []
    categories = MainCategory.objects.all()

    if category:
        movements = StockMovement.objects.filter(
            product__main_category_id=category
        )
        if start:
            movements = movements.filter(date__date__gte=start)
        if end:
            movements = movements.filter(date__date__lte=end)

        data = movements.values(
            'product__name', 'product__barcode'
        ).annotate(
            total_in=Sum('quantity', filter=Q(movement_type='in')),
            total_out=Sum('quantity', filter=Q(movement_type='out')),
        )

    return render(request, 'reports/group_report.html', {
        'data': data, 'categories': categories
    })


@login_required
def project_stock_report(request):
    project = request.GET.get('project')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    data = []
    projects = Project.objects.filter(is_active=True)

    if project:
        movements = StockMovement.objects.filter(
            project_id=project, movement_type='out'
        ).select_related('product')
        if start:
            movements = movements.filter(date__date__gte=start)
        if end:
            movements = movements.filter(date__date__lte=end)

        data = movements.values(
            'product__barcode', 'product__name'
        ).annotate(
            total_qty=Sum('quantity'),
            total_cost=Sum(F('quantity') * F('product__price'))
        )

    return render(request, 'reports/project_stock_report.html', {
        'data': data, 'projects': projects
    })


@login_required
def project_stock_export(request):
    project_id = request.GET.get('project')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    movements = StockMovement.objects.filter(
        project_id=project_id, movement_type='out'
    ).select_related('product')
    if start:
        movements = movements.filter(date__date__gte=start)
    if end:
        movements = movements.filter(date__date__lte=end)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Proje Stok Cikis'
    ws.append(['Barkod', 'Urun Adi', 'Miktar', 'Birim Fiyat', 'Toplam Tutar', 'Tarih'])
    for m in movements:
        ws.append([m.product.barcode, m.product.name, float(m.quantity),
                   float(m.product.price), float(m.quantity * m.product.price),
                   m.date.strftime('%d/%m/%Y')])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=proje_stok_cikis.xlsx'
    wb.save(response)
    return response
