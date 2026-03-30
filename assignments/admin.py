from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['assigned_to_name', 'project', 'product', 'asset', 'status', 'assignment_date']
    list_filter = ['status', 'project']
    search_fields = ['assigned_to_name', 'tc_kimlik']
