from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet
from parameters.models import GeneralSettings


@login_required
def order_list(request):
    orders = Order.objects.select_related('project', 'requested_by').all()
    q = request.GET.get('q', '')
    status = request.GET.get('status')
    if q:
        orders = orders.filter(Q(order_no__icontains=q) | Q(notes__icontains=q))
    if status:
        orders = orders.filter(status=status)
    paginator = Paginator(orders, 20)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    return render(request, 'orders/order_list.html', {'orders': orders, 'q': q})


@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            last = Order.objects.order_by('-id').first()
            order.order_no = str((last.id + 1) if last else 1).zfill(6)
            order.requested_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, f'Siparis {order.order_no} olusturuldu.')
            return redirect('order_list')
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, 'orders/order_form.html', {
        'form': form, 'formset': formset, 'title': 'Yeni Siparis'
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_approve(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = 'approved'
        order.approved_by = request.user
        order.save()
        messages.success(request, f'Siparis {order.order_no} onaylandi.')
    return redirect('order_list')


@login_required
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Siparis {order.order_no} iptal edildi.')
    return redirect('order_list')


@login_required
def order_deliver(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        for item in order.items.all():
            delivered = request.POST.get(f'delivered_{item.id}')
            if delivered:
                item.delivered_quantity = float(delivered)
                item.save()
        all_delivered = all(
            item.delivered_quantity >= item.quantity for item in order.items.all()
        )
        if all_delivered:
            order.status = 'delivered'
            order.delivery_date = timezone.now().date()
        else:
            order.status = 'shipped'
        order.save()
        messages.success(request, 'Teslim bilgileri guncellendi.')
    return redirect('order_detail', pk=pk)


@login_required
def delivery_report(request):
    orders = Order.objects.filter(
        status__in=['shipped', 'delivered']
    ).select_related('project').prefetch_related('items__product')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    if start:
        orders = orders.filter(delivery_date__gte=start)
    if end:
        orders = orders.filter(delivery_date__lte=end)
    return render(request, 'orders/delivery_report.html', {'orders': orders})


@login_required
def ordered_products(request):
    """Siparisteki urunler raporu"""
    items = OrderItem.objects.filter(
        order__status__in=['pending', 'approved', 'preparing']
    ).select_related('product', 'order__project')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    if start:
        items = items.filter(order__date__gte=start)
    if end:
        items = items.filter(order__date__lte=end)
    return render(request, 'orders/ordered_products.html', {'items': items})
