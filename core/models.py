import uuid
import math
import qrcode
from io import BytesIO
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

# Standardized Database & Model-Level Regex Validators
PHONE_VALIDATOR = RegexValidator(
    regex=r"^(\+91[\-\s]?)?[6-9]\d{9}$",
    message="Phone number must be a valid 10-digit mobile number."
)

VEHICLE_PLATE_VALIDATOR = RegexValidator(
    regex=r"^[A-Za-z]{2}[-\s]?[0-9]{1,2}[-\s]?[A-Za-z]{1,3}[-\s]?[0-9]{4}$",
    message="Vehicle number must follow standard license plate format (e.g. KL-05-AT-4455 or DL-01-A-1234)."
)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'System Administrator'
        DRIVER = 'DRIVER', 'Registered Driver'
        PASSENGER = 'PASSENGER', 'Passenger'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PASSENGER)
    phone = models.CharField(max_length=20, blank=True, null=True, validators=[PHONE_VALIDATOR])
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_user'

    def is_admin_user(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_driver_user(self):
        return self.role == self.Role.DRIVER

    def is_passenger_user(self):
        return self.role == self.Role.PASSENGER

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class Admin(models.Model):
    """
    Table 3: tbl_admin
    Stores system administrator records matching Table Design Specification.
    """
    admin_id = models.AutoField(primary_key=True, db_column='admin_id')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile', null=True, blank=True)
    name = models.CharField(max_length=50, db_column='name')
    email = models.CharField(max_length=50, unique=True, db_column='email')
    password = models.CharField(max_length=255, db_column='password')

    class Meta:
        db_table = 'tbl_admin'
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.name or (self.user.get_full_name() or self.user.username)
            self.email = self.email or self.user.email
            self.password = self.password or self.user.password
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Admin: {self.name} ({self.email})"


class Passenger(models.Model):
    """
    Table 1: tbl_passenger
    Stores passenger profiles matching Table Design Specification.
    """
    passenger_id = models.AutoField(primary_key=True, db_column='passenger_id')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passenger_profile')
    name = models.CharField(max_length=50, db_column='name')
    email = models.CharField(max_length=50, unique=True, db_column='email')
    phone_number = models.CharField(max_length=20, unique=True, db_column='phone_number', validators=[PHONE_VALIDATOR])
    password = models.CharField(max_length=255, db_column='password')
    created_at = models.DateTimeField(default=timezone.now, db_column='created_at')

    # Primary Emergency Contact (Contact 1)
    emergency_contact_name = models.CharField(max_length=50, blank=True, null=True, db_column='emergency_contact_name')
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True, db_column='emergency_contact_phone', validators=[PHONE_VALIDATOR])
    emergency_contact_relation = models.CharField(max_length=50, blank=True, null=True, default="Family", db_column='emergency_contact_relation')

    # Secondary Emergency Contact (Contact 2 - Extra)
    emergency_contact_2_name = models.CharField(max_length=50, blank=True, null=True, db_column='emergency_contact_2_name')
    emergency_contact_2_phone = models.CharField(max_length=20, blank=True, null=True, db_column='emergency_contact_2_phone', validators=[PHONE_VALIDATOR])
    emergency_contact_2_relation = models.CharField(max_length=50, blank=True, null=True, default="Friend", db_column='emergency_contact_2_relation')

    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        db_table = 'tbl_passenger'
        verbose_name = 'Passenger'
        verbose_name_plural = 'Passengers'

    # Compatibility properties for emergency contact 1
    @property
    def emergency_contact_1_name(self):
        return self.emergency_contact_name

    @emergency_contact_1_name.setter
    def emergency_contact_1_name(self, value):
        self.emergency_contact_name = value

    @property
    def emergency_contact_1_phone(self):
        return self.emergency_contact_phone

    @emergency_contact_1_phone.setter
    def emergency_contact_1_phone(self, value):
        self.emergency_contact_phone = value

    @property
    def emergency_contact_1_relation(self):
        return self.emergency_contact_relation

    @emergency_contact_1_relation.setter
    def emergency_contact_1_relation(self, value):
        self.emergency_contact_relation = value

    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.name or (self.user.get_full_name() or self.user.username)
            self.email = self.email or self.user.email
            self.phone_number = self.phone_number or (self.user.phone or '')
            self.password = self.password or self.user.password
        super().save(*args, **kwargs)

    @property
    def id(self):
        return self.passenger_id

    def __str__(self):
        return f"Passenger: {self.name} ({self.phone_number})"


class Driver(models.Model):
    """
    Table 2: tbl_driver
    Stores driver records and vehicle attributes matching Table Design Specification.
    """
    class VerificationStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        VERIFIED = 'Verified', 'Verified'
        SUSPENDED = 'Suspended', 'Suspended'
        REJECTED = 'Rejected', 'Rejected'

    driver_id = models.AutoField(primary_key=True, db_column='driver_id')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    name = models.CharField(max_length=50, db_column='name')
    phone_number = models.CharField(max_length=20, unique=True, db_column='phone_number', validators=[PHONE_VALIDATOR])
    email = models.CharField(max_length=50, unique=True, db_column='email')
    license_number = models.CharField(max_length=30, unique=True, db_column='license_number')
    vehicle_number = models.CharField(max_length=30, unique=True, db_column='vehicle_number', validators=[VEHICLE_PLATE_VALIDATOR])
    vehicle_type = models.CharField(max_length=20, default='auto', db_column='vehicle_type')
    verification_status = models.CharField(
        max_length=15, 
        choices=VerificationStatus.choices, 
        default=VerificationStatus.PENDING,
        db_column='verification_status'
    )
    qr_code = models.CharField(max_length=255, blank=True, null=True, db_column='qr_code')
    password = models.CharField(max_length=255, db_column='password')

    # Additional Safety & Verification metadata
    experience_years = models.PositiveIntegerField(default=1)
    verification_notes = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reputation_score = models.FloatField(default=85.0, help_text="Dynamic safety score (0 to 100)")
    total_trips = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=5.0)

    # Document & Photo Uploads
    driver_photo = models.ImageField(upload_to='driver_photos/', blank=True, null=True)
    license_doc = models.FileField(upload_to='driver_docs/license/', blank=True, null=True)
    id_proof_doc = models.FileField(upload_to='driver_docs/id_proof/', blank=True, null=True)
    police_clearance_doc = models.FileField(upload_to='driver_docs/police_clearance/', blank=True, null=True)
    qr_code_image = models.ImageField(upload_to='driver_qrcodes/', blank=True, null=True)

    class Meta:
        db_table = 'tbl_driver'
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    @property
    def id(self):
        return self.driver_id

    @property
    def qr_code_url(self):
        """Returns the public URL of the driver QR code image."""
        if self.qr_code_image and hasattr(self.qr_code_image, 'name') and self.qr_code_image.name:
            try:
                return self.qr_code_image.url
            except Exception:
                pass
        if self.qr_code:
            val = str(self.qr_code)
            if val.startswith('http://') or val.startswith('https://') or val.startswith('/'):
                return val
            return f"/media/{val}"
            
        # Fallback to dynamic QR generation using public tunnel if available
        base_url = "http://127.0.0.1:8000"
        try:
            from django.conf import settings
            tunnel_file = settings.BASE_DIR / '.tunnel_url'
            if tunnel_file.exists():
                with open(tunnel_file, 'r', encoding='utf-8') as f:
                    saved_url = f.read().strip()
                    if saved_url.startswith('http'):
                        base_url = saved_url.rstrip('/')
        except Exception:
            pass
            
        import urllib.parse
        encoded_url = urllib.parse.quote(f"{base_url}/verify/{self.verification_token}/")
        return f"https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={encoded_url}"

    def is_verified(self):
        return self.verification_status in [self.VerificationStatus.VERIFIED, 'VERIFIED', 'Verified']

    def generate_qr_code(self, base_url="http://127.0.0.1:8000"):
        """Generates and saves a QR code encoding the driver's public verification URL."""
        from django.core.files.storage import default_storage
        
        # Always enforce public tunnel URL if available to prevent localhost scanning failures
        try:
            from django.conf import settings
            tunnel_file = settings.BASE_DIR / '.tunnel_url'
            if tunnel_file.exists():
                with open(tunnel_file, 'r', encoding='utf-8') as f:
                    saved_url = f.read().strip()
                    if saved_url.startswith('http'):
                        base_url = saved_url.rstrip('/')
        except Exception:
            pass
            
        verify_url = f"{base_url}/verify/{self.verification_token}/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3,
        )
        qr.add_data(verify_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1A365D", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer)
        
        # Delete old file referenced by the instance if it exists
        if self.qr_code_image and self.qr_code_image.name:
            try:
                if default_storage.exists(self.qr_code_image.name):
                    default_storage.delete(self.qr_code_image.name)
            except Exception:
                pass

        import time
        timestamp = int(time.time())
        filename = f"qr_{self.license_number.replace(' ', '_')}_{self.driver_id or self.pk or 'tmp'}_{timestamp}.png"
        target_path = f"driver_qrcodes/{filename}"
        
        # Remove any existing file with target name to prevent Django appending random hashes
        if default_storage.exists(target_path):
            try:
                default_storage.delete(target_path)
            except Exception:
                pass

        self.qr_code_image.save(filename, ContentFile(buffer.getvalue()), save=False)
        self.qr_code = self.qr_code_image.url if hasattr(self.qr_code_image, 'url') else f"/media/driver_qrcodes/{filename}"
        return self.qr_code

    def recalculate_reputation(self):
        """Calculates dynamic reputation score based on ratings, verification, and complaints."""
        ratings = self.received_ratings.all()
        complaints = self.complaints.filter(status__in=['Pending', 'OPEN', 'INVESTIGATING', 'RESOLVED'])
        
        if ratings.exists():
            avg_stars = sum(r.rating for r in ratings) / ratings.count()
            self.average_rating = round(avg_stars, 2)
        else:
            avg_stars = 4.5
            self.average_rating = 4.5

        rating_component = (avg_stars / 5.0) * 70.0
        verification_bonus = 15.0 if self.is_verified() else 0.0
        trip_bonus = min(15.0, (self.total_trips * 0.5))
        penalty_deduction = sum(getattr(c, 'penalty_points_deducted', 5) for c in complaints)
        
        final_score = rating_component + verification_bonus + trip_bonus - penalty_deduction
        self.reputation_score = max(10.0, min(100.0, round(final_score, 1)))
        self.save()

    def get_vehicle_type_display(self):
        vt = str(self.vehicle_type or '').lower()
        if 'auto' in vt:
            return 'Auto-Rickshaw'
        elif 'taxi' in vt:
            return 'Local Taxi'
        elif 'cab' in vt:
            return 'Sedan / Hatchback Cab'
        return self.vehicle_type.title() if self.vehicle_type else 'Auto-Rickshaw'

    def get_verification_status_display(self):
        return self.verification_status

    @property
    def vehicle(self):
        class VehicleProxy:
            def __init__(self, driver):
                self.driver = driver
                self.registration_number = driver.vehicle_number
                self.vehicle_type = driver.vehicle_type
                if 'auto' in str(driver.vehicle_type).lower():
                    self.make_model = "Bajaj Compact RE"
                elif 'taxi' in str(driver.vehicle_type).lower():
                    self.make_model = "Maruti Suzuki Dzire"
                elif 'cab' in str(driver.vehicle_type).lower():
                    self.make_model = "Toyota Etios / Swift"
                else:
                    self.make_model = "Commercial Vehicle"
                self.color = "Yellow & Black" if "auto" in str(driver.vehicle_type).lower() else "White / Silver"
                self.seating_capacity = 3 if "auto" in str(driver.vehicle_type).lower() else 4
                self.rc_book_doc = None
                self.vehicle_photo = None
                
            def get_vehicle_type_display(self):
                return self.driver.get_vehicle_type_display()
                
            def clean_reg_number(self):
                return self.registration_number.upper().replace(" ", "").replace("-", "") if self.registration_number else ""
                
            def __str__(self):
                return f"{self.registration_number} ({self.get_vehicle_type_display()})"
        return VehicleProxy(self)

    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.name or (self.user.get_full_name() or self.user.username)
            self.email = self.email or self.user.email
            self.phone_number = self.phone_number or (self.user.phone or '')
            self.password = self.password or self.user.password

        # Automatically generate QR code and set verified_at timestamp when status is set to Verified
        if self.is_verified():
            if not self.verified_at:
                self.verified_at = timezone.now()
            if not self.qr_code_image or not self.qr_code:
                try:
                    self.generate_qr_code()
                except Exception:
                    pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Lic: {self.license_number}, Veh: {self.vehicle_number})"


class VehicleDocuments(models.Model):
    """
    Table 4: tbl_vehicle_documents
    Stores vehicle and driver license / RC documents matching Table Design Specification.
    """
    document_id = models.AutoField(primary_key=True, db_column='document_id')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='documents', db_column='driver_id')
    license_doc = models.CharField(max_length=255, db_column='license_doc', default='')
    rc_doc = models.CharField(max_length=255, db_column='rc_doc', default='')
    uploaded_at = models.DateTimeField(default=timezone.now, db_column='uploaded_at')

    # Media File Fields
    license_file = models.FileField(upload_to='driver_docs/license/', blank=True, null=True)
    rc_file = models.FileField(upload_to='vehicle_docs/rc/', blank=True, null=True)

    class Meta:
        db_table = 'tbl_vehicle_documents'
        verbose_name = 'Vehicle Document'
        verbose_name_plural = 'Vehicle Documents'

    @property
    def id(self):
        return self.document_id

    def __str__(self):
        return f"Document #{self.document_id} for Driver {self.driver.name}"


class Trip(models.Model):
    """
    Table 5: tbl_trip
    Stores safe journey sessions recording boarding & destination telemetry.
    """
    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        COMPLETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'
        SOS_TRIGGERED = 'SOS_Triggered', 'SOS Emergency Triggered'

    IN_PROGRESS = Status.ACTIVE
    ONGOING = Status.ACTIVE

    trip_id = models.AutoField(primary_key=True, db_column='trip_id')
    trip_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips_as_passenger', db_column='passenger_id')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips_as_driver', db_column='driver_id')
    
    # 2. Boarding & Destination Coordinates (Crucial for Map Integration)
    boarding_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=9.684300)
    boarding_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=76.685300)
    boarding_address = models.CharField(max_length=255, default="Current Boarding Point", blank=True)

    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    destination_address = models.CharField(max_length=255, blank=True, null=True)

    # 3. Trip Status & Timestamps
    start_time = models.DateTimeField(default=timezone.now, db_column='start_time')
    end_time = models.DateTimeField(blank=True, null=True, db_column='end_time')
    status = models.CharField(max_length=20, default='Active', choices=Status.choices, db_column='status')

    # 4. Live Tracking Fields (continuous GPS pings via AJAX)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=9.684300)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=76.685300)
    live_updated_at = models.DateTimeField(auto_now=True)
    share_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # 5. Fare Calculation & Safety Tracking Fields (Table 5 Extension)
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, db_column='distance_km', help_text="Total distance travelled in kilometers")
    fare_amount = models.DecimalField(max_digits=8, decimal_places=2, default=30.00, db_column='fare_amount', help_text="Calculated fare in INR")
    live_location_sharing = models.BooleanField(default=True, db_column='live_location_sharing', help_text="Whether passenger enabled live GPS tracking sharing")
    fare_qr_code = models.ImageField(upload_to='fare_qrcodes/', blank=True, null=True, db_column='fare_qr_code', help_text="Digital QR Code for fare receipt and UPI settlement")

    # Legacy & Compatibility Aliases for DB columns and templates
    start_location = models.CharField(max_length=255, default="Current Boarding Point", blank=True, null=True, db_column='start_location')
    end_location = models.CharField(max_length=255, blank=True, null=True, db_column='end_location')
    pickup_location_name = models.CharField(max_length=255, default="Current Location")
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=9.684300)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=76.685300)
    drop_location_name = models.CharField(max_length=255, blank=True, null=True)
    drop_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    drop_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    live_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=9.684300)
    live_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=76.685300)

    class Meta:
        db_table = 'tbl_trip'
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'

    @property
    def id(self):
        return self.trip_id

    def save(self, *args, **kwargs):
        # Synchronize boarding & destination coordinates with legacy aliases
        if not self.start_location and self.boarding_address:
            self.start_location = self.boarding_address
        elif not self.boarding_address and self.start_location:
            self.boarding_address = self.start_location

        if not self.end_location and self.destination_address:
            self.end_location = self.destination_address
        elif not self.destination_address and self.end_location:
            self.destination_address = self.end_location

        if self.boarding_latitude:
            self.pickup_latitude = self.boarding_latitude
        if self.boarding_longitude:
            self.pickup_longitude = self.boarding_longitude

        if self.current_latitude:
            self.live_latitude = self.current_latitude
        elif self.live_latitude:
            self.current_latitude = self.live_latitude

        if self.current_longitude:
            self.live_longitude = self.current_longitude
        elif self.live_longitude:
            self.current_longitude = self.live_longitude

        if self.destination_latitude:
            self.drop_latitude = self.destination_latitude
        if self.destination_longitude:
            self.drop_longitude = self.destination_longitude

        super().save(*args, **kwargs)

    @property
    def boarding_point(self):
        return self.boarding_address or self.start_location or self.pickup_location_name or "Boarding Point"

    @property
    def destination_point(self):
        val = self.destination_address or self.end_location or self.drop_location_name
        if val and str(val).strip() and str(val).strip().lower() not in [
            'destination point', 'destination drop point', 'destination', 'none', 'null', '', 'open / metered', 'open / metered destination'
        ]:
            return str(val).strip()
        # Fallback to recorded drop coordinates if available
        lat = self.destination_latitude or self.drop_latitude or (self.current_latitude if self.status in ['Completed', 'COMPLETED'] else None)
        lng = self.destination_longitude or self.drop_longitude or (self.current_longitude if self.status in ['Completed', 'COMPLETED'] else None)
        if lat and lng:
            return f"Drop Point ({round(float(lat), 4)}, {round(float(lng), 4)})"
        return None

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two GPS coordinates using the Haversine formula (in km)."""
        R = 6371  # Earth's radius in kilometers
        lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        return round(R * c, 2)

    def calculate_distance_and_fare(self):
        """Calculate distance (Haversine) and legally valid government metered tariff."""
        from decimal import Decimal, ROUND_HALF_UP

        # Determine vehicle-specific tariff parameters
        v_type = 'auto'
        if hasattr(self, 'driver') and self.driver:
            v_type = str(getattr(self.driver, 'vehicle_type', 'auto') or 'auto').lower()

        if 'taxi' in v_type or 'cab' in v_type or 'van' in v_type:
            # Regulated Taxi / Cab tariff structure (Minimum fare for first 5 km)
            BASE_DISTANCE = Decimal('5.00')
            BASE_FARE = Decimal('200.00')
            PER_KM_RATE = Decimal('18.00')
        else:
            # Kerala MVD Regulated Auto-Rickshaw Tariff (₹30 for first 1.5 km, ₹15/km thereafter)
            BASE_DISTANCE = Decimal('1.50')
            BASE_FARE = Decimal('30.00')
            PER_KM_RATE = Decimal('15.00')

        # Calculate distance based on destination coordinates or live GPS coordinates
        target_lat = self.destination_latitude or self.drop_latitude
        target_lng = self.destination_longitude or self.drop_longitude

        dest_dist = self.haversine_distance(
            self.boarding_latitude, self.boarding_longitude,
            target_lat, target_lng
        ) if (target_lat and target_lng) else 0.0

        live_dist = self.haversine_distance(
            self.boarding_latitude, self.boarding_longitude,
            self.current_latitude, self.current_longitude
        )

        distance = max(dest_dist, live_dist)
        self.distance_km = Decimal(str(distance)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if self.distance_km <= BASE_DISTANCE:
            self.fare_amount = BASE_FARE
        else:
            additional_km = self.distance_km - BASE_DISTANCE
            self.fare_amount = (BASE_FARE + (additional_km * PER_KM_RATE)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return self.distance_km, self.fare_amount

    def generate_fare_qr_code(self, base_url="http://127.0.0.1:8000"):
        """Generate a QR code containing fare receipt & UPI payment details for the completed trip."""
        import qrcode
        from io import BytesIO
        from django.core.files.base import ContentFile
        from django.core.files.storage import default_storage

        # Always enforce public tunnel URL if available to prevent localhost scanning failures
        try:
            from django.conf import settings
            tunnel_file = settings.BASE_DIR / '.tunnel_url'
            if tunnel_file.exists():
                with open(tunnel_file, 'r', encoding='utf-8') as f:
                    saved_url = f.read().strip()
                    if saved_url.startswith('http'):
                        base_url = saved_url.rstrip('/')
        except Exception:
            pass

        # Formatted digital receipt & UPI payment string
        from urllib.parse import quote
        payee_name = quote(self.driver.name or 'SafeRide Driver')
        upi_pay_str = f"upi://pay?pa=saferide@upi&pn={payee_name}&am={self.fare_amount}&cu=INR&tn=SafeRide_TRP_{self.trip_id}"
        receipt_text = (
            f"SafeRide Verified Fare Receipt\n"
            f"Trip ID: #TRP-{str(self.trip_id).zfill(4)}\n"
            f"Passenger: {self.passenger.get_full_name() or self.passenger.username}\n"
            f"Driver: {self.driver.name or self.driver.user.get_full_name()}\n"
            f"Vehicle: {self.driver.vehicle_number}\n"
            f"Distance: {self.distance_km} km\n"
            f"Total Fare: INR {self.fare_amount}\n"
            f"Date: {self.start_time.strftime('%d-%m-%Y %I:%M %p') if self.start_time else 'N/A'}\n"
            f"UPI Pay: {upi_pay_str}\n"
            f"Verify: {base_url}/verify/{self.driver.verification_token}/"
        )

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        # To launch payment apps correctly, the QR payload must strictly be the UPI URI, not plain text.
        qr.add_data(upi_pay_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0F172A", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f"fare_qr_trip_{self.trip_id}.png"

        if self.fare_qr_code and self.fare_qr_code.name:
            try:
                if default_storage.exists(self.fare_qr_code.name):
                    default_storage.delete(self.fare_qr_code.name)
            except Exception:
                pass

        self.fare_qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
        return self.fare_qr_code

    def complete_trip(self, end_lat=None, end_lng=None, end_address=None):
        self.status = 'Completed'
        self.end_time = timezone.now()

        # Update final drop coordinates if provided
        if end_lat is not None and end_lng is not None:
            try:
                from decimal import Decimal
                d_lat = Decimal(str(round(float(end_lat), 6)))
                d_lng = Decimal(str(round(float(end_lng), 6)))
                self.current_latitude = d_lat
                self.current_longitude = d_lng
                self.live_latitude = d_lat
                self.live_longitude = d_lng
                if not self.destination_latitude:
                    self.destination_latitude = d_lat
                if not self.destination_longitude:
                    self.destination_longitude = d_lng
                if not self.drop_latitude:
                    self.drop_latitude = d_lat
                if not self.drop_longitude:
                    self.drop_longitude = d_lng
            except (ValueError, TypeError):
                pass

        # Update destination address if captured at completion
        if end_address and str(end_address).strip():
            clean_addr = str(end_address).strip()
            if not self.destination_address or str(self.destination_address).strip().lower() in [
                'open / metered', 'open / metered destination', 'destination drop point', 'none', 'null', ''
            ]:
                self.destination_address = clean_addr
            self.end_location = self.destination_address
            self.drop_location_name = self.destination_address
        elif not self.destination_address or str(self.destination_address).strip().lower() in [
            'open / metered', 'open / metered destination', 'none', 'null', ''
        ]:
            lat = self.destination_latitude or self.drop_latitude or self.current_latitude
            lng = self.destination_longitude or self.drop_longitude or self.current_longitude
            if lat and lng:
                drop_label = f"Drop Point ({round(float(lat), 4)}, {round(float(lng), 4)})"
                self.destination_address = drop_label
                self.end_location = drop_label
                self.drop_location_name = drop_label
        self.calculate_distance_and_fare()
        try:
            self.generate_fare_qr_code()
        except Exception as e:
            print(f"Error generating fare QR code: {e}")
        self.save()
        self.driver.total_trips += 1
        self.driver.save()
        self.driver.recalculate_reputation()

    def __str__(self):
        return f"Trip #{self.trip_id} - {self.passenger.username} with {self.driver.name}"


class RatingReview(models.Model):
    """
    Table 6: tbl_rating_review
    Stores passenger ratings and reviews for trips matching Table Design Specification.
    """
    rating_id = models.AutoField(primary_key=True, db_column='rating_id')
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name='rating_entry', db_column='trip_id')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings', db_column='passenger_id')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='received_ratings', db_column='driver_id')
    rating = models.PositiveSmallIntegerField(
        default=5, 
        db_column='rating', 
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Range 1-5"
    )
    review = models.TextField(blank=True, null=True, db_column='review')
    created_at = models.DateTimeField(default=timezone.now, db_column='created_at')

    class Meta:
        db_table = 'tbl_rating_review'
        verbose_name = 'Rating & Review'
        verbose_name_plural = 'Ratings & Reviews'

    @property
    def id(self):
        return self.rating_id

    @property
    def review_text(self):
        return self.review

    @review_text.setter
    def review_text(self, value):
        self.review = value

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.driver.recalculate_reputation()

    def __str__(self):
        return f"{self.rating}★ by {self.passenger.username} for {self.driver.name}"


class Complaint(models.Model):
    """
    Table 7: tbl_complaint
    Stores passenger grievances matching Table Design Specification.
    """
    class Category(models.TextChoices):
        OVERCHARGING = 'OVERCHARGING', 'Overcharging / Unmetered Fare'
        RECKLESS_DRIVING = 'RECKLESS_DRIVING', 'Reckless or Dangerous Driving'
        MISBEHAVIOR = 'MISBEHAVIOR', 'Rude Behavior / Verbal Abuse'
        HARASSMENT = 'HARASSMENT', 'Harassment / Safety Threat'
        ROUTE_DEVIATION = 'ROUTE_DEVIATION', 'Unauthorized Route Deviation'
        REFUSAL_TO_COMMUTE = 'REFUSAL', 'Refusal to Commute / Drop'
        OTHER = 'OTHER', 'Other Safety Issue'

    class Status(models.TextChoices):
        OPEN = 'Pending', 'Pending'
        INVESTIGATING = 'Investigating', 'Investigating'
        RESOLVED = 'Resolved', 'Resolved'
        DISMISSED = 'Dismissed', 'Dismissed'

    complaint_id = models.AutoField(primary_key=True, db_column='complaint_id')
    complaint_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, blank=True, null=True, related_name='complaints', db_column='trip_id')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='filed_complaints', db_column='passenger_id')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='complaints', db_column='driver_id')
    description = models.TextField(db_column='description')
    status = models.CharField(max_length=15, default='Pending', db_column='status')
    created_at = models.DateTimeField(default=timezone.now, db_column='created_at')

    # Category & Resolution tracking
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.MISBEHAVIOR)
    evidence_photo = models.ImageField(upload_to='complaint_evidence/', blank=True, null=True)
    admin_remarks = models.TextField(blank=True, null=True)
    penalty_points_deducted = models.IntegerField(default=5)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_complaint'
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

    @property
    def id(self):
        return self.complaint_id

    def resolve(self, remarks="", penalty=5, dismiss=False):
        if dismiss:
            self.status = 'Dismissed'
            self.penalty_points_deducted = 0
        else:
            self.status = 'Resolved'
            self.penalty_points_deducted = penalty
            
        self.admin_remarks = remarks
        self.resolved_at = timezone.now()
        self.save()
        self.driver.recalculate_reputation()

    def __str__(self):
        return f"Complaint #{self.complaint_id} ({self.status}) against {self.driver.name}"


class SOSAlert(models.Model):
    """
    Table 8: tbl_sos_alert
    Stores real-time emergency distress events matching Table Design Specification.
    """
    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        RESPONDED = 'Responded', 'Responded'
        RESOLVED = 'Resolved', 'Resolved'

    sos_id = models.AutoField(primary_key=True, db_column='sos_id')
    alert_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sos_alerts', db_column='passenger_id')
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, blank=True, null=True, related_name='sos_events', db_column='trip_id')
    location = models.CharField(max_length=100, default="Live GPS Distress Location", db_column='location')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True, related_name='sos_incidents', db_column='driver_id')
    timestamp = models.DateTimeField(default=timezone.now, db_column='timestamp')
    status = models.CharField(max_length=15, default='Active', db_column='status')

    # GPS Coordinates & Emergency Units Dispatched (Fixed Precision 6 Decimal Places ~0.11m accuracy)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=9.684300)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=76.685300)
    location_name = models.CharField(max_length=255, default="Live GPS Distress Location")
    admin_notes = models.TextField(blank=True, null=True)
    dispatched_services = models.CharField(max_length=255, default="Local Police (112) & Emergency Contacts")
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_sos_alert'
        verbose_name = 'SOS Alert'
        verbose_name_plural = 'SOS Alerts'

    @property
    def id(self):
        return self.sos_id

    @property
    def alert_id(self):
        return self.sos_id

    @property
    def created_at(self):
        return self.timestamp

    @property
    def vehicle_number(self):
        if self.driver and self.driver.vehicle_number:
            return self.driver.vehicle_number
        if self.trip and self.trip.driver and self.trip.driver.vehicle_number:
            return self.trip.driver.vehicle_number
        return "N/A (Direct Emergency Beacon)"

    @property
    def driver_name(self):
        if self.driver:
            return self.driver.name or self.driver.user.username
        if self.trip and self.trip.driver:
            return self.trip.driver.name or self.trip.driver.user.username
        return "Direct SOS (No active trip assigned)"

    def resolve_alert(self, notes=""):
        self.status = 'Resolved'
        self.admin_notes = notes
        self.resolved_at = timezone.now()
        self.save()

    def __str__(self):
        return f"🚨 SOS Alert #{self.sos_id} by {self.passenger.username} at {self.timestamp.strftime('%H:%M:%S')}"


class IncidentReport(models.Model):
    """
    Table 9: tbl_incident_report
    Stores passenger incident reporting records matching Table Design Specification.
    """
    class IncidentType(models.TextChoices):
        ACCIDENT = 'Accident', 'Accident'
        HARASSMENT = 'Harassment', 'Harassment'
        UNSAFE_DRIVING = 'Unsafe Driving', 'Unsafe Driving'
        OTHER = 'Other', 'Other'

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        INVESTIGATING = 'Investigating', 'Investigating'
        RESOLVED = 'Resolved', 'Resolved'

    incident_id = models.AutoField(primary_key=True, db_column='incident_id')
    incident_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incident_reports', db_column='passenger_id')
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, blank=True, null=True, related_name='incident_reports', db_column='trip_id')
    incident_type = models.CharField(max_length=30, default='Unsafe Driving', db_column='incident_type')
    description = models.TextField(db_column='description')
    status = models.CharField(max_length=15, default='Pending', db_column='status')
    reported_at = models.DateTimeField(default=timezone.now, db_column='reported_at')

    class Meta:
        db_table = 'tbl_incident_report'
        verbose_name = 'Incident Report'
        verbose_name_plural = 'Incident Reports'

    @property
    def id(self):
        return self.incident_id

    def __str__(self):
        return f"Incident #{self.incident_id} ({self.incident_type}) by {self.passenger.username}"


# ==========================================================
# BACKWARD-COMPATIBILITY ALIASES & PROXIES
# ==========================================================
PassengerProfile = Passenger
DriverProfile = Driver
Vehicle = VehicleDocuments
VehicleDetails = VehicleDocuments
TripSession = Trip
TripRating = RatingReview
