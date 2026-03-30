from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import openpyxl
from .models import Product, MainCategory, SubCategory
from .forms import ProductForm, MainCategoryForm, SubCategoryForm


@login_required
def product_list(request):
    products = Product.objects.select_related('main_category', 'sub_category').filter(is_active=True)
    q = request.GET.get('q', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(barcode__icontains=q) |
                                   Q(stock_code__icontains=q) | Q(brand__icontains=q))
    cat = request.GET.get('category')
    if cat:
        products = products.filter(main_category_id=cat)

    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    categories = MainCategory.objects.all()
    return render(request, 'products/product_list.html',
                  {'products': products, 'q': q, 'categories': categories})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, 'Urun basariyla eklendi.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Yeni Urun Ekle'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Urun guncellendi.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Urun Duzenle'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        messages.success(request, 'Urun silindi.')
    return redirect('product_list')


@login_required
def product_export_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Urunler'
    headers = ['Barkod', 'Stok Kodu', 'Urun Adi', 'Birim', 'Fiyat', 'Ana Kategori',
               'Alt Kategori', 'Marka', 'Model', 'Toplam Stok']
    ws.append(headers)
    for p in Product.objects.filter(is_active=True).select_related('main_category', 'sub_category'):
        ws.append([
            p.barcode, p.stock_code, p.name, p.get_unit_display(), float(p.price),
            str(p.main_category) if p.main_category else '',
            str(p.sub_category.name) if p.sub_category else '',
            p.brand, p.model, float(p.get_total_stock())
        ])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=urunler.xlsx'
    wb.save(response)
    return response


@login_required
def category_list(request):
    main_cats = MainCategory.objects.prefetch_related('subcategories').all()
    main_form = MainCategoryForm()
    sub_form = SubCategoryForm()
    return render(request, 'products/category_list.html',
                  {'main_cats': main_cats, 'main_form': main_form, 'sub_form': sub_form})


@login_required
def main_category_create(request):
    if request.method == 'POST':
        form = MainCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ana kategori eklendi.')
    return redirect('category_list')


@login_required
def main_category_delete(request, pk):
    cat = get_object_or_404(MainCategory, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Ana kategori silindi.')
    return redirect('category_list')


@login_required
def sub_category_create(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alt kategori eklendi.')
    return redirect('category_list')


@login_required
def sub_category_delete(request, pk):
    cat = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Alt kategori silindi.')
    return redirect('category_list')


@login_required
def get_subcategories(request):
    main_id = request.GET.get('main_category_id')
    subs = SubCategory.objects.filter(main_category_id=main_id).values('id', 'name')
    return JsonResponse(list(subs), safe=False)
