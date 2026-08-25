@echo off
TITLE SafeRide - Driver Verification (MySQL / phpMyAdmin)
echo =====================================================================
echo   SAFERIDE: DRIVER VERIFICATION AND PASSENGER SAFETY SYSTEM
echo   Department of Computer Applications - Mini Project (24SJMCA245)
echo   St. Joseph's College of Engineering and Technology, Palai
echo   Database: MySQL (phpMyAdmin)
echo =====================================================================
echo.

SET PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe
IF NOT EXIST "%PYTHON_EXE%" (
    SET PYTHON_EXE=python
)

echo [*] Target Database: MySQL (saferide_db on 127.0.0.1:3306)
echo [!] Make sure XAMPP (Apache and MySQL) is STARTED before proceeding!
echo.

echo [*] Applying MySQL database migrations...
"%PYTHON_EXE%" manage.py makemigrations core
"%PYTHON_EXE%" manage.py migrate

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo =====================================================================
    echo [ERROR] Could not connect to MySQL database 'saferide_db'.
    echo Please make sure:
    echo  1. XAMPP Control Panel is open and MySQL is started (green).
    echo  2. Open http://localhost/phpmyadmin in your browser.
    echo  3. Click 'New', enter database name 'saferide_db', and click 'Create'.
    echo =====================================================================
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [*] Seeding demo accounts, verified drivers, QR codes, and test rides...
"%PYTHON_EXE%" core/seed_data.py

echo.
echo =====================================================================
echo   DEMO TEST ACCOUNTS IN MYSQL:
echo   1. Administrator:   username: admin           password: admin123
echo   2. Passenger:       username: vyshnavi        password: passenger123
echo   3. Auto Driver:     username: driver_rajesh   password: driver123
echo      Vehicle:         KL-05-AT-4455 (Bajaj RE Compact)
echo =====================================================================
echo.
echo [*] Starting SafeRide Server at http://127.0.0.1:8000 ...
echo [!] View all MySQL tables in phpMyAdmin at http://localhost/phpmyadmin
echo.

"%PYTHON_EXE%" manage.py runserver 0.0.0.0:8000
pause
