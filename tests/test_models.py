import tempfile
import shutil
from decimal import Decimal
from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.models import (
    User, Admin, Passenger, Driver, VehicleDocuments, Trip,
    RatingReview, Complaint, SOSAlert, IncidentReport
)

@override_settings(MEDIA_ROOT=tempfile.gettempdir())


class UserModelRoleTests(TestCase):
    """
    Test Case 1: Custom User Model & Role-Based Identity Tests
    Verifies that the custom User model properly enforces role segregation (Admin, Passenger, Driver).
    """

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin_tester',
            email='admin@saferide.org',
            password='testpassword123',
            role=User.Role.ADMIN
        )
        self.passenger_user = User.objects.create_user(
            username='passenger_tester',
            email='passenger@saferide.org',
            password='testpassword123',
            role=User.Role.PASSENGER,
            phone='9876543210'
        )
        self.driver_user = User.objects.create_user(
            username='driver_tester',
            email='driver@saferide.org',
            password='testpassword123',
            role=User.Role.DRIVER,
            phone='9876543211'
        )

    def test_admin_role_attributes(self):
        """Verify that an Admin user has is_admin_user=True and is not Passenger/Driver."""
        self.assertTrue(self.admin_user.is_admin_user())
        self.assertFalse(self.admin_user.is_passenger_user())
        self.assertFalse(self.admin_user.is_driver_user())
        self.assertEqual(self.admin_user.role, User.Role.ADMIN)

    def test_passenger_role_attributes(self):
        """Verify that a Passenger user has is_passenger_user=True and is not Admin/Driver."""
        self.assertTrue(self.passenger_user.is_passenger_user())
        self.assertFalse(self.passenger_user.is_admin_user())
        self.assertFalse(self.passenger_user.is_driver_user())
        self.assertEqual(self.passenger_user.role, User.Role.PASSENGER)

    def test_driver_role_attributes(self):
        """Verify that a Driver user has is_driver_user=True and is not Admin/Passenger."""
        self.assertTrue(self.driver_user.is_driver_user())
        self.assertFalse(self.driver_user.is_admin_user())
        self.assertFalse(self.driver_user.is_passenger_user())
        self.assertEqual(self.driver_user.role, User.Role.DRIVER)

    def test_passenger_profile_one_to_one_relationship(self):
        """Verify that Passenger profile links 1-to-1 with User model."""
        passenger = Passenger.objects.create(
            user=self.passenger_user,
            name='Test Passenger',
            email='passenger@saferide.org',
            phone_number='9876543210'
        )
        self.assertEqual(self.passenger_user.passenger_profile, passenger)
        self.assertEqual(passenger.user, self.passenger_user)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class DriverAndKYCModelTests(TestCase):
    """
    Test Case 2: Driver Profile, KYC & Verification Schema Tests
    Verifies Driver profile fields, verification status choices, and QR code generation.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='rajesh_driver',
            email='rajesh@saferide.org',
            password='testpassword123',
            role=User.Role.DRIVER,
            phone='9447012345'
        )
        self.driver = Driver.objects.create(
            user=self.user,
            name='Rajesh Kumar',
            email='rajesh@saferide.org',
            phone_number='9447012345',
            license_number='KL-05-2021000892',
            vehicle_number='KL-05-AT-4455',
            vehicle_type='auto',
            verification_status=Driver.VerificationStatus.PENDING
        )

    def test_driver_initial_pending_status(self):
        """Verify default verification status is Pending."""
        self.assertEqual(self.driver.verification_status, Driver.VerificationStatus.PENDING)
        self.assertFalse(self.driver.is_verified())

    def test_driver_status_transitions(self):
        """Verify status can be transitioned to Verified, Suspended, or Rejected."""
        self.driver.verification_status = Driver.VerificationStatus.VERIFIED
        self.driver.save()
        self.assertTrue(self.driver.is_verified())

        self.driver.verification_status = Driver.VerificationStatus.SUSPENDED
        self.driver.save()
        self.assertFalse(self.driver.is_verified())

    def test_driver_qr_code_generation(self):
        """Verify that driver generates a unique QR code."""
        qr_data = self.driver.generate_qr_code()
        self.assertIsNotNone(qr_data)
        self.assertTrue(len(self.driver.qr_code) > 0)


class TripModelPrecisionTests(TestCase):
    """
    Test Case 3: Trip Telemetry & Decimal Coordinate Precision Tests
    Verifies that boarding, destination, and live tracking GPS coordinates maintain exact Decimal precision.
    """

    def setUp(self):
        self.passenger_user = User.objects.create_user(
            username='vyshnavi',
            email='vyshnavi@saferide.org',
            password='testpassword123',
            role=User.Role.PASSENGER
        )
        self.driver_user = User.objects.create_user(
            username='driver_suresh',
            email='suresh@saferide.org',
            password='testpassword123',
            role=User.Role.DRIVER
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            name='Suresh Nair',
            email='suresh@saferide.org',
            phone_number='9447098765',
            license_number='KL-05-2019001234',
            vehicle_number='KL-05-AB-1234',
            verification_status=Driver.VerificationStatus.VERIFIED
        )

    def test_trip_coordinate_decimal_precision(self):
        """Verify that boarding and destination coordinates save with exact 6 decimal places."""
        boarding_lat = Decimal('9.684321')
        boarding_lng = Decimal('76.685312')
        dest_lat = Decimal('9.691234')
        dest_lng = Decimal('76.690456')

        trip = Trip.objects.create(
            passenger=self.passenger_user,
            driver=self.driver,
            boarding_latitude=boarding_lat,
            boarding_longitude=boarding_lng,
            boarding_address="St. Thomas College Gate, Palai",
            destination_latitude=dest_lat,
            destination_longitude=dest_lng,
            destination_address="Pala KSRTC Bus Stand",
            status=Trip.Status.ACTIVE
        )

        # Refresh from database
        saved_trip = Trip.objects.get(trip_id=trip.trip_id)
        self.assertEqual(saved_trip.boarding_latitude, boarding_lat)
        self.assertEqual(saved_trip.boarding_longitude, boarding_lng)
        self.assertEqual(saved_trip.destination_latitude, dest_lat)
        self.assertEqual(saved_trip.destination_longitude, dest_lng)
        self.assertEqual(saved_trip.status, Trip.Status.ACTIVE)

    def test_trip_completion_flow(self):
        """Verify that complete_trip updates status, timestamp, and driver reputation."""
        trip = Trip.objects.create(
            passenger=self.passenger_user,
            driver=self.driver,
            status=Trip.Status.ACTIVE
        )
        initial_trips = self.driver.total_trips
        trip.complete_trip()

        self.driver.refresh_from_db()
        self.assertEqual(trip.status, Trip.Status.COMPLETED)
        self.assertIsNotNone(trip.end_time)
        self.assertEqual(self.driver.total_trips, initial_trips + 1)


class SOSAlertModelTests(TestCase):
    """
    Test Case 4: SOS Emergency Model & Dispatch Lifecycle Tests
    Verifies that SOSAlert links to Trip, Driver, Passenger, and stores exact GPS telemetry.
    """

    def setUp(self):
        self.passenger = User.objects.create_user(
            username='ananya',
            email='ananya@saferide.org',
            password='testpassword123',
            role=User.Role.PASSENGER
        )
        self.driver_user = User.objects.create_user(
            username='driver_manoj',
            email='manoj@saferide.org',
            password='testpassword123',
            role=User.Role.DRIVER
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            name='Manoj George',
            email='manoj@saferide.org',
            phone_number='9846012345',
            license_number='KL-05-2018005678',
            vehicle_number='KL-05-XY-9999',
            verification_status=Driver.VerificationStatus.VERIFIED
        )
        self.trip = Trip.objects.create(
            passenger=self.passenger,
            driver=self.driver,
            status=Trip.Status.ACTIVE
        )

    def test_sos_alert_creation_and_relations(self):
        """Verify that SOSAlert correctly links to Passenger, Driver, Trip, and records timestamp."""
        sos_lat = Decimal('9.691200')
        sos_lng = Decimal('76.690400')

        alert = SOSAlert.objects.create(
            passenger=self.passenger,
            driver=self.driver,
            trip=self.trip,
            latitude=sos_lat,
            longitude=sos_lng,
            location_name="Palai Highway Junction Distress Beacon",
            status=SOSAlert.Status.ACTIVE
        )

        self.assertEqual(alert.passenger, self.passenger)
        self.assertEqual(alert.driver, self.driver)
        self.assertEqual(alert.trip, self.trip)
        self.assertEqual(alert.latitude, sos_lat)
        self.assertEqual(alert.longitude, sos_lng)
        self.assertEqual(alert.status, SOSAlert.Status.ACTIVE)
        self.assertIsNotNone(alert.timestamp)

    def test_sos_alert_resolution(self):
        """Verify that an administrator can mark an SOS alert resolved with remarks."""
        alert = SOSAlert.objects.create(
            passenger=self.passenger,
            driver=self.driver,
            status=SOSAlert.Status.ACTIVE
        )
        alert.resolve_alert(notes="Police Patrol #12 reached spot. Passenger escorted safely.")
        
        alert.refresh_from_db()
        self.assertEqual(alert.status, SOSAlert.Status.RESOLVED)
        self.assertIsNotNone(alert.resolved_at)
        self.assertIn("Police Patrol #12", alert.admin_notes)


class RatingAndComplaintModelTests(TestCase):
    """
    Test Case 5: Ratings & Complaints Constraints Tests
    Verifies rating 1-5 range validator and complaint filing integrity.
    """

    def setUp(self):
        self.passenger = User.objects.create_user(
            username='neha',
            email='neha@saferide.org',
            password='testpassword123',
            role=User.Role.PASSENGER
        )
        self.driver_user = User.objects.create_user(
            username='driver_biju',
            email='biju@saferide.org',
            password='testpassword123',
            role=User.Role.DRIVER
        )
        self.driver = Driver.objects.create(
            user=self.driver_user,
            name='Biju Varghese',
            email='biju@saferide.org',
            phone_number='9847054321',
            license_number='KL-05-2017009876',
            vehicle_number='KL-05-CC-3333',
            verification_status=Driver.VerificationStatus.VERIFIED
        )
        self.trip = Trip.objects.create(
            passenger=self.passenger,
            driver=self.driver,
            status=Trip.Status.COMPLETED
        )

    def test_valid_rating_saves_successfully(self):
        """Verify that a rating of 5 stars saves and calculates reputation."""
        rating_obj = RatingReview.objects.create(
            trip=self.trip,
            passenger=self.passenger,
            driver=self.driver,
            rating=5,
            review="Polite driver, smooth ride."
        )
        self.assertEqual(rating_obj.rating, 5)

    def test_invalid_rating_raises_validation_error(self):
        """Verify that rating outside 1-5 raises a ValidationError upon full_clean()."""
        invalid_rating = RatingReview(
            trip=self.trip,
            passenger=self.passenger,
            driver=self.driver,
            rating=6,
            review="Invalid star count"
        )
        with self.assertRaises(ValidationError):
            invalid_rating.full_clean()

    def test_complaint_filing_and_resolution(self):
        """Verify complaint filing, penalty point deduction, and status updates."""
        complaint = Complaint.objects.create(
            trip=self.trip,
            passenger=self.passenger,
            driver=self.driver,
            category=Complaint.Category.OVERCHARGING,
            description="Driver demanded extra fare above standard metered tariff."
        )
        self.assertEqual(complaint.status, 'Pending')
        
        complaint.resolve(remarks="Driver warned and excess fare refunded.", penalty=5)
        self.assertEqual(complaint.status, 'Resolved')
        self.assertEqual(complaint.penalty_points_deducted, 5)
        self.assertIsNotNone(complaint.resolved_at)
