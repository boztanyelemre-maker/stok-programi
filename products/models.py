from django.db import models
from django.conf import settings


class MainCategory(models.Model):
    name = models.CharField('Ana Kategori', max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ana Kategori'
        verbose_name_plural = 'Ana Kategoriler'
        ordering = ['name']

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE,
                                      verbose_name='Ana Kategori', related_name='subcategories')
    name = models.CharField('Alt Kategori', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Alt Kategori'
        verbose_name_plural = 'Alt Kategoriler'
        ordering = ['name']
        unique_together = ['main_category', 'name']

    def __str__(self):
        return f"{self.main_category.name} > {self.name}"


class Product(models.Model):
    UNIT_CHOICES = [
        ('adet', 'Adet'),
        ('kg', 'Kilogram'),
        ('lt', 'Litre'),
        ('mt', 'Metre'),
        ('m2', 'Metrekare'),
        ('paket', 'Paket'),
        ('kutu', 'Kutu'),
        ('takim', 'Takim'),
        ('cift', 'Cift'),
        ('top', 'Top'),
    ]
    barcode = models.CharField('Barkod', max_length=100, unique=True)
    stock_code = models.CharField('Stok Kodu', max_length=100, blank=True)
    name = models.CharField('Urun Adi', max_length=500)
    unit = models.CharField('Birim', max_length=20, choices=UNIT_CHOICES, default='adet')
    price = models.DecimalField('Fiyat', max_digits=12, decimal_places=2, default=0)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Ana Kategori')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Alt Kategori')
    brand = models.CharField('Marka', max_length=200, blank=True)
    model = models.CharField('Model', max_length=200, blank=True)
    description = models.TextField('Aciklama', blank=True)
    critical_stock_level = models.DecimalField('Kritik Stok Seviyesi', max_digits=12, decimal_places=2,
                                               default=10)
    image = models.ImageField('Urun Resmi', upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField('Aktif', default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   verbose_name='Olusturan', related_name='created_products')
    created_at = models.DateTimeField('Olusturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Guncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Urun'
        verbose_name_plural = 'Urunler'
        ordering = ['name']

    def __str__(self):
        return f"{self.barcode} - {self.name}"

    def get_total_stock(self):
        from stock.models import ProjectStock
        return ProjectStock.objects.filter(product=self).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    @property
    def is_critical(self):
        return self.get_total_stock() <= self.critical_stock_level
