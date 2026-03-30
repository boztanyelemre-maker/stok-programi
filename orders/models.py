from django.db import models
from django.conf import settings


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('standard', 'Standart'),
        ('urgent', 'Acil'),
        ('planned', 'Planli'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandi'),
        ('preparing', 'Hazirlaniyor'),
        ('shipped', 'Gonderildi'),
        ('delivered', 'Teslim Edildi'),
        ('cancelled', 'Iptal'),
    ]
    order_no = models.CharField('Siparis No', max_length=50, unique=True)
    project = models.ForeignKey('parameters.Project', on_delete=models.CASCADE,
                                verbose_name='Proje', related_name='orders')
    warehouse = models.ForeignKey('parameters.Warehouse', on_delete=models.SET_NULL,
                                  null=True, blank=True, verbose_name='Talep Eden Depo')
    order_type = models.CharField('Siparis Turu', max_length=20, choices=ORDER_TYPE_CHOICES,
                                  default='standard')
    status = models.CharField('Durum', max_length=20, choices=STATUS_CHOICES, default='pending')
    date = models.DateField('Siparis Tarihi', auto_now_add=True)
    time = models.TimeField('Saat', auto_now_add=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, verbose_name='Talep Eden',
                                     related_name='requested_orders')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, verbose_name='Onaylayan',
                                    related_name='approved_orders')
    delivery_date = models.DateField('Teslim Tarihi', null=True, blank=True)
    notes = models.TextField('Notlar', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Siparis'
        verbose_name_plural = 'Siparisler'
        ordering = ['-created_at']

    def __str__(self):
        return f"SIP-{self.order_no}"

    @property
    def total_amount(self):
        total = 0
        for item in self.items.all():
            total += item.quantity * item.unit_price
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Siparis',
                              related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='Urun')
    quantity = models.DecimalField('Siparis Miktari', max_digits=12, decimal_places=2)
    delivered_quantity = models.DecimalField('Teslim Edilen', max_digits=12, decimal_places=2, default=0)
    unit_price = models.DecimalField('Birim Fiyat', max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Siparis Kalemi'
        verbose_name_plural = 'Siparis Kalemleri'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def remaining(self):
        return self.quantity - self.delivered_quantity

    @property
    def total_price(self):
        return self.quantity * self.unit_price
