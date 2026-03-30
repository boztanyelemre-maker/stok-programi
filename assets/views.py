from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Asset
from .forms import AssetForm


@login_required
def asset_list(request):
    assets = Asset.objects.select_related('project', 'warehouse', 'main_category').all()
    q = request.GET.get('q', '')
    if q:
        assets = assets.filter(
            Q(name__icontains=q) | Q(barcode__icontains=q) | Q(code__icontains=q) |
            Q(serial_no__icontains=q) | Q(brand__icontains=q)
        )
    status = request.GET.get('status')
    if status:
        assets = assets.filter(status=status)
    paginator = Paginator(assets, 20)
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    return render(request, 'assets/asset_list.html', {'assets': assets, 'q': q})


@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.created_by = request.user
            asset.save()
            messages.success(request, 'Demirbas eklendi.')
            return redirect('asset_list')
    else:
        form = AssetForm()
    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Demirbas Ekle'})


@login_required
def asset_edit(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Demirbas guncellendi.')
            return redirect('asset_list')
    else:
        form = AssetForm(instance=asset)
    return render(request, 'assets/asset_form.html', {'form': form, 'title': 'Demirbas Duzenle'})


@login_required
def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    return render(request, 'assets/asset_detail.html', {'asset': asset})


@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        asset.delete()
        messages.success(request, 'Demirbas silindi.')
    return redirect('asset_list')
