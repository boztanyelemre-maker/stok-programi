from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Yonetici'),
        ('manager', 'Mudur'),
        ('staff', 'Personel'),
        ('warehouse', 'Depocu'),
    ]
    role = models.CharField('Rol', max_length=20, choices=ROLE_CHOICES, default='staff')
    tc_kimlik = models.CharField('TC Kimlik No', max_length=11, blank=True)
    phone = models.CharField('Cep Telefonu', max_length=20, blank=True)
    work_phone = models.CharField('Is Telefonu', max_length=20, blank=True)
    company = models.CharField('Firma Adi', max_length=200, blank=True)
    authorized_name = models.CharField('Yetkili Adi', max_length=100, blank=True)
    authorized_surname = models.CharField('Yetkili Soyadi', max_length=100, blank=True)
    country = models.CharField('Ulke', max_length=100, default='Turkiye')
    city = models.CharField('Il', max_length=100, blank=True)
    district = models.CharField('Ilce', max_length=100, blank=True)
    title = models.CharField('Unvan/Gorevi', max_length=100, blank=True)
    is_approved = models.BooleanField('Onaylandi', default=False)
    projects = models.ManyToManyField('parameters.Project', blank=True, verbose_name='Atanan Projeler')
    created_at = models.DateTimeField('Olusturulma Tarihi', auto_now_add=True)
    updated_at = models.DateTimeField('Guncellenme Tarihi', auto_now=True)

    class Meta:
        verbose_name = 'Kullanici'
        verbose_name_plural = 'Kullanicilar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username
