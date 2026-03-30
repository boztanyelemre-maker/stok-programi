from django.urls import path
from . import views

urlpatterns = [
    path('giris-fisi/', views.stock_entry, name='stock_entry'),
    path('cikis-fisi/', views.stock_exit, name='stock_exit'),
    path('transfer-fisi/', views.stock_transfer, name='stock_transfer'),
    path('teslim-fisi/', views.stock_delivery, name='stock_delivery'),
    path('fisler/', views.stock_slip_list, name='stock_slip_list'),
    path('fisler/<int:pk>/', views.stock_slip_detail, name='stock_slip_detail'),
    path('liste/', views.stock_list, name='stock_list'),
    path('hareketler/', views.stock_movements, name='stock_movements'),
    path('kritik/', views.critical_stock, name='critical_stock'),
    path('kritik/excel/', views.critical_stock_export, name='critical_stock_export'),
    path('sayim/', views.stock_count_form, name='stock_count_form'),
    path('sayim/liste/', views.stock_count_list, name='stock_count_list'),
    path('api/sayim-urunler/', views.stock_count_products, name='stock_count_products'),
    path('api/depolar/', views.get_warehouses, name='get_warehouses'),
]
