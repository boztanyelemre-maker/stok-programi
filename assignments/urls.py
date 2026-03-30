from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('yeni/', views.assignment_create, name='assignment_create'),
    path('<int:pk>/duzenle/', views.assignment_edit, name='assignment_edit'),
    path('<int:pk>/iade/', views.assignment_return, name='assignment_return'),
    path('<int:pk>/sil/', views.assignment_delete, name='assignment_delete'),
]
