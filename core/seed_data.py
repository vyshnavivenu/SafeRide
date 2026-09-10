import os
import sys
from pathlib import Path

# Add project root directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
import django
django.setup()

from django.utils import timezone
from core.models import (
    User, Admin, Passenger, Driver, VehicleDocuments, Trip, RatingReview, Complaint, SOSAlert, IncidentReport
)

def run_seed():
    print("[*] Starting SafeRide Demo Database Seeding into tbl_ tables...")

    # 1. Create Superuser Administrator (tbl_user & tbl_admin)
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'SafeRide',
            'last_name': 'Administrator',
            'email': 'admin@saferide.org',
            'role': User.Role.ADMIN,
            'is_staff': True,
            'is_superuser': True,
        }
    )
    admin_user.set_password('admin123')
    admin_user.save()

    admin_record, _ = Admin.objects.update_or_create(
        user=admin_user,
        defaults={
            'name': 'SafeRide Administrator',
            'email': 'admin@saferide.org',
            'password': admin_user.password,
        }
    )
    print("[+] Created Administrator in tbl_admin: username='admin', password='admin123'")

    # 2. Create Passenger Users (tbl_user & tbl_passenger)
    p1_user, _ = User.objects.get_or_create(
        username='vyshnavi',
        defaults={
            'first_name': 'Vyshnavi',
            'last_name': 'Venu',
            'email': 'vyshnavi@sjcetpalai.ac.in',
            'phone': '+91 9847123456',
            'role': User.Role.PASSENGER,
        }
    )
    p1_user.set_password('passenger123')
    p1_user.save()

    p1_record, _ = Passenger.objects.update_or_create(
        user=p1_user,
        defaults={
            'name': 'Vyshnavi Venu',
            'email': 'vyshnavi@sjcetpalai.ac.in',
            'phone_number': '+91 9847123456',
            'password': p1_user.password,
            'emergency_contact_name': 'Venu C Nair',
            'emergency_contact_phone': '+91 9447012345',
            'emergency_contact_relation': 'Parent',
            'address': 'Palai, Kottayam, Kerala',
        }
    )
    print("[+] Created Passenger in tbl_passenger: username='vyshnavi', password='passenger123'")

    p2_user, _ = User.objects.get_or_create(
        username='rahul',
        defaults={
            'first_name': 'Rahul',
            'last_name': 'Kurian',
            'email': 'rahul.k@gmail.com',
            'phone': '+91 9895001122',
            'role': User.Role.PASSENGER,
        }
    )
    p2_user.set_password('passenger123')
    p2_user.save()

    p2_record, _ = Passenger.objects.update_or_create(
        user=p2_user,
        defaults={
            'name': 'Rahul Kurian',
            'email': 'rahul.k@gmail.com',
            'phone_number': '+91 9895001122',
            'password': p2_user.password,
            'emergency_contact_name': 'Anita Kurian',
            'emergency_contact_phone': '+91 9895009988',
            'emergency_contact_relation': 'Sister',
            'address': 'Kottayam Road, Palai',
        }
    )
    print("[+] Created Passenger in tbl_passenger: username='rahul', password='passenger123'")

    # Clean up any extraneous or test records so strictly only vyshnavi and rahul exist in tbl_passenger
    official_passenger_usernames = ['vyshnavi', 'rahul']
    extra_passengers = Passenger.objects.exclude(user__username__in=official_passenger_usernames)
    if extra_passengers.exists():
        for ep in extra_passengers:
            u = ep.user
            print(f"[-] Removing non-passenger / test record from tbl_passenger: '{ep.name}' ({ep.email})")
            ep.delete()
            if u and not u.is_superuser and u.role == User.Role.PASSENGER:
                u.delete()

    drivers_data = [
        {
            'username': 'driver_rajesh',
            'password': 'driver123',
            'name': 'Rajesh Kumar',
            'first_name': 'Rajesh',
            'last_name': 'Kumar',
            'phone': '+91 9447182930',
            'license_no': 'KL-05-20180004521',
            'experience': 7,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-05-AT-4455',
            'v_type': 'auto',
            'rep_score': 96.5,
            'trips': 642,
            'avg_rating': 4.9,
        },
        {
            'username': 'driver_anand',
            'password': 'driver123',
            'name': 'Anand Joseph',
            'first_name': 'Anand',
            'last_name': 'Joseph',
            'phone': '+91 9847334455',
            'license_no': 'KL-05-20150009812',
            'experience': 9,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-05-TX-1024',
            'v_type': 'taxi',
            'rep_score': 94.0,
            'trips': 418,
            'avg_rating': 4.8,
        },
        {
            'username': 'driver_suresh',
            'password': 'driver123',
            'name': 'Suresh Babu',
            'first_name': 'Suresh',
            'last_name': 'Babu',
            'phone': '+91 9745112233',
            'license_no': 'KL-05-20200003411',
            'experience': 4,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-05-CB-8890',
            'v_type': 'cab',
            'rep_score': 89.5,
            'trips': 215,
            'avg_rating': 4.6,
        },
        {
            'username': 'driver_vinod',
            'password': 'driver123',
            'name': 'Vinod Mohan',
            'first_name': 'Vinod',
            'last_name': 'Mohan',
            'phone': '+91 9400223344',
            'license_no': 'KL-05-20240001290',
            'experience': 1,
            'status': Driver.VerificationStatus.PENDING,
            'reg_no': 'KL-05-AT-9911',
            'v_type': 'auto',
            'rep_score': 75.0,
            'trips': 12,
            'avg_rating': 4.2,
        },
        {
            'username': 'driver_varun',
            'password': 'driver123',
            'name': 'Varun Menon',
            'first_name': 'Varun',
            'last_name': 'Menon',
            'phone': '+91 9847223344',
            'license_no': 'KL-05-20210008899',
            'experience': 5,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-05-CB-4422',
            'v_type': 'cab',
            'rep_score': 93.0,
            'trips': 310,
            'avg_rating': 4.85,
        }
    ]

    # Clean up any extraneous driver accounts
    seeded_usernames = [d['username'] for d in drivers_data]
    extra_drivers = User.objects.filter(role=User.Role.DRIVER).exclude(username__in=seeded_usernames)
    if extra_drivers.exists():
        cleaned_count = extra_drivers.count()
        extra_drivers.delete()
        print(f"[-] Removed {cleaned_count} extraneous driver account(s).")

    driver_objs = []
    for d in drivers_data:
        d_user, _ = User.objects.get_or_create(
            username=d['username'],
            defaults={
                'first_name': d['first_name'],
                'last_name': d['last_name'],
                'phone': d['phone'],
                'email': f"{d['username']}@saferide.org",
                'role': User.Role.DRIVER,
            }
        )
        d_user.set_password(d['password'])
        d_user.save()

        d_prof, _ = Driver.objects.update_or_create(
            user=d_user,
            defaults={
                'name': d['name'],
                'phone_number': d['phone'],
                'email': f"{d['username']}@saferide.org",
                'license_number': d['license_no'],
                'vehicle_number': d['reg_no'],
                'vehicle_type': d['v_type'],
                'password': d_user.password,
                'experience_years': d['experience'],
                'verification_status': d['status'],
                'reputation_score': d['rep_score'],
                'total_trips': d['trips'],
                'average_rating': d['avg_rating'],
                'verified_at': timezone.now() if d['status'] == Driver.VerificationStatus.VERIFIED else None,
                'verification_notes': 'Document verification completed and police clearance verified.' if d['status'] == Driver.VerificationStatus.VERIFIED else 'Awaiting physical RC verification',
            }
        )

        VehicleDocuments.objects.update_or_create(
            driver=d_prof,
            defaults={
                'license_doc': f"/media/driver_docs/license/lic_{d['license_no']}.pdf",
                'rc_doc': f"/media/vehicle_docs/rc/rc_{d['reg_no']}.pdf",
            }
        )

        if d_prof.is_verified():
            d_prof.generate_qr_code("http://127.0.0.1:8000")
            d_prof.save()

        driver_objs.append(d_prof)
        print(f"[+] Created Driver in tbl_driver: username='{d['username']}', Vehicle='{d['reg_no']}' ({d['status']})")

    # 4. Create Sample Completed Trips & Ratings (tbl_trip & tbl_rating_review)
    rajesh_driver = driver_objs[0]
    anand_driver = driver_objs[1]

    trip1, _ = Trip.objects.get_or_create(
        passenger=p1_user,
        driver=rajesh_driver,
        pickup_location_name='SJCET Campus Main Gate, Palai',
        defaults={
            'start_location': 'SJCET Campus Main Gate, Palai',
            'end_location': 'Palai Private Bus Stand',
            'status': 'Completed',
            'start_time': timezone.now() - timezone.timedelta(days=1, hours=2),
            'end_time': timezone.now() - timezone.timedelta(days=1, hours=1, minutes=45),
            'pickup_latitude': 9.6843,
            'pickup_longitude': 76.6853,
            'live_latitude': 9.7121,
            'live_longitude': 76.6888,
        }
    )

    RatingReview.objects.get_or_create(
        trip=trip1,
        defaults={
            'driver': rajesh_driver,
            'passenger': p1_user,
            'rating': 5,
            'review': 'Very polite driver, drove safely at regulated speeds, and followed the direct meter fare! Highly recommend.',
        }
    )
    print("[+] Created Completed Trip & Rating in tbl_trip & tbl_rating_review")

    trip2, _ = Trip.objects.get_or_create(
        passenger=p2_user,
        driver=anand_driver,
        pickup_location_name='Lalam Temple Junction, Palai',
        defaults={
            'start_location': 'Lalam Temple Junction, Palai',
            'end_location': 'Kottayam Railway Station',
            'status': 'Completed',
            'start_time': timezone.now() - timezone.timedelta(days=2),
            'end_time': timezone.now() - timezone.timedelta(days=2, hours=-1),
            'pickup_latitude': 9.7082,
            'pickup_longitude': 76.6835,
            'live_latitude': 9.5916,
            'live_longitude': 76.5222,
        }
    )

    RatingReview.objects.get_or_create(
        trip=trip2,
        defaults={
            'driver': anand_driver,
            'passenger': p2_user,
            'rating': 5,
            'review': 'Clean cab and smooth driving. Helped with luggage and took the safest route.',
        }
    )

    # 4b. Backfill any trips missing destination points with realistic Palai locations
    dest_defaults = [
        ("Pala KSRTC Bus Station", 9.691200, 76.690400),
        ("St. Thomas Cathedral, Palai", 9.709000, 76.682000),
        ("Lalam Bridge Junction, Palai", 9.708200, 76.683500),
        ("Palai Town Civil Station", 9.710000, 76.680000),
    ]
    unspecified_trips = Trip.objects.filter(destination_address__isnull=True) | Trip.objects.filter(
        destination_address__in=['', 'Destination Point', 'Destination Drop Point']
    )
    for idx, t in enumerate(unspecified_trips):
        d_name, d_lat, d_lng = dest_defaults[idx % len(dest_defaults)]
        t.destination_address = d_name
        t.end_location = d_name
        t.drop_location_name = d_name
        t.destination_latitude = d_lat
        t.destination_longitude = d_lng
        t.drop_latitude = d_lat
        t.drop_longitude = d_lng
        t.save()
    print("[+] Verified and populated Destination Points for all completed trips")

    # 5. Create Active SOS Alert (tbl_sos_alert)
    if not SOSAlert.objects.filter(passenger=p1_user, driver=rajesh_driver, status='Active').exists():
        SOSAlert.objects.create(
            passenger=p1_user,
            driver=rajesh_driver,
            status='Active',
            location='Near SJCET Campus, Palai Bypass Road',
            latitude=9.6843,
            longitude=76.6853,
            location_name='Near SJCET Campus, Palai Bypass Road',
            admin_notes='Distress beacon received. Emergency response team alerted.',
            dispatched_services='Local Police Station (112), Campus Safety Hotline',
        )
    print("[+] Created SOS Alert in tbl_sos_alert")

    print("\n[SUCCESS] SafeRide Database Tables (tbl_*) seeded successfully!")

if __name__ == '__main__':
    run_seed()
