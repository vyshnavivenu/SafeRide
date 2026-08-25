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
            'emergency_contact_1_name': 'Venu Chandrasekharan Nair (Father)',
            'emergency_contact_1_phone': '+91 9447012345',
            'emergency_contact_1_relation': 'Parent',
            'emergency_contact_2_name': 'SJCET Security / Helpdesk',
            'emergency_contact_2_phone': '+91 4822239700',
            'emergency_contact_2_relation': 'Campus Security',
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
            'emergency_contact_1_name': 'Anita Kurian',
            'emergency_contact_1_phone': '+91 9895009988',
            'emergency_contact_1_relation': 'Sister',
            'address': 'Kottayam Road, Palai',
        }
    )

    # 3. Create Drivers & Vehicle Documents (tbl_driver & tbl_vehicle_documents)
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
            'username': 'driver_pradeep',
            'password': 'driver123',
            'name': 'Pradeep Chandran',
            'first_name': 'Pradeep',
            'last_name': 'Chandran',
            'phone': '+91 9447665544',
            'license_no': 'KL-05-20170008821',
            'experience': 8,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-05-AT-7788',
            'v_type': 'auto',
            'rep_score': 95.0,
            'trips': 520,
            'avg_rating': 4.85,
        },
        {
            'username': 'driver_mathew',
            'password': 'driver123',
            'name': 'Mathew Varghese',
            'first_name': 'Mathew',
            'last_name': 'Varghese',
            'phone': '+91 9847119988',
            'license_no': 'KL-35-20160007743',
            'experience': 10,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-35-TX-4521',
            'v_type': 'taxi',
            'rep_score': 98.5,
            'trips': 780,
            'avg_rating': 4.95,
        },
        {
            'username': 'driver_hari',
            'password': 'driver123',
            'name': 'Harikrishnan Nair',
            'first_name': 'Harikrishnan',
            'last_name': 'Nair',
            'phone': '+91 9745887766',
            'license_no': 'KL-05-20190005512',
            'experience': 5,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-05-CB-3344',
            'v_type': 'cab',
            'rep_score': 91.0,
            'trips': 340,
            'avg_rating': 4.75,
        },
        {
            'username': 'driver_shaji',
            'password': 'driver123',
            'name': 'Shaji Thomas',
            'first_name': 'Shaji',
            'last_name': 'Thomas',
            'phone': '+91 9495223311',
            'license_no': 'KL-05-20210006678',
            'experience': 3,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-05-EV-1205',
            'v_type': 'cab',
            'rep_score': 93.5,
            'trips': 195,
            'avg_rating': 4.90,
        },
        {
            'username': 'driver_anoop',
            'password': 'driver123',
            'name': 'Anoop Rajan',
            'first_name': 'Anoop',
            'last_name': 'Rajan',
            'phone': '+91 9605443322',
            'license_no': 'KL-35-20230009988',
            'experience': 2,
            'status': Driver.VerificationStatus.PENDING,
            'reg_no': 'KL-35-AT-6622',
            'v_type': 'auto',
            'rep_score': 78.0,
            'trips': 45,
            'avg_rating': 4.40,
        },
        {
            'username': 'driver_deepak',
            'password': 'driver123',
            'name': 'Deepak K. S.',
            'first_name': 'Deepak',
            'last_name': 'K. S.',
            'phone': '+91 9946115500',
            'license_no': 'KL-07-20140003321',
            'experience': 11,
            'status': Driver.VerificationStatus.VERIFIED,
            'reg_no': 'KL-07-CB-9080',
            'v_type': 'cab',
            'rep_score': 97.0,
            'trips': 910,
            'avg_rating': 4.92,
        }
    ]

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
            'driving_safety_rating': 5,
            'vehicle_cleanliness_rating': 5,
            'behavior_rating': 5,
            'fare_honesty_rating': 5,
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
            'driving_safety_rating': 5,
            'vehicle_cleanliness_rating': 5,
            'behavior_rating': 5,
            'fare_honesty_rating': 5,
            'review': 'Clean cab and smooth driving. Helped with luggage and took the safest route.',
        }
    )

    # 5. Create Sample Complaint (tbl_complaint)
    Complaint.objects.get_or_create(
        passenger=p2_user,
        driver=driver_objs[3], # Vinod
        category=Complaint.Category.OVERCHARGING,
        defaults={
            'description': 'Driver demanded excess fare above meter rate during night commute and refused to use standard fare table.',
            'status': 'Pending',
            'penalty_points_deducted': 5,
        }
    )
    print("[+] Created Complaint in tbl_complaint")

    # 6. Create Active SOS Alert (tbl_sos_alert)
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

    # 7. Create Sample Incident Report (tbl_incident_report)
    if not IncidentReport.objects.filter(passenger=p1_user, incident_type='Unsafe Driving').exists():
        IncidentReport.objects.create(
            passenger=p1_user,
            incident_type='Unsafe Driving',
            description='Aggressive overtaking near steep turn on Pala highway.',
            status='Pending',
        )
    print("[+] Created Incident Report in tbl_incident_report")

    print("\n[SUCCESS] SafeRide Database Tables (tbl_*) seeded successfully!")

if __name__ == '__main__':
    run_seed()
