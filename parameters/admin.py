from django.contrib import admin
from .models import Project, Warehouse, Location, Room, GeneralSettings


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'is_active']
    list_filter = ['project']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'warehouse', 'is_active']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active']


@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    list_display = ['stock_entry_counter', 'stock_exit_counter', 'transfer_counter']
