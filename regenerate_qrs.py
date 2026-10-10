import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
django.setup()

from core.models import Trip, Driver

trips = Trip.objects.filter(status='Completed')
trip_count = 0
for t in trips:
    if t.fare_qr_code:
        t.generate_fare_qr_code()
        t.save(update_fields=['fare_qr_code'])
        trip_count += 1

print(f"Successfully regenerated {trip_count} existing Trip Fare QR codes!")

drivers = Driver.objects.all()
driver_count = 0
for d in drivers:
    if d.is_verified():
        d.generate_qr_code()
        d.save(update_fields=['qr_code', 'qr_code_image'])
        driver_count += 1

print(f"Successfully regenerated {driver_count} existing Driver Verification QR codes!")

