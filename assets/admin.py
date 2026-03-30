from django.contrib import admin
from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['barcode', 'name', 'brand', 'project', 'status', 'assigned_to']
    list_filter = ['status', 'project', 'main_category']
    search_fields = ['barcode', 'name', 'serial_no']
