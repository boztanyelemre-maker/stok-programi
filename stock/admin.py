from django.contrib import admin
from .models import ProjectStock, StockSlip, StockSlipItem, StockMovement, StockCount, StockCountItem


class StockSlipItemInline(admin.TabularInline):
    model = StockSlipItem
    extra = 1


@admin.register(StockSlip)
class StockSlipAdmin(admin.ModelAdmin):
    list_display = ['slip_no', 'slip_type', 'status', 'date', 'project', 'created_by']
    list_filter = ['slip_type', 'status', 'project']
    inlines = [StockSlipItemInline]


@admin.register(ProjectStock)
class ProjectStockAdmin(admin.ModelAdmin):
    list_display = ['product', 'project', 'warehouse', 'quantity']
    list_filter = ['project']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'project', 'date']
    list_filter = ['movement_type', 'project']
