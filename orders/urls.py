from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('yeni/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/onayla/', views.order_approve, name='order_approve'),
    path('<int:pk>/iptal/', views.order_cancel, name='order_cancel'),
    path('<int:pk>/teslim/', views.order_deliver, name='order_deliver'),
    path('teslim-raporu/', views.delivery_report, name='delivery_report'),
    path('siparisteki-urunler/', views.ordered_products, name='ordered_products'),
]
