import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
django.setup()

from core.models import User, Admin, Passenger, Driver, Trip, SOSAlert, Complaint, RatingReview, VehicleDocuments

def analyze_all():
    print("================================================================================")
    print("                SAFERIDE: DETAILED DATABASE AUDIT & DATA ANALYSIS               ")
    print("================================================================================\n")

    print("--- 1. USERS & CREDENTIALS (tbl_user) ---")
    users = User.objects.all().order_by('id')
    print(f"Total Users: {users.count()}")
    for u in users:
        u_name = u.get_full_name() or u.username
        u_phone = u.phone or 'N/A'
        print(f" • [ID {u.id:2d}] {u.username:16} | Role: {str(u.role):10} | Name: {u_name:20} | Phone: {u_phone:15} | Email: {u.email}")

    print("\n--- 2. ADMIN PROFILE (tbl_admin) ---")
    admins = Admin.objects.all()
    for a in admins:
        print(f" • [Admin ID {a.admin_id}] User: {a.user.username if a.user else 'N/A'} | Name: {a.name} | Email: {a.email}")

    print("\n--- 3. PASSENGERS & EMERGENCY CONTACTS (tbl_passenger) ---")
    passengers = Passenger.objects.all().order_by('passenger_id')
    print(f"Total Passengers: {passengers.count()}")
    for p in passengers:
        print(f" * [Passenger ID {p.passenger_id}] {p.name} ({p.user.username}) | Phone: {p.phone_number} | Address: {p.address}")
        print(f"    |-- Contact 1: {p.emergency_contact_1_name} ({p.emergency_contact_1_phone} - {p.emergency_contact_1_relation})")
        print(f"    |-- Contact 2: {p.emergency_contact_2_name} ({p.emergency_contact_2_phone} - {p.emergency_contact_2_relation})")
        print(f"    +-- Contact 3: {p.emergency_contact_3_name} ({p.emergency_contact_3_phone} - {p.emergency_contact_3_relation})")

    print("\n--- 4. DRIVERS, VEHICLES & VERIFICATION STATUS (tbl_driver) ---")
    drivers = Driver.objects.all().order_by('driver_id')
    print(f"Total Drivers: {drivers.count()}")
    for d in drivers:
        qr_status = d.qr_code_image.name if d.qr_code_image else "No QR (Pending)"
        print(f" * [Driver ID {d.driver_id:2d}] {d.name:18} | Plate: {d.vehicle_number:14} | Type: {d.get_vehicle_type_display():12} | Lic: {d.license_number:17} | Status: {d.verification_status:9} | Rep: {d.reputation_score:5.1f}/100 | Stars: {d.average_rating:3.1f}/5.0 | Trips: {d.total_trips:3d} | QR: {qr_status}")

    print("\n--- 5. VEHICLE DOCUMENTS & KYC (tbl_vehicle_documents) ---")
    docs = VehicleDocuments.objects.all().order_by('document_id')
    print(f"Total Vehicle Documents: {docs.count()}")
    for doc in docs:
        print(f" * [Doc ID {doc.document_id:2d}] Driver: {doc.driver.name} (ID: {doc.driver_id}) | License Doc: {doc.license_doc} | RC Doc: {doc.rc_doc}")

    print("\n--- 6. TRIP RECORDS & BOARDING TELEMETRY (tbl_trip) ---")
    trips = Trip.objects.all().order_by('trip_id')
    print(f"Total Trips: {trips.count()}")
    for t in trips:
        p_name = t.passenger.get_full_name() or t.passenger.username if t.passenger else "N/A"
        d_name = t.driver.name if t.driver else "N/A"
        print(f" * [Trip ID {t.trip_id}] Passenger: {p_name:18} | Driver: {d_name:18} | Status: {t.status:10}")
        print(f"    |-- Pickup : {t.boarding_address} ({t.boarding_latitude}, {t.boarding_longitude})")
        print(f"    +-- Dropoff: {t.destination_address or 'In Transit'} ({t.destination_latitude}, {t.destination_longitude})")

    print("\n--- 7. SOS DISTRESS ALERTS & DISPATCH (tbl_sos_alert) ---")
    alerts = SOSAlert.objects.all().order_by('sos_id')
    print(f"Total SOS Alerts: {alerts.count()}")
    for s in alerts:
        p_name = s.passenger.get_full_name() or s.passenger.username if s.passenger else "N/A"
        d_name = s.driver.name if s.driver else "N/A"
        print(f" * [Alert ID {s.sos_id}] Passenger: {p_name} | Driver: {d_name} | Status: {s.status} | Time: {s.timestamp}")
        print(f"    +-- Telemetry: {s.location} (Lat: {s.latitude}, Lng: {s.longitude})")

    print("\n--- 8. COMPLAINTS & GRIEVANCES (tbl_complaint) ---")
    complaints = Complaint.objects.all().order_by('complaint_id')
    print(f"Total Complaints: {complaints.count()}")
    for c in complaints:
        p_name = c.passenger.get_full_name() or c.passenger.username if c.passenger else "N/A"
        d_name = c.driver.name if c.driver else "N/A"
        print(f" * [Complaint ID {c.complaint_id}] Passenger: {p_name} -> Driver: {d_name} | Category: '{c.category}' | Status: {c.status} | Penalty: -{c.penalty_points_deducted} pts")
        print(f"    +-- Description: \"{c.description}\"")

    print("\n--- 9. RATINGS & REVIEWS (tbl_rating_review) ---")
    reviews = RatingReview.objects.all().order_by('rating_id')
    print(f"Total Rating Reviews: {reviews.count()}")
    for r in reviews:
        p_name = r.passenger.get_full_name() or r.passenger.username if r.passenger else "N/A"
        d_name = r.driver.name if r.driver else "N/A"
        print(f" * [Rating ID {r.rating_id}] {p_name} on {d_name}: {r.rating}/5.0 stars | Review: \"{r.review}\" | Safety: {r.driving_safety_rating}/5 | Cleanliness: {r.vehicle_cleanliness_rating}/5 | Behavior: {r.behavior_rating}/5 | Fare Honesty: {r.fare_honesty_rating}/5")

if __name__ == '__main__':
    analyze_all()
