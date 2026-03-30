@echo off
chcp 65001 >nul
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  echo [HATA] "python" komutu bulunamadi.
  echo Python indirin: https://www.python.org/downloads/
  echo Kurulumda "Add python.exe to PATH" secenegini isaretleyin.
  pause
  exit /b 1
)

echo Sanal ortam olusturuluyor...
python -m venv venv
if errorlevel 1 (
  echo [HATA] venv olusturulamadi.
  pause
  exit /b 1
)

echo Bagimliliklar yukleniyor...
"venv\Scripts\python.exe" -m pip install --upgrade pip
"venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo [HATA] pip install basarisiz.
  pause
  exit /b 1
)

echo.
echo Tamam. Sunucu icin runserver-8080.bat dosyasini calistirin.
pause
