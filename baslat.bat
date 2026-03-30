@echo off
chcp 65001 >nul 2>&1
title Naron Stok Yonetim Sistemi
color 1F

echo ============================================================
echo     NARON STOK YONETIM SISTEMI - Tav Gard Guvenlik A.S.
echo ============================================================
echo.

:: Klasor yolunu belirle
cd /d "%~dp0"

:: .env dosyasi varsa yukle
if exist ".env" (
    echo [*] .env dosyasi yukleniyor...
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        set "%%a=%%b"
    )
)

:: Python kontrolu
echo [1/6] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [HATA] Python bulunamadi!
    echo.
    echo Python'u https://www.python.org/downloads/ adresinden indirip kurun.
    echo Kurulum sirasinda "Add Python to PATH" secenegini isaretleyin.
    echo.
    pause
    exit /b 1
)
python --version
echo.

:: Sanal ortam kontrolu ve olusturma
echo [2/6] Sanal ortam kontrol ediliyor...
if not exist "venv" (
    echo    Sanal ortam olusturuluyor...
    python -m venv venv
    if errorlevel 1 (
        echo [HATA] Sanal ortam olusturulamadi!
        pause
        exit /b 1
    )
    echo    Sanal ortam olusturuldu.
) else (
    echo    Sanal ortam mevcut.
)
echo.

:: Sanal ortami aktif et
call venv\Scripts\activate.bat

:: Bagimliliklari kur
echo [3/6] Bagimliliklar kontrol ediliyor...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [HATA] Bagimliliklar kurulamadi!
    pause
    exit /b 1
)
echo    Bagimliliklar tamam.
echo.

:: Migration
echo [4/6] Veritabani guncelleniyor...
python manage.py migrate --run-syncdb >nul 2>&1
python manage.py migrate
echo.

:: Admin kullanici kontrolu
echo [5/6] Admin kullanici kontrol ediliyor...
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
    print('   Admin kullanici olusturuldu.')
    print('   Kullanici Adi : admin')
    print('   Sifre         : admin123')
else:
    print('   Admin kullanici mevcut.')
"
echo.

:: Sunucuyu baslat
echo [6/6] Sunucu baslatiliyor...
echo.
echo ============================================================
echo    Uygulama hazir!
echo.
echo    Tarayicinizda asagidaki adresi acin:
echo    http://127.0.0.1:8000
echo.
echo    Giris Bilgileri:
echo      Kullanici Adi : admin
echo      Sifre         : admin123
echo.
echo    Durdurmak icin bu pencerede Ctrl+C basin.
echo ============================================================
echo.

:: Tarayiciyi otomatik ac
start http://127.0.0.1:8000

:: Sunucuyu baslat
python manage.py runserver 0.0.0.0:8000
