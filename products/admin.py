from django.contrib import admin
from .models import Product, MainCategory, SubCategory


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'main_category', 'created_at']
    list_filter = ['main_category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['barcode', 'name', 'unit', 'price', 'main_category', 'brand', 'is_active']
    list_filter = ['main_category', 'unit', 'is_active']
    search_fields = ['barcode', 'name', 'stock_code']
