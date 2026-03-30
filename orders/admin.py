from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'project', 'order_type', 'status', 'date', 'requested_by']
    list_filter = ['status', 'order_type', 'project']
    inlines = [OrderItemInline]
