import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
django.setup()

from core.models import Trip

trips = Trip.objects.filter(status='Completed')
count = 0
for t in trips:
    if t.fare_qr_code:
        t.generate_fare_qr_code()
        t.save(update_fields=['fare_qr_code'])
        count += 1

print(f"Successfully regenerated {count} existing QR codes!")
