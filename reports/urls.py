from django.urls import path
from . import views

urlpatterns = [
    path('stok/', views.stock_report, name='stock_report'),
    path('transfer/', views.transfer_report, name='transfer_report'),
    path('transfer-maliyet/', views.transfer_cost_report, name='transfer_cost_report'),
    path('grup/', views.group_report, name='group_report'),
    path('proje-stok/', views.project_stock_report, name='project_stock_report'),
    path('proje-stok/excel/', views.project_stock_export, name='project_stock_export'),
]
