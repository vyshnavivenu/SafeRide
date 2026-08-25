import tempfile
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from core.models import (
    User, Passenger, Driver, VehicleDocuments,
    Trip, RatingReview, Complaint, SOSAlert
)

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class SafeRideModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. Admin User
        self.admin = User.objects.create_superuser(
            username='test_admin', password='password123', email='admin@test.com', role=User.Role.ADMIN
        )
        
        # 2. Passenger User
        self.passenger = User.objects.create_user(
            username='test_passenger', password='password123', email='passenger@test.com', role=User.Role.PASSENGER
        )
        self.passenger_profile = Passenger.objects.create(
            user=self.passenger,
            emergency_contact_1_name='Emergency Father',
            emergency_contact_1_phone='+91 9876543210',
            emergency_contact_1_relation='Father'
        )
        
        # 3. Driver User & Profile
        self.driver_user = User.objects.create_user(
            username='test_driver', password='password123', email='driver@test.com', role=User.Role.DRIVER
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            license_number='KL-05-TEST9999',
            vehicle_number='KL-05-ZZ-9999',
            vehicle_type='auto',
            experience_years=5,
            verification_status=Driver.VerificationStatus.VERIFIED,
            reputation_score=90.0,
            total_trips=10,
            average_rating=4.8
        )
        self.driver.generate_qr_code()
        self.driver.save()

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SafeRide')

    def test_driver_verification_search(self):
        # Search by vehicle number
        response = self.client.get(reverse('verify_driver_search'), {'query': 'KL-05-ZZ-9999'})
        self.assertEqual(response.status_code, 302) # Redirects to safety card
        
        # Follow redirect
        response = self.client.get(reverse('verify_driver_token', kwargs={'token': self.driver.verification_token}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'KL-05-TEST9999')
        self.assertContains(response, 'VERIFIED')

    def test_qr_code_generated(self):
        self.assertTrue(bool(self.driver.qr_code))

    def test_trip_session_lifecycle_and_rating(self):
        self.client.login(username='test_passenger', password='password123')
        
        # Start Trip
        trip = Trip.objects.create(
            passenger=self.passenger,
            driver=self.driver,
            pickup_location_name='Test Boarding Spot',
            status=Trip.Status.ACTIVE
        )
        self.assertEqual(trip.status, Trip.Status.ACTIVE)
        
        # Complete Trip
        trip.complete_trip()
        self.assertEqual(trip.status, 'Completed')
        self.assertEqual(self.driver.total_trips, 11)

        # Rate Trip
        rating = RatingReview.objects.create(
            trip=trip,
            driver=self.driver,
            passenger=self.passenger,
            rating=5,
            driving_safety_rating=5,
            vehicle_cleanliness_rating=5,
            behavior_rating=5,
            fare_honesty_rating=5,
            review='Excellent smooth ride.'
        )
        self.driver.refresh_from_db()
        self.assertGreaterEqual(self.driver.reputation_score, 80.0)

    def test_sos_alert_trigger(self):
        self.client.login(username='test_passenger', password='password123')
        response = self.client.post(
            reverse('trigger_sos_alert'),
            data={'latitude': 9.6843, 'longitude': 76.6853, 'location_name': 'Test Emergency Point'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SOSAlert.objects.filter(passenger=self.passenger, status=SOSAlert.Status.ACTIVE).exists())

    def test_complaint_and_penalty_deduction(self):
        initial_score = self.driver.reputation_score
        complaint = Complaint.objects.create(
            passenger=self.passenger,
            driver=self.driver,
            category=Complaint.Category.OVERCHARGING,
            description='Test grievance description',
            status=Complaint.Status.OPEN
        )
        complaint.resolve(remarks='Confirmed overcharging', penalty=10)
        self.driver.refresh_from_db()
        self.assertLess(self.driver.reputation_score, initial_score)

    def test_rest_api_endpoints(self):
        # 1. Driver verification API
        response = self.client.get(reverse('api_verify_driver'), {'q': 'KL-05-ZZ-9999'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['found'])

        # 2. Active SOS API
        response = self.client.get(reverse('api_sos_active'))
        self.assertEqual(response.status_code, 200)
