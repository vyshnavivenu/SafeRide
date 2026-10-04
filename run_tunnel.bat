@echo off
TITLE SafeRide - Public Mobile WhatsApp Tunnel
echo =====================================================================
echo   SAFERIDE: PUBLIC HTTPS MOBILE TUNNEL FOR WHATSAPP
echo   Provides clickable public URL that opens on any phone anywhere!
echo =====================================================================
echo.

SET PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python314\python.exe
IF NOT EXIST "%PYTHON_EXE%" (
    SET PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe
)
IF NOT EXIST "%PYTHON_EXE%" (
    SET PYTHON_EXE=python
)

"%PYTHON_EXE%" tunnel_launcher.py
pause
