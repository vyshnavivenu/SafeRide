"""
================================================================================
          SAFERIDE DATABASE CLEANUP & CURATED DEMO TRIP SEEDER                
================================================================================
Cleans redundant test trips and seeds 3 realistic demonstration journeys:
  - Trip 1: Completed ride with Driver Rajesh (Rated 5.0 ★)
  - Trip 2: Completed ride with Driver Anand (Rated 5.0 ★)
  - Trip 3: Completed ride awaiting rating (with interactive 'Rate Ride' button)
================================================================================
"""

import os
import sys
import django
from decimal import Decimal
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
django.setup()

from django.utils import timezone
from core.models import User, Passenger, Driver, Trip, RatingReview, SOSAlert, Complaint


def cleanup_and_seed_trips():
    print("=" * 70)
    print("CLEANING UP DUPLICATE TEST TRIPS & SEEDING DEMO JOURNEYS")
    print("=" * 70)

    # 1. Clean old test trips and related ratings/alerts
    old_trips_count = Trip.objects.count()
    RatingReview.objects.all().delete()
    SOSAlert.objects.all().delete()
    Trip.objects.all().delete()
    print(f"[OK] Removed {old_trips_count} old test trip sessions, alerts, and reviews.")

    # 2. Get or create passenger 'vyshnavi'
    passenger_user, _ = User.objects.get_or_create(
        username='vyshnavi',
        defaults={
            'email': 'vyshnavi@saferide.org',
            'first_name': 'Vyshnavi',
            'last_name': 'Venu',
            'role': User.Role.PASSENGER,
            'phone': '9846012345'
        }
    )
    passenger_user.set_password('passenger123')
    passenger_user.save()

    passenger_profile, _ = Passenger.objects.get_or_create(
        user=passenger_user,
        defaults={
            'name': 'Vyshnavi Venu',
            'email': 'vyshnavi@saferide.org',
            'phone_number': '9846012345'
        }
    )

    # 3. Ensure Driver Rajesh exists and is verified
    driver_rajesh_user, _ = User.objects.get_or_create(
        username='driver_rajesh',
        defaults={
            'email': 'rajesh@saferide.org',
            'first_name': 'Rajesh',
            'last_name': 'Kumar',
            'role': User.Role.DRIVER,
            'phone': '9447012345'
        }
    )
    driver_rajesh_user.set_password('driver123')
    driver_rajesh_user.save()

    driver_rajesh, _ = Driver.objects.get_or_create(
        user=driver_rajesh_user,
        defaults={
            'name': 'Rajesh Kumar',
            'email': 'rajesh@saferide.org',
            'phone_number': '9447012345',
            'license_number': 'KL-05-2021000892',
            'vehicle_number': 'KL-05-AT-4455',
            'vehicle_type': 'auto',
            'verification_status': Driver.VerificationStatus.VERIFIED,
            'reputation_score': 96.5,
            'total_trips': 142
        }
    )
    driver_rajesh.verification_status = Driver.VerificationStatus.VERIFIED
    driver_rajesh.save()
    driver_rajesh.generate_qr_code()

    # 4. Ensure Driver Anand exists and is verified
    driver_anand_user, _ = User.objects.get_or_create(
        username='driver_anand',
        defaults={
            'email': 'anand@saferide.org',
            'first_name': 'Anand',
            'last_name': 'Menon',
            'role': User.Role.DRIVER,
            'phone': '9447098765'
        }
    )
    driver_anand_user.set_password('driver123')
    driver_anand_user.save()

    driver_anand, _ = Driver.objects.get_or_create(
        user=driver_anand_user,
        defaults={
            'name': 'Anand Menon',
            'email': 'anand@saferide.org',
            'phone_number': '9447098765',
            'license_number': 'KL-05-2020005432',
            'vehicle_number': 'KL-05-TX-1024',
            'vehicle_type': 'taxi',
            'verification_status': Driver.VerificationStatus.VERIFIED,
            'reputation_score': 94.0,
            'total_trips': 98
        }
    )
    driver_anand.verification_status = Driver.VerificationStatus.VERIFIED
    driver_anand.save()
    driver_anand.generate_qr_code()

    now = timezone.now()

    # -------------------------------------------------------------
    # DEMO TRIP 1: Completed ride with Driver Rajesh (Rated 5.0 ★)
    # -------------------------------------------------------------
    trip1 = Trip.objects.create(
        passenger=passenger_user,
        driver=driver_rajesh,
        boarding_address="St. Thomas College Gate, Palai",
        boarding_latitude=Decimal('9.684300'),
        boarding_longitude=Decimal('76.685300'),
        destination_address="Pala KSRTC Bus Stand",
        destination_latitude=Decimal('9.691200'),
        destination_longitude=Decimal('76.690400'),
        start_time=now - timedelta(hours=2),
        end_time=now - timedelta(hours=1, minutes=45),
        status=Trip.Status.COMPLETED
    )
    RatingReview.objects.create(
        trip=trip1,
        passenger=passenger_user,
        driver=driver_rajesh,
        rating=5,
        driving_safety_rating=5,
        vehicle_cleanliness_rating=5,
        behavior_rating=5,
        fare_honesty_rating=5,
        review="Very polite driver, smooth ride, and strict adherence to speed limits."
    )
    print(f"[STAR] Created Demo Trip #{trip1.trip_id} (St. Thomas College -> Pala KSRTC Stand, 5.0 Star Rated)")

    # -------------------------------------------------------------
    # DEMO TRIP 2: Completed ride with Driver Anand (Rated 5.0 ★)
    # -------------------------------------------------------------
    trip2 = Trip.objects.create(
        passenger=passenger_user,
        driver=driver_anand,
        boarding_address="Palai Private Bus Stand",
        boarding_latitude=Decimal('9.688000'),
        boarding_longitude=Decimal('76.687000'),
        destination_address="Mar Sleeva Medicity, Palai",
        destination_latitude=Decimal('9.712600'),
        destination_longitude=Decimal('76.685400'),
        start_time=now - timedelta(days=1, hours=3),
        end_time=now - timedelta(days=1, hours=2, minutes=30),
        status=Trip.Status.COMPLETED
    )
    RatingReview.objects.create(
        trip=trip2,
        passenger=passenger_user,
        driver=driver_anand,
        rating=5,
        driving_safety_rating=5,
        vehicle_cleanliness_rating=5,
        behavior_rating=5,
        fare_honesty_rating=5,
        review="Comfortable taxi ride, clean vehicle, excellent safety protocol."
    )
    print(f"[STAR] Created Demo Trip #{trip2.trip_id} (Palai Private Stand -> Mar Sleeva Medicity, 5.0 Star Rated)")

    # -------------------------------------------------------------
    # DEMO TRIP 3: Completed ride awaiting rating (Rate Ride button active)
    # -------------------------------------------------------------
    trip3 = Trip.objects.create(
        passenger=passenger_user,
        driver=driver_rajesh,
        boarding_address="Pala Municipal Town Hall",
        boarding_latitude=Decimal('9.687500'),
        boarding_longitude=Decimal('76.684800'),
        destination_address="St. Joseph's College of Engineering, Choondacherry",
        destination_latitude=Decimal('9.664000'),
        destination_longitude=Decimal('76.698000'),
        start_time=now - timedelta(minutes=40),
        end_time=now - timedelta(minutes=15),
        status=Trip.Status.COMPLETED
    )
    print(f"[OK] Created Demo Trip #{trip3.trip_id} (Pala Town Hall -> St. Joseph's College, 'Rate Ride' Ready)")

    print("=" * 70)
    print("TRIP HISTORY CLEANUP & SEEDING COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == '__main__':
    cleanup_and_seed_trips()
