from django.urls import path
from . import views

urlpatterns = [
    path('projeler/', views.project_settings, name='project_settings'),
    path('projeler/ekle/', views.project_create, name='project_create'),
    path('projeler/<int:pk>/duzenle/', views.project_edit, name='project_edit'),
    path('projeler/<int:pk>/sil/', views.project_delete, name='project_delete'),
    path('lokasyonlar/', views.location_settings, name='location_settings'),
    path('depo/ekle/', views.warehouse_create, name='warehouse_create'),
    path('depo/<int:pk>/sil/', views.warehouse_delete, name='warehouse_delete'),
    path('lokasyon/ekle/', views.location_create, name='location_create'),
    path('lokasyon/<int:pk>/sil/', views.location_delete, name='location_delete'),
    path('oda/ekle/', views.room_create, name='room_create'),
    path('oda/<int:pk>/sil/', views.room_delete, name='room_delete'),
    path('genel/', views.general_settings, name='general_settings'),
    path('api/lokasyonlar/', views.api_locations, name='api_locations'),
    path('api/odalar/', views.api_rooms, name='api_rooms'),
]
