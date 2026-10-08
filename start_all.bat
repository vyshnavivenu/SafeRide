@echo off
TITLE SafeRide - Start Everything
echo =====================================================================
echo   STARTING SAFERIDE SERVER AND TUNNEL
echo =====================================================================
echo.
echo [!] Make sure XAMPP MySQL is running!
echo.
echo Starting Django Server in a new window...
start "SafeRide Django Server" cmd /k ".\run_server.bat"

echo Starting Public Tunnel in a new window...
start "SafeRide Public Tunnel" cmd /k "python tunnel_launcher.py 3"

echo.
echo Both processes have been launched in separate windows!
echo You can close this window now.
pause
