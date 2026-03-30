from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import openpyxl
from datetime import datetime

from .models import ProjectStock, StockSlip, StockSlipItem, StockMovement, StockCount, StockCountItem
from .forms import StockSlipForm, StockSlipItemFormSet, StockTransferForm, StockFilterForm
from products.models import Product
from parameters.models import Project, Warehouse, GeneralSettings


def _generate_slip_no(slip_type):
    settings = GeneralSettings.get_settings()
    counter_map = {
        'entry': ('stock_entry_counter', 'GF'),
        'exit': ('stock_exit_counter', 'CF'),
        'transfer': ('transfer_counter', 'TF'),
        'count': ('count_counter', 'SF'),
        'delivery': ('delivery_counter', 'TES'),
    }
    field, prefix = counter_map[slip_type]
    counter = getattr(settings, field)
    slip_no = f"{prefix}-{counter:06d}"
    setattr(settings, field, counter + 1)
    settings.save()
    return slip_no


def _apply_stock_movement(slip):
    """Fis onaylandiginda stok hareketlerini uygula"""
    for item in slip.items.all():
        if slip.slip_type == 'entry':
            ps, _ = ProjectStock.objects.get_or_create(
                product=item.product, project=slip.project,
                warehouse=slip.warehouse,
                defaults={'quantity': 0}
            )
            ps.quantity += item.quantity
            ps.save()
            StockMovement.objects.create(
                product=item.product, project=slip.project,
                warehouse=slip.warehouse, movement_type='in',
                quantity=item.quantity, slip=slip,
                date=timezone.now(), created_by=slip.created_by
            )
        elif slip.slip_type == 'exit':
            try:
                ps = ProjectStock.objects.get(
                    product=item.product, project=slip.project,
                    warehouse=slip.warehouse
                )
                ps.quantity -= item.quantity
                ps.save()
            except ProjectStock.DoesNotExist:
                pass
            StockMovement.objects.create(
                product=item.product, project=slip.project,
                warehouse=slip.warehouse, movement_type='out',
                quantity=item.quantity, slip=slip,
                date=timezone.now(), created_by=slip.created_by
            )
        elif slip.slip_type == 'transfer':
            # Kaynaktan dusur
            try:
                ps_source = ProjectStock.objects.get(
                    product=item.product, project=slip.project,
                    warehouse=slip.warehouse
                )
                ps_source.quantity -= item.quantity
                ps_source.save()
            except ProjectStock.DoesNotExist:
                pass
            StockMovement.objects.create(
                product=item.product, project=slip.project,
                warehouse=slip.warehouse, movement_type='transfer_out',
                quantity=item.quantity, slip=slip,
                date=timezone.now(), created_by=slip.created_by
            )
            # Hedefe ekle
            ps_target, _ = ProjectStock.objects.get_or_create(
                product=item.product,
                project=slip.target_project,
                warehouse=slip.target_warehouse,
                defaults={'quantity': 0}
            )
            ps_target.quantity += item.quantity
            ps_target.save()
            StockMovement.objects.create(
                product=item.product, project=slip.target_project,
                warehouse=slip.target_warehouse, movement_type='transfer_in',
                quantity=item.quantity, slip=slip,
                date=timezone.now(), created_by=slip.created_by
            )


@login_required
def stock_entry(request):
    if request.method == 'POST':
        form = StockSlipForm(request.POST)
        formset = StockSlipItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            slip = form.save(commit=False)
            slip.slip_type = 'entry'
            slip.slip_no = _generate_slip_no('entry')
            slip.created_by = request.user
            slip.status = 'confirmed'
            slip.save()
            formset.instance = slip
            formset.save()
            _apply_stock_movement(slip)
            messages.success(request, f'Giris fisi {slip.slip_no} olusturuldu.')
            return redirect('stock_slip_list')
    else:
        form = StockSlipForm(initial={'date': timezone.now().date(),
                                      'time': timezone.now().time()})
        formset = StockSlipItemFormSet()
    return render(request, 'stock/slip_form.html', {
        'form': form, 'formset': formset, 'title': 'Stok Giris Fisi',
        'slip_type': 'entry'
    })


@login_required
def stock_exit(request):
    if request.method == 'POST':
        form = StockSlipForm(request.POST)
        formset = StockSlipItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            slip = form.save(commit=False)
            slip.slip_type = 'exit'
            slip.slip_no = _generate_slip_no('exit')
            slip.created_by = request.user
            slip.status = 'confirmed'
            slip.save()
            formset.instance = slip
            formset.save()
            _apply_stock_movement(slip)
            messages.success(request, f'Cikis fisi {slip.slip_no} olusturuldu.')
            return redirect('stock_slip_list')
    else:
        form = StockSlipForm(initial={'date': timezone.now().date(),
                                      'time': timezone.now().time()})
        formset = StockSlipItemFormSet()
    return render(request, 'stock/slip_form.html', {
        'form': form, 'formset': formset, 'title': 'Stok Cikis Fisi',
        'slip_type': 'exit'
    })


@login_required
def stock_transfer(request):
    if request.method == 'POST':
        form = StockSlipForm(request.POST)
        formset = StockSlipItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            slip = form.save(commit=False)
            slip.slip_type = 'transfer'
            slip.slip_no = _generate_slip_no('transfer')
            slip.created_by = request.user
            slip.status = 'confirmed'
            slip.save()
            formset.instance = slip
            formset.save()
            _apply_stock_movement(slip)
            messages.success(request, f'Transfer fisi {slip.slip_no} olusturuldu.')
            return redirect('stock_slip_list')
    else:
        form = StockSlipForm(initial={'date': timezone.now().date(),
                                      'time': timezone.now().time()})
        formset = StockSlipItemFormSet()
    return render(request, 'stock/slip_form.html', {
        'form': form, 'formset': formset, 'title': 'Transfer Fisi',
        'slip_type': 'transfer'
    })


@login_required
def stock_delivery(request):
    if request.method == 'POST':
        form = StockSlipForm(request.POST)
        formset = StockSlipItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            slip = form.save(commit=False)
            slip.slip_type = 'delivery'
            slip.slip_no = _generate_slip_no('delivery')
            slip.created_by = request.user
            slip.status = 'confirmed'
            slip.save()
            formset.instance = slip
            formset.save()
            _apply_stock_movement(slip)
            messages.success(request, f'Teslim fisi {slip.slip_no} olusturuldu.')
            return redirect('stock_slip_list')
    else:
        form = StockSlipForm(initial={'date': timezone.now().date(),
                                      'time': timezone.now().time()})
        formset = StockSlipItemFormSet()
    return render(request, 'stock/slip_form.html', {
        'form': form, 'formset': formset, 'title': 'Teslim Fisi',
        'slip_type': 'delivery'
    })


@login_required
def stock_slip_list(request):
    slips = StockSlip.objects.select_related('project', 'created_by').all()
    slip_type = request.GET.get('type')
    if slip_type:
        slips = slips.filter(slip_type=slip_type)
    q = request.GET.get('q', '')
    if q:
        slips = slips.filter(Q(slip_no__icontains=q) | Q(description__icontains=q))

    form = StockFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('project'):
            slips = slips.filter(project=form.cleaned_data['project'])
        if form.cleaned_data.get('start_date'):
            slips = slips.filter(date__gte=form.cleaned_data['start_date'])
        if form.cleaned_data.get('end_date'):
            slips = slips.filter(date__lte=form.cleaned_data['end_date'])

    paginator = Paginator(slips, 20)
    page = request.GET.get('page')
    slips = paginator.get_page(page)
    return render(request, 'stock/slip_list.html', {
        'slips': slips, 'q': q, 'filter_form': form, 'slip_type': slip_type
    })


@login_required
def stock_slip_detail(request, pk):
    slip = get_object_or_404(StockSlip.objects.prefetch_related('items__product'), pk=pk)
    return render(request, 'stock/slip_detail.html', {'slip': slip})


@login_required
def stock_list(request):
    stocks = ProjectStock.objects.select_related('product', 'project', 'warehouse').filter(
        quantity__gt=0
    )
    q = request.GET.get('q', '')
    if q:
        stocks = stocks.filter(Q(product__name__icontains=q) | Q(product__barcode__icontains=q))
    project = request.GET.get('project')
    if project:
        stocks = stocks.filter(project_id=project)

    paginator = Paginator(stocks, 20)
    page = request.GET.get('page')
    stocks = paginator.get_page(page)
    projects = Project.objects.filter(is_active=True)
    return render(request, 'stock/stock_list.html', {
        'stocks': stocks, 'q': q, 'projects': projects
    })


@login_required
def stock_movements(request):
    movements = StockMovement.objects.select_related('product', 'project', 'created_by').all()
    q = request.GET.get('q', '')
    if q:
        movements = movements.filter(
            Q(product__name__icontains=q) | Q(product__barcode__icontains=q)
        )
    form = StockFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('project'):
            movements = movements.filter(project=form.cleaned_data['project'])
        if form.cleaned_data.get('start_date'):
            movements = movements.filter(date__date__gte=form.cleaned_data['start_date'])
        if form.cleaned_data.get('end_date'):
            movements = movements.filter(date__date__lte=form.cleaned_data['end_date'])

    paginator = Paginator(movements, 20)
    page = request.GET.get('page')
    movements = paginator.get_page(page)
    return render(request, 'stock/movement_list.html', {
        'movements': movements, 'q': q, 'filter_form': form
    })


@login_required
def critical_stock(request):
    products = Product.objects.filter(is_active=True)
    critical_products = []
    for p in products:
        total = p.get_total_stock()
        if total <= p.critical_stock_level:
            critical_products.append({
                'product': p,
                'total_stock': total,
                'critical_level': p.critical_stock_level
            })
    return render(request, 'stock/critical_stock.html', {
        'critical_products': critical_products
    })


@login_required
def critical_stock_export(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Kritik Stok'
    ws.append(['Ad', 'Kod', 'Barkod', 'Mevcut Miktar', 'Kritik Seviye'])
    for p in Product.objects.filter(is_active=True):
        total = p.get_total_stock()
        if total <= p.critical_stock_level:
            ws.append([p.name, p.stock_code, p.barcode, float(total), float(p.critical_stock_level)])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=kritik_stok.xlsx'
    wb.save(response)
    return response


@login_required
def stock_count_form(request):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        warehouse_id = request.POST.get('warehouse')
        project = get_object_or_404(Project, pk=project_id)
        warehouse = Warehouse.objects.filter(pk=warehouse_id).first() if warehouse_id else None

        slip = StockSlip.objects.create(
            slip_no=_generate_slip_no('count'),
            slip_type='count',
            date=timezone.now().date(),
            time=timezone.now().time(),
            project=project,
            warehouse=warehouse,
            created_by=request.user,
            status='confirmed'
        )
        count = StockCount.objects.create(
            slip=slip, project=project, warehouse=warehouse,
            count_date=timezone.now().date(),
            created_by=request.user, status='completed'
        )

        product_ids = request.POST.getlist('product_id')
        counted_qtys = request.POST.getlist('counted_qty')
        system_qtys = request.POST.getlist('system_qty')

        for pid, cqty, sqty in zip(product_ids, counted_qtys, system_qtys):
            product = Product.objects.get(pk=pid)
            cqty = float(cqty or 0)
            sqty = float(sqty or 0)
            StockCountItem.objects.create(
                count=count, product=product,
                system_quantity=sqty, counted_quantity=cqty
            )
            diff = cqty - sqty
            if diff != 0:
                ps, _ = ProjectStock.objects.get_or_create(
                    product=product, project=project, warehouse=warehouse,
                    defaults={'quantity': 0}
                )
                ps.quantity = cqty
                ps.save()
                StockMovement.objects.create(
                    product=product, project=project, warehouse=warehouse,
                    movement_type='count_adj', quantity=abs(diff),
                    slip=slip, description=f'Sayim duzeltme: {sqty} -> {cqty}',
                    date=timezone.now(), created_by=request.user
                )

        messages.success(request, 'Sayim kaydedildi.')
        return redirect('stock_count_list')

    projects = Project.objects.filter(is_active=True)
    return render(request, 'stock/count_form.html', {'projects': projects})


@login_required
def stock_count_list(request):
    counts = StockCount.objects.select_related('project', 'slip').all()
    paginator = Paginator(counts, 20)
    page = request.GET.get('page')
    counts = paginator.get_page(page)
    return render(request, 'stock/count_list.html', {'counts': counts})


@login_required
def stock_count_products(request):
    """AJAX: Proje ve depoya gore urun listesi + sistem stok miktarlari"""
    project_id = request.GET.get('project')
    warehouse_id = request.GET.get('warehouse')
    stocks = ProjectStock.objects.filter(project_id=project_id).select_related('product')
    if warehouse_id:
        stocks = stocks.filter(warehouse_id=warehouse_id)
    data = [{'id': s.product.id, 'barcode': s.product.barcode,
             'name': s.product.name, 'quantity': float(s.quantity)}
            for s in stocks]
    return JsonResponse(data, safe=False)


@login_required
def get_warehouses(request):
    project_id = request.GET.get('project_id')
    whs = Warehouse.objects.filter(project_id=project_id, is_active=True).values('id', 'name')
    return JsonResponse(list(whs), safe=False)
