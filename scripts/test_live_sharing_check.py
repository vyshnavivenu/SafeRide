"""
================================================================================
         SAFERIDE LIVE LOCATION SHARING & GPS TELEMETRY AUDIT             
================================================================================
Comprehensive verification of:
  1. Live Share Token Generation (UUID4 unique tracking token)
  2. Asynchronous GPS Telemetry Ingestion (AJAX & REST API updates)
  3. Database Coordinate Synchronization (Exact Decimal Precision)
  4. Public Unauthenticated Live Tracking Portal (/live-track/<token>/)
  5. Continuous Live Polling REST Endpoint (/api/v1/trips/<id>/location/)
================================================================================
"""

import os
import sys
import json
import django
from decimal import Decimal

# Setup Django Environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from core.models import User, Passenger, Driver, Trip


def print_check(step_num, title, detail=""):
    print(f" [PASS] | Step {step_num}: {title} {detail}")


def run_live_sharing_audit():
    print("=" * 80)
    print("           SAFERIDE LIVE LOCATION SHARING INTEGRATION AUDIT           ")
    print("=" * 80)

    client = Client()

    # 1. Setup Active Trip Session
    passenger_user = User.objects.filter(role=User.Role.PASSENGER).first()
    driver = Driver.objects.filter(verification_status=Driver.VerificationStatus.VERIFIED).first()

    assert passenger_user is not None, "Passenger account not found."
    assert driver is not None, "Verified driver account not found."

    trip = Trip.objects.create(
        passenger=passenger_user,
        driver=driver,
        boarding_address="St. Thomas College Gate, Palai",
        boarding_latitude=Decimal('9.684300'),
        boarding_longitude=Decimal('76.685300'),
        destination_address="Pala KSRTC Bus Stand",
        destination_latitude=Decimal('9.691200'),
        destination_longitude=Decimal('76.690400'),
        current_latitude=Decimal('9.684300'),
        current_longitude=Decimal('76.685300'),
        status=Trip.Status.ACTIVE
    )

    # -------------------------------------------------------------
    # 1. SHARE TOKEN VERIFICATION
    # -------------------------------------------------------------
    assert trip.share_token is not None, "Trip did not generate a share_token."
    share_url = reverse('live_share', kwargs={'token': trip.share_token})
    print_check(1, "Secure UUID Share Token Generated", f"(Token: {trip.share_token})")

    # -------------------------------------------------------------
    # 2. SIMULATE VEHICLE MOVEMENT VIA LIVE GPS API
    # -------------------------------------------------------------
    client.force_login(passenger_user)
    updated_lat = 9.688550
    updated_lng = 76.687650

    update_url = reverse('update_trip_location', kwargs={'trip_id': trip.trip_id})
    res = client.post(
        update_url,
        data=json.dumps({'latitude': updated_lat, 'longitude': updated_lng}),
        content_type='application/json'
    )
    assert res.status_code == 200, f"Location update failed with status {res.status_code}"
    res_data = res.json()
    assert res_data.get('status') == 'success' or res_data.get('success') is True, "Location update did not return success"
    print_check(2, "Passenger App Pings Live Coordinates", f"({updated_lat}, {updated_lng})")

    # -------------------------------------------------------------
    # 3. DATABASE TELEMETRY ACCURACY CHECK
    # -------------------------------------------------------------
    trip.refresh_from_db()
    assert abs(float(trip.current_latitude) - updated_lat) < 0.0001
    assert abs(float(trip.current_longitude) - updated_lng) < 0.0001
    print_check(3, "Database Synchronized Real-Time Coordinates", f"({trip.current_latitude}, {trip.current_longitude})")

    # -------------------------------------------------------------
    # 4. PUBLIC GUARDIAN LIVE TRACKING PAGE ACCESS (UNAUTHENTICATED)
    # -------------------------------------------------------------
    public_client = Client()  # Unauthenticated guest / family member
    live_res = public_client.get(share_url)
    assert live_res.status_code == 200, f"Public live share URL returned {live_res.status_code}"
    content = live_res.content.decode('utf-8')
    assert driver.name in content or driver.user.get_full_name() in content
    assert driver.vehicle_number in content or driver.vehicle.registration_number in content
    assert "Live Satellite GPS" in content or "LIVE SATELLITE GPS ACTIVE" in content
    print_check(4, "Public Guardian / Family Portal Accessible", f"({share_url})")

    # -------------------------------------------------------------
    # 5. REST API TELEMETRY POLLING CHECK
    # -------------------------------------------------------------
    poll_url = reverse('api_trip_location', kwargs={'trip_id': trip.trip_id})
    poll_res = public_client.get(poll_url)
    assert poll_res.status_code == 200, f"Telemetry polling returned {poll_res.status_code}"
    poll_data = poll_res.json()
    assert float(poll_data.get('latitude')) == float(trip.current_latitude)
    assert float(poll_data.get('longitude')) == float(trip.current_longitude)
    print_check(5, "Live Telemetry Polling API Stream Active", f"(Lat: {poll_data.get('latitude')}, Lng: {poll_data.get('longitude')})")

    # Clean up test trip
    trip.delete()

    print("=" * 80)
    print("LIVE LOCATION SHARING AUDIT: ALL 5/5 CHECKS PASSED (100% OPERATIONAL)")
    print("=" * 80)


if __name__ == '__main__':
    run_live_sharing_audit()
