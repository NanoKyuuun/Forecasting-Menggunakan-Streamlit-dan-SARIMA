@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "APP_DIR=%ROOT_DIR%sarima-streamlit-dashboard"
set "PYTHON_EXE=%APP_DIR%\.venv\Scripts\python.exe"
set "PORT=%~1"

if "%PORT%"=="" set "PORT=8501"

echo.
echo [Run] Dashboard Streamlit SARIMA
echo.

if not exist "%APP_DIR%\app.py" (
    echo [Error] Folder aplikasi tidak ditemukan: "%APP_DIR%"
    echo Pastikan run.bat dijalankan dari root repo.
    if not "%NO_PAUSE%"=="1" pause
    exit /b 1
)

if not exist "%PYTHON_EXE%" (
    echo [Error] Virtual environment belum siap.
    echo Jalankan setup.bat terlebih dahulu.
    if not "%NO_PAUSE%"=="1" pause
    exit /b 1
)

cd /d "%APP_DIR%"
echo Aplikasi akan berjalan di:
echo   http://localhost:%PORT%
echo.
echo Tekan CTRL+C untuk menghentikan server.
echo.

"%PYTHON_EXE%" -m streamlit run app.py --server.port "%PORT%" --server.headless true --browser.gatherUsageStats false

echo.
echo [Info] Server Streamlit berhenti.
if not "%NO_PAUSE%"=="1" pause
