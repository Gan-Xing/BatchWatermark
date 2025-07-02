@echo off
chcp 65001 >nul
echo ====================================
echo BatchWatermark Windows Build Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not detected, please install Python first
    pause
    exit /b 1
)

REM Clean old files
echo [1/3] Cleaning old files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo Cleanup complete!
echo.

REM Install dependencies
echo [2/3] Checking and installing dependencies...
pip install -r requirements.txt
echo.

REM Start packaging
echo [3/3] Starting packaging...
pyinstaller --clean --onefile --windowed --icon=assets/app_icon.ico --name="BatchWatermark" batch_watermark.py

if errorlevel 1 (
    echo.
    echo [ERROR] Packaging failed!
    pause
    exit /b 1
)

echo.
echo ====================================
echo Packaging successful!
echo File location: dist\BatchWatermark.exe
echo ====================================
echo.
pause