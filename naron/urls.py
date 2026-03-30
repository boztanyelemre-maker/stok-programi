from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('hesap/', include('accounts.urls')),
    path('urunler/', include('products.urls')),
    path('stok/', include('stock.urls')),
    path('siparisler/', include('orders.urls')),
    path('demirbaslar/', include('assets.urls')),
    path('zimmet/', include('assignments.urls')),
    path('raporlar/', include('reports.urls')),
    path('parametreler/', include('parameters.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
