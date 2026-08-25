import os
import django
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
django.setup()

from django.utils import timezone
from core.models import (
    User, Admin, Passenger, Driver, VehicleDocuments, VehicleDetails,
    Trip, RatingReview, Complaint, SOSAlert, IncidentReport
)

def seed():
    print(">>> Starting SafeRide Database Seeding...")

    # 1. System Administrators
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
    Admin.objects.get_or_create(user=admin_user, defaults={'name': 'Central Safety Control', 'email': 'admin@saferide.org', 'password': admin_user.password})

    # 2. Registered Passengers
    passengers_data = [
        {
            'username': 'vyshnavi', 'first_name': 'Vyshnavi', 'last_name': 'Venu',
            'email': 'vyshnavi@gmail.com', 'phone': '+91 94471 23456',
            'ec1_name': 'Venu K. (Father)', 'ec1_phone': '+91 94470 11223', 'ec1_rel': 'Father',
            'ec2_name': 'Anjali Venu (Sister)', 'ec2_phone': '+91 98460 55443', 'ec2_rel': 'Sister',
            'ec3_name': 'Hostel Warden (SJCET)', 'ec3_phone': '+91 94950 88776', 'ec3_rel': 'Warden',
        },
        {
            'username': 'meghanair', 'first_name': 'Megha', 'last_name': 'Nair',
            'email': 'megha.nair@gmail.com', 'phone': '+91 98461 98765',
            'ec1_name': 'Suresh Nair (Father)', 'ec1_phone': '+91 98460 12345', 'ec1_rel': 'Father',
            'ec2_name': 'Pooja Pillai (Friend)', 'ec2_phone': '+91 97450 67890', 'ec2_rel': 'Friend',
            'ec3_name': 'Campus Security Desk', 'ec3_phone': '+91 94460 33221', 'ec3_rel': 'Campus Security',
        },
        {
            'username': 'rohit_menon', 'first_name': 'Rohit', 'last_name': 'Menon',
            'email': 'rohit.menon@gmail.com', 'phone': '+91 97451 12389',
            'ec1_name': 'Deepa Menon (Mother)', 'ec1_phone': '+91 97450 99887', 'ec1_rel': 'Mother',
            'ec2_name': 'Arun George (Roommate)', 'ec2_phone': '+91 94951 44556', 'ec2_rel': 'Friend',
            'ec3_name': 'Emergency Police Helpline', 'ec3_phone': '112', 'ec3_rel': 'Emergency Service',
        },
        {
            'username': 'ananya_s', 'first_name': 'Ananya', 'last_name': 'Sharma',
            'email': 'ananya.sharma@infopark.com', 'phone': '+91 99462 87654',
            'ec1_name': 'Rajesh Sharma (Spouse)', 'ec1_phone': '+91 99460 22110', 'ec1_rel': 'Spouse',
            'ec2_name': 'Kochi Police Control', 'ec2_phone': '112', 'ec2_rel': 'Police',
            'ec3_name': 'Women Helpline Desk', 'ec3_phone': '1091', 'ec3_rel': 'Helpline',
        },
    ]

    passengers = []
    for pd in passengers_data:
        u, _ = User.objects.get_or_create(
            username=pd['username'],
            defaults={
                'first_name': pd['first_name'],
                'last_name': pd['last_name'],
                'email': pd['email'],
                'phone': pd['phone'],
                'role': User.Role.PASSENGER
            }
        )
        u.set_password('passenger123')
        u.save()

        p, _ = Passenger.objects.get_or_create(
            user=u,
            defaults={
                'name': f"{pd['first_name']} {pd['last_name']}",
                'email': pd['email'],
                'phone_number': pd['phone'],
                'password': u.password,
                'emergency_contact_1_name': pd['ec1_name'],
                'emergency_contact_1_phone': pd['ec1_phone'],
                'emergency_contact_1_relation': pd['ec1_rel'],
                'emergency_contact_2_name': pd['ec2_name'],
                'emergency_contact_2_phone': pd['ec2_phone'],
                'emergency_contact_2_relation': pd['ec2_rel'],
                'emergency_contact_3_name': pd['ec3_name'],
                'emergency_contact_3_phone': pd['ec3_phone'],
                'emergency_contact_3_relation': pd['ec3_rel'],
            }
        )
        passengers.append(u)

    print(f"Verified {len(passengers)} Passengers seeded.")

    # 3. Verified and Pending Drivers
    drivers_data = [
        {
            'username': 'driver_rajesh', 'name': 'Rajesh Kumar', 'phone': '+91 94471 82930',
            'email': 'rajesh.auto@gmail.com', 'license': 'KL-05-2021000892', 'vehicle_num': 'KL-05-AT-4455',
            'vehicle_type': 'auto', 'make_model': 'Bajaj RE Compact 4S Auto', 'exp': 8,
            'status': Driver.VerificationStatus.VERIFIED, 'reputation': 95.8, 'avg_rating': 4.9, 'trips': 142
        },
        {
            'username': 'driver_vinod', 'name': 'Vinod Mohan', 'phone': '+91 98462 73849',
            'email': 'vinod.taxi@gmail.com', 'license': 'KL-05-20190005512', 'vehicle_num': 'KL-05-CB-3344',
            'vehicle_type': 'taxi', 'make_model': 'Maruti Suzuki Dzire Tour', 'exp': 12,
            'status': Driver.VerificationStatus.VERIFIED, 'reputation': 92.4, 'avg_rating': 4.7, 'trips': 210
        },
        {
            'username': 'driver_anoop', 'name': 'Anoop Rajan', 'phone': '+91 97453 62718',
            'email': 'anoop.rajan@gmail.com', 'license': 'KL-35-20230009988', 'vehicle_num': 'KL-35-AT-6622',
            'vehicle_type': 'cab', 'make_model': 'Hyundai Aura CNG Cab', 'exp': 5,
            'status': Driver.VerificationStatus.VERIFIED, 'reputation': 96.5, 'avg_rating': 4.9, 'trips': 88
        },
        {
            'username': 'driver_shaji', 'name': 'Shaji Thomas', 'phone': '+91 99464 51627',
            'email': 'shaji.ev@gmail.com', 'license': 'KL-05-20210006678', 'vehicle_num': 'KL-05-EV-1205',
            'vehicle_type': 'auto', 'make_model': 'Mahindra Treo Electric Auto', 'exp': 6,
            'status': Driver.VerificationStatus.VERIFIED, 'reputation': 98.2, 'avg_rating': 5.0, 'trips': 175
        },
        {
            'username': 'driver_deepak', 'name': 'Deepak K. S.', 'phone': '+91 94955 40516',
            'email': 'deepak.ks@gmail.com', 'license': 'KL-07-20140003321', 'vehicle_num': 'KL-07-CB-9080',
            'vehicle_type': 'auto', 'make_model': 'Piaggio Ape City Plus', 'exp': 10,
            'status': Driver.VerificationStatus.VERIFIED, 'reputation': 89.0, 'avg_rating': 4.5, 'trips': 190
        },
        {
            'username': 'driver_suresh', 'name': 'Suresh G. Pillai', 'phone': '+91 98476 39485',
            'email': 'suresh.van@gmail.com', 'license': 'KL-05-20180004411', 'vehicle_num': 'KL-05-TX-7890',
            'vehicle_type': 'van', 'make_model': 'Force Traveller 12-Seater', 'exp': 14,
            'status': Driver.VerificationStatus.PENDING, 'reputation': 90.0, 'avg_rating': 4.8, 'trips': 0
        },
        {
            'username': 'driver_manoj', 'name': 'Manoj V. Nair', 'phone': '+91 97467 28394',
            'email': 'manoj.pala@gmail.com', 'license': 'KL-35-20220007733', 'vehicle_num': 'KL-35-R-4512',
            'vehicle_type': 'auto', 'make_model': 'Bajaj Maxima Z Diesel', 'exp': 4,
            'status': Driver.VerificationStatus.PENDING, 'reputation': 90.0, 'avg_rating': 4.8, 'trips': 0
        },
    ]

    drivers = []
    for dd in drivers_data:
        u, _ = User.objects.get_or_create(
            username=dd['username'],
            defaults={
                'first_name': dd['name'].split()[0],
                'last_name': " ".join(dd['name'].split()[1:]),
                'email': dd['email'],
                'phone': dd['phone'],
                'role': User.Role.DRIVER
            }
        )
        u.set_password('driver123')
        u.save()

        d, _ = Driver.objects.get_or_create(
            user=u,
            defaults={
                'name': dd['name'],
                'phone_number': dd['phone'],
                'email': dd['email'],
                'license_number': dd['license'],
                'vehicle_number': dd['vehicle_num'],
                'vehicle_type': dd['vehicle_type'],
                'password': u.password,
                'experience_years': dd['exp'],
                'verification_status': dd['status'],
                'reputation_score': dd['reputation'],
                'average_rating': dd['avg_rating'],
                'total_trips': dd['trips'],
                'verified_at': timezone.now() if dd['status'] == Driver.VerificationStatus.VERIFIED else None,
                'verification_notes': 'Document verified by Central Transport Inspector' if dd['status'] == Driver.VerificationStatus.VERIFIED else 'Awaiting license inspection',
            }
        )
        # Generate QR code PNG
        if d.is_verified() and not d.qr_code:
            d.generate_qr_code('http://127.0.0.1:8000')
            d.save()

        # Link Vehicle documents
        VehicleDocuments.objects.get_or_create(
            driver=d,
            defaults={
                'license_doc': f"{dd['license']}_verified.pdf",
                'rc_doc': f"{dd['vehicle_num']}_rc.pdf",
            }
        )
        drivers.append(d)

    print(f"Verified {len(drivers)} Drivers seeded with vehicle specs and digital QR codes.")

    # 4. Realistic Trips & Routes
    transit_routes = [
        ('St. Joseph\'s College of Engineering & Technology, Palai', 9.684300, 76.685300, 'Palai KSRTC Bus Terminal', 9.711800, 76.684400),
        ('Pala Private Bus Stand', 9.712500, 76.683000, 'Alphonsa College, Palai', 9.702000, 76.689000),
        ('Pala Town Centre', 9.713000, 76.685000, 'Mar Sleeva Medicity, Cherpunkal', 9.664000, 76.612000),
        ('St. Thomas College, Palai', 9.715000, 76.681000, 'Kottayam Railway Station', 9.589000, 76.522000),
        ('Kottayam Medical College', 9.624000, 76.538000, 'Kottayam KSRTC Stand', 9.591000, 76.524000),
    ]

    reviews_text = [
        ("Very polite driver! Drove at safe speed throughout the rain.", 5, 5, 5, 5, 5),
        ("Extremely smooth and punctual commute. Clean auto-rickshaw.", 5, 5, 5, 5, 5),
        ("Driver was courteous and charged strictly by the digital fare rate.", 5, 5, 5, 5, 5),
        ("Helpful driver, verified QR badge matched the vehicle license plate perfectly.", 5, 5, 5, 5, 5),
        ("Comfortable ride. Followed direct route without unnecessary deviation.", 4, 4, 5, 4, 4),
        ("Prompt pickup near the college main gate. Recommended for night commuters.", 5, 5, 5, 5, 5),
    ]

    now = timezone.now()
    rajesh_driver = Driver.objects.get(user__username='driver_rajesh')
    vyshnavi_user = User.objects.get(username='vyshnavi')

    for i in range(8):
        route = transit_routes[i % len(transit_routes)]
        d = drivers[i % 5] # verified drivers only
        p = passengers[i % len(passengers)]
        
        trip_time = now - timedelta(days=i, hours=random.randint(1, 10))
        trip, created = Trip.objects.get_or_create(
            passenger=p,
            driver=d,
            start_time=trip_time,
            defaults={
                'boarding_address': route[0],
                'boarding_latitude': route[1],
                'boarding_longitude': route[2],
                'destination_address': route[3],
                'destination_latitude': route[4],
                'destination_longitude': route[5],
                'current_latitude': route[4],
                'current_longitude': route[5],
                'end_time': trip_time + timedelta(minutes=random.randint(15, 40)),
                'status': 'Completed'
            }
        )

        if created:
            r_data = reviews_text[i % len(reviews_text)]
            RatingReview.objects.get_or_create(
                trip=trip,
                defaults={
                    'passenger': p,
                    'driver': d,
                    'rating': r_data[1],
                    'driving_safety_rating': r_data[2],
                    'vehicle_cleanliness_rating': r_data[3],
                    'behavior_rating': r_data[4],
                    'fare_honesty_rating': r_data[5],
                    'review': r_data[0],
                    'created_at': trip.end_time or now
                }
            )

    print("Created historical verified trips & passenger ratings.")

    # 5. Complaints & Grievances
    vinod_driver = Driver.objects.get(user__username='driver_vinod')
    megha_user = User.objects.get(username='meghanair')
    
    c1, _ = Complaint.objects.get_or_create(
        passenger=megha_user,
        driver=vinod_driver,
        category=Complaint.Category.OVERCHARGING,
        defaults={
            'description': 'Driver demanded 50 rupees above the standard meter fare during late night commute from Pala bus stand.',
            'status': 'Pending',
            'created_at': now - timedelta(hours=3),
        }
    )

    c2, _ = Complaint.objects.get_or_create(
        passenger=vyshnavi_user,
        driver=rajesh_driver,
        category=Complaint.Category.MISBEHAVIOR,
        defaults={
            'description': 'Driver was talking loudly on phone while navigating intersection.',
            'status': 'Resolved',
            'admin_remarks': 'Driver Rajesh was summoned, issued a formal safety caution, and 5 penalty points were deducted from reputation.',
            'penalty_points_deducted': 5,
            'resolved_at': now - timedelta(days=2),
            'created_at': now - timedelta(days=3),
        }
    )
    print("Seeded realistic complaints & grievance redressal records.")

    # 6. Real-Time Emergency SOS Alerts
    SOSAlert.objects.get_or_create(
        passenger=megha_user,
        driver=vinod_driver,
        defaults={
            'latitude': 9.684300,
            'longitude': 76.685300,
            'location_name': "Near SJCET Main Campus Gate, Palai",
            'status': 'Active',
            'timestamp': now - timedelta(minutes=4),
            'dispatched_services': 'Palai Police Station (112), Women Helpline (1091)',
        }
    )

    SOSAlert.objects.get_or_create(
        passenger=vyshnavi_user,
        driver=rajesh_driver,
        defaults={
            'latitude': 9.712500,
            'longitude': 76.683000,
            'location_name': "Pala Private Bus Stand Terminal",
            'status': 'Resolved',
            'timestamp': now - timedelta(days=1),
            'admin_notes': '1-Touch test alert triggered by commuter. Passenger confirmed safe.',
            'resolved_at': now - timedelta(days=1, minutes=-10),
        }
    )
    print("Seeded realistic SOS emergency distress alerts.")

    # Recalculate all driver reputation scores
    for d in Driver.objects.all():
        d.recalculate_reputation()

    print(">>> SAFE RIDE DATABASE SEEDING COMPLETED SUCCESSFULLY 100%! <<<")

if __name__ == '__main__':
    seed()
