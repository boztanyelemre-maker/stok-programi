from django.db import models
from django.conf import settings


class Assignment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('returned', 'Iade Edildi'),
        ('lost', 'Kayip'),
        ('damaged', 'Hasarli'),
    ]
    assigned_to_name = models.CharField('Ad Soyad', max_length=200)
    assigned_to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                         null=True, blank=True, verbose_name='Kullanici')
    tc_kimlik = models.CharField('TC Kimlik', max_length=11, blank=True)
    title = models.CharField('Unvan/Gorevi', max_length=200, blank=True)
    project = models.ForeignKey('parameters.Project', on_delete=models.CASCADE,
                                verbose_name='Proje')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE,
                                verbose_name='Malzeme', null=True, blank=True)
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE,
                              verbose_name='Demirbas', null=True, blank=True)
    quantity = models.DecimalField('Miktar', max_digits=12, decimal_places=2, default=1)
    assignment_date = models.DateField('Zimmet Tarihi')
    return_date = models.DateField('Iade Tarihi', null=True, blank=True)
    status = models.CharField('Durum', max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField('Aciklama', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, verbose_name='Olusturan',
                                   related_name='created_assignments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Zimmet'
        verbose_name_plural = 'Zimmetler'
        ordering = ['-assignment_date']

    def __str__(self):
        item = self.product or self.asset
        return f"{self.assigned_to_name} - {item}"
