#!/bin/bash
# ============================================================
#  NARON STOK YONETIM SISTEMI - Tav Gard Guvenlik A.S.
#  Linux / macOS Baslat Scripti
# ============================================================

set -e
cd "$(dirname "$0")"

echo "============================================================"
echo "    NARON STOK YONETIM SISTEMI - Tav Gard Guvenlik A.S."
echo "============================================================"
echo ""

# .env dosyasi varsa yukle
if [ -f ".env" ]; then
    echo "[*] .env dosyasi yukleniyor..."
    export $(grep -v '^#' .env | xargs)
fi

# Python kontrolu
echo "[1/6] Python kontrol ediliyor..."
if ! command -v python3 &> /dev/null; then
    echo "[HATA] Python3 bulunamadi! Lutfen kurun:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi
python3 --version
echo ""

# Sanal ortam
echo "[2/6] Sanal ortam kontrol ediliyor..."
if [ ! -d "venv" ]; then
    echo "   Sanal ortam olusturuluyor..."
    python3 -m venv venv
    echo "   Sanal ortam olusturuldu."
else
    echo "   Sanal ortam mevcut."
fi
echo ""

source venv/bin/activate

# Bagimliliklar
echo "[3/6] Bagimliliklar kontrol ediliyor..."
pip install -r requirements.txt -q
echo "   Bagimliliklar tamam."
echo ""

# Migration
echo "[4/6] Veritabani guncelleniyor..."
python manage.py migrate
echo ""

# Admin kullanici
echo "[5/6] Admin kullanici kontrol ediliyor..."
python -c "
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'naron.settings'
import django
django.setup()
from accounts.models import User
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'admin@tavgard.com', 'admin123')
    u.first_name = 'Admin'
    u.last_name = 'Kullanici'
    u.role = 'admin'
    u.company = 'Tav Gard Guvenlik A.S.'
    u.is_approved = True
    u.save()
    print('   Admin kullanici olusturuldu: admin / admin123')
else:
    print('   Admin kullanici mevcut.')
"
echo ""

# Sunucu
echo "[6/6] Sunucu baslatiliyor..."
echo ""
echo "============================================================"
echo "   Uygulama hazir!"
echo ""
echo "   Tarayicinizda acin: http://127.0.0.1:8000"
echo ""
echo "   Giris: admin / admin123"
echo ""
echo "   Durdurmak icin Ctrl+C basin."
echo "============================================================"
echo ""

python manage.py runserver 0.0.0.0:8000
