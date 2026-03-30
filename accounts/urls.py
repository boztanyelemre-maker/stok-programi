from django.urls import path
from . import views

urlpatterns = [
    path('giris/', views.login_view, name='login'),
    path('cikis/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile'),
    path('sifre-degistir/', views.change_password_view, name='change_password'),
    path('kullanicilar/', views.user_list_view, name='user_list'),
    path('kullanicilar/yeni/', views.user_create_view, name='user_create'),
    path('kullanicilar/<int:pk>/duzenle/', views.user_edit_view, name='user_edit'),
    path('kullanicilar/<int:pk>/onayla/', views.user_approve_view, name='user_approve'),
]
