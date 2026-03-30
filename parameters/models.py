from django.db import models


class Project(models.Model):
    name = models.CharField('Proje Adi', max_length=300, unique=True)
    code = models.CharField('Proje Kodu', max_length=50, blank=True)
    is_active = models.BooleanField('Aktif', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Proje'
        verbose_name_plural = 'Projeler'
        ordering = ['name']

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Proje',
                                related_name='warehouses')
    name = models.CharField('Depo/Bina Adi', max_length=200)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Depo/Bina'
        verbose_name_plural = 'Depolar/Binalar'
        ordering = ['name']

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class Location(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='Depo/Bina',
                                  related_name='locations')
    name = models.CharField('Lokasyon (Kat)', max_length=200)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Lokasyon'
        verbose_name_plural = 'Lokasyonlar'
        ordering = ['name']

    def __str__(self):
        return f"{self.warehouse.name} - {self.name}"


class Room(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Lokasyon',
                                 related_name='rooms')
    name = models.CharField('Oda/Alan', max_length=200)
    is_active = models.BooleanField('Aktif', default=True)

    class Meta:
        verbose_name = 'Oda/Alan'
        verbose_name_plural = 'Odalar/Alanlar'
        ordering = ['name']

    def __str__(self):
        return f"{self.location.name} - {self.name}"


class GeneralSettings(models.Model):
    stock_entry_counter = models.IntegerField('Stok Giris Fisi Sayaci', default=1)
    stock_exit_counter = models.IntegerField('Stok Cikis Fisi Sayaci', default=1)
    delivery_counter = models.IntegerField('Teslim Fisi Sayaci', default=1)
    transfer_counter = models.IntegerField('Transfer Fisi Sayaci', default=1)
    count_counter = models.IntegerField('Stok Sayim Fisi Sayaci', default=1)

    class Meta:
        verbose_name = 'Genel Ayar'
        verbose_name_plural = 'Genel Ayarlar'

    def __str__(self):
        return 'Genel Ayarlar'

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
