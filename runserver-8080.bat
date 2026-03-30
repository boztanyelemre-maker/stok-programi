@echo off
cd /d "%~dp0"

if exist "venv\Scripts\python.exe" (
  "venv\Scripts\python.exe" manage.py runserver 8080
  goto :eof
)

python manage.py runserver 8080
if errorlevel 1 (
  echo.
  echo Sunucu baslamadi. Deneyin:
  echo   1. setup-venv.bat calistirin ^(bir kez^)
  echo   2. Python yoksa: https://www.python.org/downloads/ ^- kurulumda PATH ekleyin
  echo   PowerShell icin venv: python -m venv venv
  echo   Sonra: .\venv\Scripts\python.exe -m pip install -r requirements.txt
  echo.
  pause
)
