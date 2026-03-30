from django.db import models
from django.conf import settings


class ProjectStock(models.Model):
    """Her proje+depo+urun kombinasyonu icin stok miktari"""
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE,
                                verbose_name='Urun', related_name='project_stocks')
    project = models.ForeignKey('parameters.Project', on_delete=models.CASCADE,
                                verbose_name='Proje', related_name='stocks')
    warehouse = models.ForeignKey('parameters.Warehouse', on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='Depo')
    location = models.ForeignKey('parameters.Location', on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='Lokasyon')
    room = models.ForeignKey('parameters.Room', on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name='Oda')
    quantity = models.DecimalField('Miktar', max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Proje Stok'
        verbose_name_plural = 'Proje Stoklari'
        unique_together = ['product', 'project', 'warehouse', 'location', 'room']

    def __str__(self):
        return f"{self.product.name} - {self.project.name}: {self.quantity}"


class StockSlip(models.Model):
    SLIP_TYPES = [
        ('entry', 'Giris Fisi'),
        ('exit', 'Cikis Fisi'),
        ('transfer', 'Transfer Fisi'),
        ('count', 'Sayim Fisi'),
        ('delivery', 'Teslim Fisi'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Taslak'),
        ('confirmed', 'Onaylandi'),
        ('cancelled', 'Iptal Edildi'),
    ]
    slip_no = models.CharField('Fis No', max_length=50, unique=True)
    slip_type = models.CharField('Fis Turu', max_length=20, choices=SLIP_TYPES)
    status = models.CharField('Durum', max_length=20, choices=STATUS_CHOICES, default='draft')
    date = models.DateField('Tarih')
    time = models.TimeField('Saat')
    project = models.ForeignKey('parameters.Project', on_delete=models.CASCADE,
                                verbose_name='Proje', related_name='slips')
    warehouse = models.ForeignKey('parameters.Warehouse', on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='Depo')
    description = models.TextField('Aciklama', blank=True)
    # Transfer icin
    target_project = models.ForeignKey('parameters.Project', on_delete=models.SET_NULL,
                                       null=True, blank=True, verbose_name='Hedef Proje',
                                       related_name='incoming_slips')
    target_warehouse = models.ForeignKey('parameters.Warehouse', on_delete=models.SET_NULL,
                                         null=True, blank=True, verbose_name='Hedef Depo',
                                         related_name='incoming_slips')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name='Stok Personeli',
                              related_name='handled_slips')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, verbose_name='Olusturan',
                                   related_name='created_slips')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, verbose_name='Onaylayan',
                                    related_name='approved_slips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stok Fisi'
        verbose_name_plural = 'Stok Fisleri'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.get_slip_type_display()} - {self.slip_no}"

    @property
    def total_quantity(self):
        return self.items.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def total_amount(self):
        total = 0
        for item in self.items.all():
            total += item.quantity * item.unit_price
        return total


class StockSlipItem(models.Model):
    slip = models.ForeignKey(StockSlip, on_delete=models.CASCADE,
                             verbose_name='Fis', related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE,
                                verbose_name='Urun')
    quantity = models.DecimalField('Miktar', max_digits=12, decimal_places=2)
    unit_price = models.DecimalField('Birim Fiyat', max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Fis Kalemi'
        verbose_name_plural = 'Fis Kalemleri'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Giris'),
        ('out', 'Cikis'),
        ('transfer_out', 'Transfer Cikis'),
        ('transfer_in', 'Transfer Giris'),
        ('count_adj', 'Sayim Duzeltme'),
    ]
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE,
                                verbose_name='Urun', related_name='movements')
    project = models.ForeignKey('parameters.Project', on_delete=models.CASCADE,
                                verbose_name='Proje')
    warehouse = models.ForeignKey('parameters.Warehouse', on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='Depo')
    movement_type = models.CharField('Hareket Turu', max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField('Miktar', max_digits=12, decimal_places=2)
    slip = models.ForeignKey(StockSlip, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Fis', related_name='movements')
    description = models.TextField('Aciklama', blank=True)
    date = models.DateTimeField('Tarih')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, verbose_name='Islem Yapan')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stok Hareketi'
        verbose_name_plural = 'Stok Hareketleri'
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} x {self.quantity}"


class StockCount(models.Model):
    """Stok sayim kaydi"""
    STATUS_CHOICES = [
        ('pending', 'Bekliyor'),
        ('completed', 'Tamamlandi'),
        ('approved', 'Onaylandi'),
    ]
    slip = models.OneToOneField(StockSlip, on_delete=models.CASCADE, verbose_name='Fis',
                                related_name='count_record')
    project = models.ForeignKey('parameters.Project', on_delete=models.CASCADE,
                                verbose_name='Proje')
    warehouse = models.ForeignKey('parameters.Warehouse', on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='Depo')
    count_date = models.DateField('Sayim Tarihi')
    status = models.CharField('Durum', max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField('Notlar', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stok Sayim'
        verbose_name_plural = 'Stok Sayimlari'
        ordering = ['-count_date']


class StockCountItem(models.Model):
    count = models.ForeignKey(StockCount, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='Urun')
    system_quantity = models.DecimalField('Sistem Miktari', max_digits=12, decimal_places=2)
    counted_quantity = models.DecimalField('Sayilan Miktar', max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Sayim Kalemi'
        verbose_name_plural = 'Sayim Kalemleri'

    @property
    def difference(self):
        return self.counted_quantity - self.system_quantity
