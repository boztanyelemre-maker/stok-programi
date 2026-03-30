from django.db import models
from django.conf import settings
from django.utils import timezone


class Asset(models.Model):
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('maintenance', 'Bakimda'),
        ('retired', 'Kullanim Disi'),
        ('lost', 'Kayip'),
    ]
    barcode = models.CharField('Barkod', max_length=100, unique=True)
    code = models.CharField('Demirbas Kodu', max_length=100, blank=True)
    name = models.CharField('Ad', max_length=500)
    serial_no = models.CharField('Seri No', max_length=200, blank=True)
    brand = models.CharField('Marka', max_length=200, blank=True)
    model = models.CharField('Model', max_length=200, blank=True)
    main_category = models.ForeignKey('products.MainCategory', on_delete=models.SET_NULL,
                                      null=True, blank=True, verbose_name='Ana Kategori')
    sub_category = models.ForeignKey('products.SubCategory', on_delete=models.SET_NULL,
                                     null=True, blank=True, verbose_name='Alt Kategori')
    unit = models.CharField('Birim', max_length=20, default='adet')
    quantity = models.DecimalField('Miktar', max_digits=12, decimal_places=2, default=1)
    project = models.ForeignKey('parameters.Project', on_delete=models.SET_NULL,
                                null=True, blank=True, verbose_name='Proje')
    warehouse = models.ForeignKey('parameters.Warehouse', on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='Depo')
    location = models.ForeignKey('parameters.Location', on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='Lokasyon')
    status = models.CharField('Durum', max_length=20, choices=STATUS_CHOICES, default='active')
    warranty_start = models.DateField('Garanti Baslangic', null=True, blank=True)
    warranty_years = models.IntegerField('Garanti Suresi (Yil)', default=0)
    maintenance_period_months = models.IntegerField('Bakim Periyodu (Ay)', default=0)
    last_maintenance_date = models.DateField('Son Bakim Tarihi', null=True, blank=True)
    next_maintenance_date = models.DateField('Sonraki Bakim Tarihi', null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, verbose_name='Zimmetli Kisi')
    notes = models.TextField('Notlar', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, verbose_name='Olusturan',
                                   related_name='created_assets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Demirbas'
        verbose_name_plural = 'Demirbaslar'
        ordering = ['name']

    def __str__(self):
        return f"{self.barcode} - {self.name}"

    @property
    def warranty_end(self):
        if self.warranty_start and self.warranty_years:
            return self.warranty_start.replace(year=self.warranty_start.year + self.warranty_years)
        return None

    @property
    def is_warranty_valid(self):
        end = self.warranty_end
        if end:
            return timezone.now().date() <= end
        return False

    @property
    def needs_maintenance(self):
        if self.next_maintenance_date:
            return timezone.now().date() >= self.next_maintenance_date
        return False
