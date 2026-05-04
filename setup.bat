@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "APP_DIR=%ROOT_DIR%sarima-streamlit-dashboard"
set "VENV_DIR=%APP_DIR%\.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

echo.
echo [Setup] Dashboard Streamlit SARIMA
echo.

if not exist "%APP_DIR%\app.py" (
    echo [Error] Folder aplikasi tidak ditemukan: "%APP_DIR%"
    echo Pastikan setup.bat dijalankan dari root repo.
    if not "%NO_PAUSE%"=="1" pause
    exit /b 1
)

if not exist "%PYTHON_EXE%" (
    echo [Setup] Virtual environment belum ada. Membuat .venv...
    where py >nul 2>nul
    if "%ERRORLEVEL%"=="0" (
        py -3 -m venv "%VENV_DIR%"
    ) else (
        where python >nul 2>nul
        if not "%ERRORLEVEL%"=="0" (
            echo [Error] Python tidak ditemukan. Install Python 3.11+ lalu jalankan setup.bat lagi.
            if not "%NO_PAUSE%"=="1" pause
            exit /b 1
        )
        python -m venv "%VENV_DIR%"
    )

    if not exist "%PYTHON_EXE%" (
        echo [Error] Gagal membuat virtual environment.
        if not "%NO_PAUSE%"=="1" pause
        exit /b 1
    )
)

echo [Setup] Install dependency dari requirements.txt...
"%PYTHON_EXE%" -m pip install --disable-pip-version-check -r "%APP_DIR%\requirements.txt"
if not "%ERRORLEVEL%"=="0" (
    echo [Error] Gagal install dependency.
    if not "%NO_PAUSE%"=="1" pause
    exit /b 1
)

echo.
echo [OK] Setup selesai.
echo Jalankan aplikasi dengan:
echo   run.bat
echo atau port custom:
echo   run.bat 8511
echo.
if not "%NO_PAUSE%"=="1" pause
