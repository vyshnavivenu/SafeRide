import tempfile
from decimal import Decimal
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from core.models import User, Passenger, Driver, Trip, RatingReview

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class RoleBasedAccessControlTests(TestCase):
    """
    Test Case 3: Role-Based Access Control (RBAC) & View Routing Security Tests
    Verifies that unauthorized roles are strictly forbidden from accessing protected endpoints.
    """

    def setUp(self):
        self.client = Client()
        
        # 1. Administrator User
        self.admin_user = User.objects.create_superuser(
            username='admin_controller',
            email='admin@saferide.org',
            password='password123',
            role=User.Role.ADMIN
        )

        # 2. Passenger User
        self.passenger_user = User.objects.create_user(
            username='passenger_riya',
            email='riya@saferide.org',
            password='password123',
            role=User.Role.PASSENGER,
            phone='9847012345'
        )
        self.passenger_profile = Passenger.objects.create(
            user=self.passenger_user,
            name='Riya Thomas',
            email='riya@saferide.org',
            phone_number='9847012345'
        )

        # 3. Verified Driver User
        self.verified_driver_user = User.objects.create_user(
            username='driver_verified',
            email='verified@saferide.org',
            password='password123',
            role=User.Role.DRIVER,
            phone='9447011111'
        )
        self.verified_driver = Driver.objects.create(
            user=self.verified_driver_user,
            name='Verified Driver',
            email='verified@saferide.org',
            phone_number='9447011111',
            license_number='KL-05-2020002222',
            vehicle_number='KL-05-AT-2222',
            verification_status=Driver.VerificationStatus.VERIFIED
        )

        # 4. Unverified / Pending Driver User
        self.unverified_driver_user = User.objects.create_user(
            username='driver_pending',
            email='pending@saferide.org',
            password='password123',
            role=User.Role.DRIVER,
            phone='9447033333'
        )
        self.unverified_driver = Driver.objects.create(
            user=self.unverified_driver_user,
            name='Pending Driver',
            email='pending@saferide.org',
            phone_number='9447033333',
            license_number='KL-05-2020003333',
            vehicle_number='KL-05-AT-3333',
            verification_status=Driver.VerificationStatus.PENDING
        )

    # -------------------------------------------------------------
    # 1. SECURITY & ACCESS RESTRICTIONS
    # -------------------------------------------------------------
    def test_passenger_cannot_access_driver_dashboard(self):
        """Verify that a Passenger is blocked from accessing the Driver Dashboard."""
        self.client.force_login(self.passenger_user)
        response = self.client.get(reverse('driver_dashboard'))
        # Should either return 403 Forbidden or redirect to passenger dashboard/unauthorized
        self.assertIn(response.status_code, [302, 403])

    def test_passenger_cannot_access_admin_dashboard(self):
        """Verify that a Passenger is blocked from accessing the Administrator Dashboard."""
        self.client.force_login(self.passenger_user)
        response = self.client.get(reverse('admin_dashboard'))
        self.assertIn(response.status_code, [302, 403])

    def test_driver_cannot_access_admin_dashboard(self):
        """Verify that a Driver is blocked from accessing the Administrator Dashboard."""
        self.client.force_login(self.verified_driver_user)
        response = self.client.get(reverse('admin_dashboard'))
        self.assertIn(response.status_code, [302, 403])

    def test_anonymous_user_redirected_from_passenger_dashboard(self):
        """Verify that an unauthenticated guest is redirected to the login page."""
        response = self.client.get(reverse('passenger_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login' in response.url)

    # -------------------------------------------------------------
    # 2. DRIVER VERIFICATION STATUS ACCESS CONTROL
    # -------------------------------------------------------------
    def test_unverified_driver_blocked_from_safety_badge(self):
        """Verify that an unverified (Pending) driver cannot display a public verified badge."""
        self.client.force_login(self.unverified_driver_user)
        response = self.client.get(reverse('driver_id_badge'))
        # Pending driver should be redirected or shown verification pending state
        self.assertIn(response.status_code, [200, 302])
        if response.status_code == 200:
            self.assertContains(response, 'Pending')

    def test_verified_driver_can_access_driver_portal(self):
        """Verify that a Verified driver successfully loads the Driver Dashboard with 200 OK."""
        self.client.force_login(self.verified_driver_user)
        response = self.client.get(reverse('driver_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Verified Driver')

    # -------------------------------------------------------------
    # 3. PASSENGER RIDE INITIATION & BOOKING FLOW
    # -------------------------------------------------------------
    def test_passenger_ride_initiation_flow(self):
        """Verify that a passenger can start a trip with a verified driver, creating an Active trip."""
        self.client.force_login(self.passenger_user)
        
        post_data = {
            'pickup_name': 'St. Thomas College Gate, Palai',
            'pickup_lat': 9.684300,
            'pickup_lng': 76.685300,
            'destination_name': 'Pala KSRTC Bus Station',
            'destination_lat': 9.691200,
            'destination_lng': 76.690400,
        }
        
        response = self.client.post(
            reverse('start_trip', kwargs={'driver_id': self.verified_driver.driver_id}),
            data=post_data,
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify trip created in database
        trip = Trip.objects.filter(passenger=self.passenger_user, driver=self.verified_driver).first()
        self.assertIsNotNone(trip)
        self.assertEqual(trip.status, Trip.Status.ACTIVE)
        self.assertEqual(trip.boarding_address, 'St. Thomas College Gate, Palai')
        self.assertEqual(trip.destination_address, 'Pala KSRTC Bus Station')

    def test_admin_access_to_sos_monitoring_command_center(self):
        """Verify that an Administrator can access the SOS Dispatch Monitoring Command Center."""
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('admin_sos_monitoring'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Live Emergency SOS Dispatch Command')
