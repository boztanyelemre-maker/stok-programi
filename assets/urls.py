from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('yeni/', views.asset_create, name='asset_create'),
    path('<int:pk>/', views.asset_detail, name='asset_detail'),
    path('<int:pk>/duzenle/', views.asset_edit, name='asset_edit'),
    path('<int:pk>/sil/', views.asset_delete, name='asset_delete'),
]
