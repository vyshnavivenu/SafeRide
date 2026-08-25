"""
================================================================================
          SAFERIDE END-TO-END "HAPPY PATH" WORKFLOW INTEGRATION AUDIT         
================================================================================
Simulates the complete real-world passenger and driver safety lifecycle:
  1. Passenger Authentication & Session Initialization
  2. Driver QR Code Safety Verification Scan
  3. Geolocation Capture & Safe Trip Initiation
  4. Active Trip Telemetry & Status Verification
  5. Asynchronous SOS Emergency Distress Beacon Dispatch (AJAX / Fetch)
  6. Safe Trip Completion & 5-Star Rating / Reputation Recalculation
================================================================================
"""

import os
import sys
import json
import django
from decimal import Decimal

# Setup Django Environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from core.models import User, Passenger, Driver, Trip, SOSAlert, RatingReview


def print_step(step_num, title, status="RUNNING"):
    colors = {
        "PASS": "\033[92m[PASS]\033[0m",
        "FAIL": "\033[91m[FAIL]\033[0m",
        "RUNNING": "\033[94m[RUNNING]\033[0m"
    }
    print(f" {colors.get(status, status)} | Stage {step_num}: {title}")


def run_happy_path_verification():
    print("=" * 80)
    print("          SAFERIDE PRODUCTION E2E 'HAPPY PATH' SIMULATION         ")
    print("=" * 80)

    client = Client()

    # Setup: Clean or initialize Passenger and Verified Driver
    passenger_user, _ = User.objects.get_or_create(
        username='vyshnavi_e2e',
        defaults={
            'email': 'vyshnavi.e2e@saferide.org',
            'role': User.Role.PASSENGER,
            'phone': '9846012345'
        }
    )
    passenger_user.set_password('password123')
    passenger_user.save()

    passenger_profile, _ = Passenger.objects.get_or_create(
        user=passenger_user,
        defaults={
            'name': 'Vyshnavi Venu',
            'email': 'vyshnavi.e2e@saferide.org',
            'phone_number': '9846012345'
        }
    )

    driver = Driver.objects.filter(verification_status=Driver.VerificationStatus.VERIFIED).first()
    if not driver:
        driver_user, _ = User.objects.get_or_create(
            username='rajesh_driver_e2e',
            defaults={
                'email': 'rajesh.driver.e2e@saferide.org',
                'role': User.Role.DRIVER,
                'phone': '9447012399'
            }
        )
        driver_user.set_password('password123')
        driver_user.save()

        driver = Driver.objects.create(
            user=driver_user,
            name='Rajesh Kumar',
            email='rajesh.driver.e2e@saferide.org',
            phone_number='9447012399',
            license_number='KL-05-2022009999',
            vehicle_number='KL-05-AT-9999',
            vehicle_type='auto',
            verification_status=Driver.VerificationStatus.VERIFIED
        )
    driver.verification_status = Driver.VerificationStatus.VERIFIED
    driver.save()
    driver.generate_qr_code()

    # -------------------------------------------------------------
    # STAGE 1: PASSENGER LOGS IN
    # -------------------------------------------------------------
    login_success = client.login(username='vyshnavi_e2e', password='password123')
    assert login_success, "Failed to authenticate passenger user."
    
    dash_res = client.get(reverse('passenger_dashboard'))
    assert dash_res.status_code == 200, f"Dashboard returned status {dash_res.status_code}"
    print_step(1, "Passenger Authentication & Dashboard Session Initialized", "PASS")

    # -------------------------------------------------------------
    # STAGE 2: PASSENGER SCANS VERIFIED DRIVER'S QR CODE
    # -------------------------------------------------------------
    verify_url = reverse('verify_driver_token', kwargs={'token': driver.verification_token})
    verify_res = client.get(verify_url)
    assert verify_res.status_code == 200, f"Driver QR verification returned {verify_res.status_code}"
    assert "Rajesh Kumar" in verify_res.content.decode('utf-8')
    assert "KL-05-AT-4455" in verify_res.content.decode('utf-8')
    print_step(2, f"Passenger Scans Verified Driver QR Badge ({driver.vehicle_number})", "PASS")

    # -------------------------------------------------------------
    # STAGE 3: DESTINATION ENTERED & BROWSER FETCHES GPS COORDINATES
    # -------------------------------------------------------------
    start_trip_url = reverse('start_trip', kwargs={'driver_id': driver.driver_id})
    trip_payload = {
        'pickup_name': 'St. Thomas College Gate, Palai',
        'pickup_lat': 9.684300,
        'pickup_lng': 76.685300,
        'destination_name': 'Pala KSRTC Bus Stand',
        'destination_lat': 9.691200,
        'destination_lng': 76.690400
    }
    start_res = client.post(start_trip_url, data=trip_payload, follow=True)
    assert start_res.status_code == 200, f"Start trip request failed with status {start_res.status_code}"
    print_step(3, "Destination Entered & Live Geolocation Coordinates Captured", "PASS")

    # -------------------------------------------------------------
    # STAGE 4: TRIP STATUS BECOMES 'ACTIVE' WITH FIXED PRECISION
    # -------------------------------------------------------------
    active_trip = Trip.objects.filter(passenger=passenger_user, driver=driver, status=Trip.Status.ACTIVE).order_by('-start_time').first()
    assert active_trip is not None, "Active trip was not found in the database."
    assert active_trip.status == Trip.Status.ACTIVE
    assert abs(float(active_trip.boarding_latitude) - 9.684300) < 0.0001
    assert abs(float(active_trip.boarding_longitude) - 76.685300) < 0.0001
    print_step(4, f"Trip #{active_trip.trip_id} Status Transitioned to 'Active' (Telemetry Synced)", "PASS")

    # -------------------------------------------------------------
    # STAGE 5: SOS BUTTON CLICKED -> FETCH JSON PAYLOAD -> SUCCESS
    # -------------------------------------------------------------
    sos_api_url = reverse('trigger_sos_alert')
    sos_payload = {
        'trip_id': active_trip.trip_id,
        'driver_id': driver.driver_id,
        'latitude': 9.689500,
        'longitude': 76.688100,
        'location_name': 'Emergency Transit Corridor SH-32'
    }
    sos_res = client.post(
        sos_api_url,
        data=json.dumps(sos_payload),
        content_type='application/json'
    )
    assert sos_res.status_code in [200, 201], f"SOS API returned status {sos_res.status_code}"
    sos_json = sos_res.json()
    assert sos_res.status_code == 200 and (sos_json.get('status') == 'success' or sos_json.get('success') is True), "SOS API failed"
    print_step(5, f"Distress Beacon #{sos_json.get('alert_id')} Broadcasted to Admin Real-Time Queue", "PASS")

    # Verify SOS record in tbl_sos_alert
    sos_alert = SOSAlert.objects.get(sos_id=sos_json['alert_id'])
    assert sos_alert.status == SOSAlert.Status.ACTIVE
    assert abs(float(sos_alert.latitude) - 9.689500) < 0.0001
    
    # Verify trip status transitioned to SOS_TRIGGERED
    active_trip.refresh_from_db()
    assert active_trip.status == Trip.Status.SOS_TRIGGERED
    print_step(5, f"1-Touch SOS Beacon Dispatched (Alert #{sos_alert.sos_id} Logged to DB)", "PASS")

    # -------------------------------------------------------------
    # STAGE 6: TRIP ENDS & PASSENGER SUBMITS 5-STAR RATING
    # -------------------------------------------------------------
    active_trip.complete_trip()
    assert active_trip.status == Trip.Status.COMPLETED
    assert active_trip.end_time is not None

    rating_url = reverse('rate_trip', kwargs={'trip_id': active_trip.trip_id})
    rating_payload = {
        'rating': 5,
        'driving_safety_rating': 5,
        'vehicle_cleanliness_rating': 5,
        'behavior_rating': 5,
        'fare_honesty_rating': 5,
        'review': 'Exceptional service, smooth driving, and top-notch safety compliance!'
    }
    rate_res = client.post(rating_url, data=rating_payload, follow=True)
    assert rate_res.status_code == 200, f"Rating submission returned {rate_res.status_code}"

    # Verify RatingReview in tbl_rating_review
    review_obj = RatingReview.objects.filter(trip=active_trip).first()
    assert review_obj is not None, "RatingReview record was not created."
    assert review_obj.rating == 5
    
    driver.refresh_from_db()
    assert driver.average_rating > 0
    print_step(6, f"Trip Completed Safely & 5-Star Rating Submitted (Reputation: {driver.reputation_score}/100)", "PASS")

    print("=" * 80)
    print("ALL 6 STAGES OF THE PRODUCTION HAPPY PATH EXECUTED WITH 100% SUCCESS!")
    print("=" * 80)


if __name__ == '__main__':
    run_happy_path_verification()
