import tempfile
from decimal import Decimal
from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.models import User, Passenger, Driver, Trip, SOSAlert

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class EmergencyAndTrackingAPITests(APITestCase):
    """
    Test Case 4: REST API, Live GPS Tracking & Real-Time SOS Dispatch Tests
    Uses Django REST Framework's APIClient to simulate asynchronous AJAX and mobile app calls.
    """

    def setUp(self):
        self.client = APIClient()

        # 1. Passenger User
        self.passenger = User.objects.create_user(
            username='api_passenger',
            email='api_passenger@saferide.org',
            password='password123',
            role=User.Role.PASSENGER,
            phone='9846055555'
        )
        self.passenger_profile = Passenger.objects.create(
            user=self.passenger,
            name='API Passenger',
            email='api_passenger@saferide.org',
            phone_number='9846055555'
        )

        # 2. Verified Driver
        self.driver_user = User.objects.create_user(
            username='api_driver',
            email='api_driver@saferide.org',
            password='password123',
            role=User.Role.DRIVER,
            phone='9846066666'
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            name='API Driver',
            email='api_driver@saferide.org',
            phone_number='9846066666',
            license_number='KL-05-2022005555',
            vehicle_number='KL-05-AT-5555',
            verification_status=Driver.VerificationStatus.VERIFIED
        )

        # 3. Active Trip Session
        self.trip = Trip.objects.create(
            passenger=self.passenger,
            driver=self.driver,
            boarding_latitude=Decimal('9.684300'),
            boarding_longitude=Decimal('76.685300'),
            boarding_address="Palai Main Junction",
            current_latitude=Decimal('9.684300'),
            current_longitude=Decimal('76.685300'),
            status=Trip.Status.ACTIVE
        )

    # -------------------------------------------------------------
    # 1. LIVE GPS TELEMETRY PING UPDATE API
    # -------------------------------------------------------------
    def test_update_live_location_api(self):
        """
        Scenario: Mobile GPS ping continuously updates the vehicle's coordinates.
        Action: Send JSON POST with new coordinates to /api/trip/<trip_id>/location/.
        Expectation: HTTP 200 OK, JSON success=True, and Trip database coordinates updated.
        """
        self.client.force_authenticate(user=self.passenger)
        
        new_lat = 9.689555
        new_lng = 76.688777

        payload = {
            'latitude': new_lat,
            'longitude': new_lng
        }

        url = reverse('api_trip_location', kwargs={'trip_id': self.trip.trip_id})
        response = self.client.post(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json() if hasattr(response, 'json') else response.data
        self.assertTrue(data.get('success'))

        # Verify Trip coordinates updated in the database
        self.trip.refresh_from_db()
        self.assertAlmostEqual(float(self.trip.current_latitude), new_lat, places=4)
        self.assertAlmostEqual(float(self.trip.current_longitude), new_lng, places=4)

    # -------------------------------------------------------------
    # 2. EMERGENCY SOS REAL-TIME DISPATCH API
    # -------------------------------------------------------------
    def test_sos_dispatch_trigger_api(self):
        """
        Scenario: Passenger triggers 1-touch Emergency SOS button during an active ride.
        Action: Send JSON POST to /api/sos/trigger/ with GPS distress payload.
        Expectation: HTTP 200 OK, JSON success=True, alert_id returned,
                     instant SOSAlert creation in tbl_sos_alert, and Trip status becomes SOS_TRIGGERED.
        """
        self.client.force_authenticate(user=self.passenger)

        sos_lat = 9.691234
        sos_lng = 76.690456

        payload = {
            'trip_id': self.trip.trip_id,
            'driver_id': self.driver.driver_id,
            'latitude': sos_lat,
            'longitude': sos_lng,
            'location_name': 'Emergency Transit Corridor SH-32'
        }

        url = reverse('api_sos_trigger')
        response = self.client.post(url, data=payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json() if hasattr(response, 'json') else response.data
        self.assertTrue(data.get('success'))
        self.assertIn('alert_id', data)

        alert_id = data['alert_id']

        # Verify database record in tbl_sos_alert
        sos_alert = SOSAlert.objects.filter(sos_id=alert_id).first()
        self.assertIsNotNone(sos_alert)
        self.assertEqual(sos_alert.passenger, self.passenger)
        self.assertEqual(sos_alert.driver, self.driver)
        self.assertEqual(sos_alert.trip, self.trip)
        self.assertEqual(sos_alert.status, SOSAlert.Status.ACTIVE)
        self.assertAlmostEqual(float(sos_alert.latitude), sos_lat, places=4)
        self.assertAlmostEqual(float(sos_alert.longitude), sos_lng, places=4)

        # Verify Trip state transitioned to SOS_TRIGGERED
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.status, Trip.Status.SOS_TRIGGERED)

    # -------------------------------------------------------------
    # 3. VERIFIED DRIVERS DIRECTORY API
    # -------------------------------------------------------------
    def test_driver_directory_api_returns_verified_drivers(self):
        """
        Scenario: Passenger / Public app queries the verified driver directory.
        Action: GET /api/v1/drivers/.
        Expectation: HTTP 200 OK with list of registered verified drivers.
        """
        url = reverse('api_driver_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json() if hasattr(response, 'json') else response.data
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 1)
