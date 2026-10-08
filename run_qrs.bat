@echo off
SET PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python314\python.exe
IF NOT EXIST "%PYTHON_EXE%" (
    SET PYTHON_EXE=C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe
)
IF NOT EXIST "%PYTHON_EXE%" (
    SET PYTHON_EXE=python
)
"%PYTHON_EXE%" manage.py shell -c "from core.models import Trip; trips = Trip.objects.filter(status='Completed'); count=0; [t.generate_fare_qr_code() for t in trips]; [t.save(update_fields=['fare_qr_code']) for t in trips]; print(f'Successfully regenerated existing QR codes!')"
