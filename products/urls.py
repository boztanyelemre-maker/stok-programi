from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('yeni/', views.product_create, name='product_create'),
    path('<int:pk>/duzenle/', views.product_edit, name='product_edit'),
    path('<int:pk>/sil/', views.product_delete, name='product_delete'),
    path('excel/', views.product_export_excel, name='product_export_excel'),
    path('kategoriler/', views.category_list, name='category_list'),
    path('kategoriler/ana/ekle/', views.main_category_create, name='main_category_create'),
    path('kategoriler/ana/<int:pk>/sil/', views.main_category_delete, name='main_category_delete'),
    path('kategoriler/alt/ekle/', views.sub_category_create, name='sub_category_create'),
    path('kategoriler/alt/<int:pk>/sil/', views.sub_category_delete, name='sub_category_delete'),
    path('api/alt-kategoriler/', views.get_subcategories, name='get_subcategories'),
]
