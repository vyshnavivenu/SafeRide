@echo off
TITLE SafeRide - Driver Verification (Quick Run with SQLite)
echo =====================================================================
echo   SAFERIDE: DRIVER VERIFICATION AND PASSENGER SAFETY SYSTEM
echo   Running in Quick Mode (Local SQLite Database)
echo =====================================================================
echo.

SET PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python314\python.exe
IF NOT EXIST "%PYTHON_EXE%" (
    SET PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe
)
IF NOT EXIST "%PYTHON_EXE%" (
    SET PYTHON_EXE=python
)

SET USE_SQLITE=True

echo [*] Applying database migrations (SQLite)...
"%PYTHON_EXE%" manage.py makemigrations core
"%PYTHON_EXE%" manage.py migrate

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Migration failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [*] Seeding demo accounts, verified drivers, QR codes, and test rides...
"%PYTHON_EXE%" core/seed_data.py

echo.
echo =====================================================================
echo   DEMO TEST ACCOUNTS:
echo   1. Administrator:   username: admin           password: admin123
echo   2. Passenger:       username: vyshnavi        password: passenger123
echo   3. Auto Driver:     username: driver_rajesh   password: driver123
echo      Vehicle:         KL-05-AT-4455 (Bajaj RE Compact)
echo =====================================================================
echo.
echo [*] Starting SafeRide Server at http://127.0.0.1:8000 ...
echo.

"%PYTHON_EXE%" manage.py runserver 0.0.0.0:8000
pause
