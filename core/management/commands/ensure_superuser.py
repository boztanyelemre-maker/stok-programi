"""
Render ucretsiz planda Shell kapali oldugunda superuser olusturmak icin.

Render Dashboard -> Web Service -> Environment:
  BOOTSTRAP_SUPERUSER_USERNAME = admin
  BOOTSTRAP_SUPERUSER_PASSWORD = guclu_sifre
  BOOTSTRAP_SUPERUSER_EMAIL = sizin@email.com   (istege bagli)

Deploy sonrasi guvenlik icin bu uc degiskeni silin veya sifreyi degistirin.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'BOOTSTRAP_SUPERUSER_* ortam degiskenleriyle superuser olusturur (yoksa hicbir sey yapmaz).'

    def handle(self, *args, **options):
        username = (os.environ.get('BOOTSTRAP_SUPERUSER_USERNAME') or '').strip()
        password = os.environ.get('BOOTSTRAP_SUPERUSER_PASSWORD')
        email = (os.environ.get('BOOTSTRAP_SUPERUSER_EMAIL') or 'admin@example.com').strip()

        if not username or not password:
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Bootstrap atlandi: {username} zaten var.')
            return

        user = User.objects.create_superuser(username=username, email=email, password=password)
        user.role = 'admin'
        user.is_approved = True
        user.save(update_fields=['role', 'is_approved'])
        self.stdout.write(self.style.SUCCESS(f'Superuser olusturuldu: {username}'))
