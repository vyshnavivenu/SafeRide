import re
from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, Passenger, Driver, VehicleDocuments, RatingReview, Complaint, IncidentReport
)

# Standardized Regex Validators
NAME_REGEX = r"^[a-zA-Z\s\.\'\-]+$"
PHONE_REGEX = r"^(\+91[\-\s]?)?[6-9]\d{9}$"
VEHICLE_PLATE_REGEX = r"^[A-Za-z]{2}[-\s]?[0-9]{1,2}[-\s]?[A-Za-z]{1,3}[-\s]?[0-9]{4}$"
LICENSE_REGEX = r"^[A-Za-z]{2}[-\s]?[0-9A-Za-z\s\/\-]{6,20}$"

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 Megabytes
ALLOWED_KYC_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.webp']

def validate_kyc_document(file_obj, label="Document"):
    """Validates that uploaded KYC file is strictly a PDF/image and does not exceed 5MB."""
    if not file_obj:
        return file_obj
    
    if hasattr(file_obj, 'size') and file_obj.size > MAX_FILE_SIZE_BYTES:
        size_mb = round(file_obj.size / (1024 * 1024), 2)
        raise forms.ValidationError(f"{label} file size exceeds the 5MB limit ({size_mb}MB uploaded). Please compress your file.")
    
    import os
    if hasattr(file_obj, 'name') and file_obj.name:
        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext not in ALLOWED_KYC_EXTENSIONS:
            raise forms.ValidationError(f"{label} must be a valid PDF document or standard image (.pdf, .jpg, .jpeg, .png, .webp).")
    return file_obj

name_validator = RegexValidator(
    regex=NAME_REGEX,
    message="Name must contain only alphabetic characters, spaces, dots, or hyphens."
)

phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message="Enter a valid 10-digit Indian mobile number (e.g. 9876543210 or +91 9876543210)."
)

vehicle_plate_validator = RegexValidator(
    regex=VEHICLE_PLATE_REGEX,
    message="Enter a valid vehicle plate format (e.g. KL-05-AT-4455 or DL-01-A-1234)."
)

license_validator = RegexValidator(
    regex=LICENSE_REGEX,
    message="Enter a valid driving license format (e.g. KL-05-2021000892)."
)


class PassengerRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, 
        min_length=2,
        required=True, 
        validators=[name_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'First Name',
            'pattern': NAME_REGEX,
            'title': 'Letters and spaces only'
        })
    )
    last_name = forms.CharField(
        max_length=50, 
        min_length=1,
        required=True, 
        validators=[name_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Last Name',
            'pattern': NAME_REGEX,
            'title': 'Letters and spaces only'
        })
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    phone = forms.CharField(
        max_length=20, 
        required=True, 
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'type': 'tel',
            'placeholder': 'Phone Number (e.g. 9876543210 or +91 9876543210)',
            'pattern': r'(\+91[\-\s]?)?[6-9]\d{9}'
        })
    )
    
    emergency_contact_1_name = forms.CharField(
        max_length=100, 
        required=False, 
        validators=[name_validator],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Name (Optional)'})
    )
    emergency_contact_1_phone = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': 'Emergency Contact Phone (Optional)'})
    )
    emergency_contact_1_relation = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship (e.g. Parent, Guardian)'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a Username'}),
        }

    def clean_first_name(self):
        fn = self.cleaned_data.get('first_name', '').strip()
        if not re.match(NAME_REGEX, fn):
            raise forms.ValidationError("First name must contain only letters and spaces.")
        if len(fn) < 2:
            raise forms.ValidationError("First name must be at least 2 characters.")
        return fn

    def clean_last_name(self):
        ln = self.cleaned_data.get('last_name', '').strip()
        if not re.match(NAME_REGEX, ln):
            raise forms.ValidationError("Last name must contain only letters and spaces.")
        return ln

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise forms.ValidationError("Email address is required.")
        if Passenger.objects.filter(email__iexact=email).exists() or User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A passenger account with this email address is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 12 and digits.startswith('91'):
            digits = digits[2:]
        if len(digits) != 10 or not digits[0] in '6789':
            raise forms.ValidationError("Please enter a valid 10-digit mobile number starting with 6, 7, 8, or 9.")
        if Passenger.objects.filter(phone_number=phone).exists() or Passenger.objects.filter(phone_number__endswith=digits).exists():
            raise forms.ValidationError("A passenger account with this phone number is already registered.")
        return phone

    def clean_emergency_contact_1_name(self):
        name = self.cleaned_data.get('emergency_contact_1_name', '').strip()
        if name and not re.match(NAME_REGEX, name):
            raise forms.ValidationError("Contact name must contain only letters and spaces.")
        return name

    def clean_emergency_contact_1_phone(self):
        phone = self.cleaned_data.get('emergency_contact_1_phone', '').strip()
        if phone:
            digits = re.sub(r'\D', '', phone)
            if len(digits) == 12 and digits.startswith('91'):
                digits = digits[2:]
            if len(digits) != 10:
                raise forms.ValidationError("Emergency contact phone must be a valid 10-digit number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('username') and cleaned_data.get('email'):
            base_user = cleaned_data.get('email').split('@')[0]
            candidate = base_user
            idx = 1
            while User.objects.filter(username=candidate).exists():
                candidate = f"{base_user}{idx}"
                idx += 1
            cleaned_data['username'] = candidate
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.PASSENGER
        if commit:
            user.save()
            Passenger.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}".strip() or user.username,
                email=user.email,
                phone_number=user.phone or '',
                password=user.password,
                emergency_contact_1_name=self.cleaned_data.get('emergency_contact_1_name') or 'Primary Emergency Contact',
                emergency_contact_1_phone=self.cleaned_data.get('emergency_contact_1_phone') or user.phone or '+91 9447012345',
                emergency_contact_1_relation=self.cleaned_data.get('emergency_contact_1_relation') or 'Family',
            )
        return user


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            'emergency_contact_1_name', 'emergency_contact_1_phone', 'emergency_contact_1_relation',
            'emergency_contact_2_name', 'emergency_contact_2_phone', 'emergency_contact_2_relation',
            'emergency_contact_3_name', 'emergency_contact_3_phone', 'emergency_contact_3_relation',
            'address'
        ]
        widgets = {
            'emergency_contact_1_name': forms.TextInput(attrs={'class': 'form-control', 'pattern': NAME_REGEX, 'placeholder': 'Contact Name'}),
            'emergency_contact_1_phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': '10-digit Phone'}),
            'emergency_contact_1_relation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Father, Mother, Guardian'}),
            'emergency_contact_2_name': forms.TextInput(attrs={'class': 'form-control', 'pattern': NAME_REGEX, 'placeholder': 'Contact Name'}),
            'emergency_contact_2_phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': '10-digit Phone'}),
            'emergency_contact_2_relation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Friend, Colleague'}),
            'emergency_contact_3_name': forms.TextInput(attrs={'class': 'form-control', 'pattern': NAME_REGEX, 'placeholder': 'Contact Name'}),
            'emergency_contact_3_phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': '10-digit Phone'}),
            'emergency_contact_3_relation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Campus Hostel, Warden'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Residential / Campus Address'}),
        }

    def _validate_contact_name(self, field_name):
        val = self.cleaned_data.get(field_name, '').strip()
        if val and not re.match(NAME_REGEX, val):
            raise forms.ValidationError("Contact name must contain only letters and spaces.")
        return val

    def _validate_contact_phone(self, field_name):
        val = self.cleaned_data.get(field_name, '').strip()
        if val:
            digits = re.sub(r'\D', '', val)
            if len(digits) == 12 and digits.startswith('91'):
                digits = digits[2:]
            if len(digits) != 10:
                raise forms.ValidationError("Phone number must contain exactly 10 digits.")
        return val

    def clean_emergency_contact_1_name(self):
        return self._validate_contact_name('emergency_contact_1_name')

    def clean_emergency_contact_2_name(self):
        return self._validate_contact_name('emergency_contact_2_name')

    def clean_emergency_contact_3_name(self):
        return self._validate_contact_name('emergency_contact_3_name')

    def clean_emergency_contact_1_phone(self):
        return self._validate_contact_phone('emergency_contact_1_phone')

    def clean_emergency_contact_2_phone(self):
        return self._validate_contact_phone('emergency_contact_2_phone')

    def clean_emergency_contact_3_phone(self):
        return self._validate_contact_phone('emergency_contact_3_phone')


class AdminDriverRegistrationForm(forms.Form):
    # Driver User Account Info
    username = forms.CharField(max_length=50, min_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. driver_rajesh'}))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Initial Password for Driver'}))
    first_name = forms.CharField(max_length=50, min_length=2, validators=[name_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Driver First Name', 'pattern': NAME_REGEX}))
    last_name = forms.CharField(max_length=50, min_length=1, validators=[name_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Driver Last Name', 'pattern': NAME_REGEX}))
    phone = forms.CharField(max_length=20, validators=[phone_validator], widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': 'Driver Mobile (e.g. 9876543210)'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Driver Email (Optional)'}))
    
    # Driver KYC
    license_number = forms.CharField(max_length=50, validators=[license_validator], widget=forms.TextInput(attrs={'class': 'form-control font-monospace text-uppercase', 'placeholder': 'e.g. KL-05-2021000892'}))
    experience_years = forms.IntegerField(min_value=0, max_value=60, initial=3, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 60}))
    driver_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    license_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,image/*'}))
    id_proof_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,image/*'}))
    police_clearance_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,image/*'}))

    # Vehicle Info
    registration_number = forms.CharField(max_length=30, validators=[vehicle_plate_validator], widget=forms.TextInput(attrs={'class': 'form-control font-monospace text-uppercase', 'placeholder': 'e.g. KL-05-AT-4455'}))
    vehicle_type = forms.ChoiceField(
        choices=[
            ('auto', 'Auto-Rickshaw'),
            ('taxi', 'Local Taxi (Hatchback/Sedan)'),
            ('cab', 'Sedan / Hatchback Cab'),
            ('van', 'Passenger Van / Minibus'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    make_model = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bajaj RE Compact 4S / Swift Dzire'}))
    rc_book_doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,image/*'}))
    
    # Immediate Approval Checkbox
    auto_approve = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label="Approve & Generate QR Code immediately")

    def clean_first_name(self):
        fn = self.cleaned_data.get('first_name', '').strip()
        if not re.match(NAME_REGEX, fn):
            raise forms.ValidationError("First name must contain only letters and spaces.")
        return fn

    def clean_last_name(self):
        ln = self.cleaned_data.get('last_name', '').strip()
        if not re.match(NAME_REGEX, ln):
            raise forms.ValidationError("Last name must contain only letters and spaces.")
        return ln

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(f"Username '{username}' is already taken.")
        return username

    def clean_license_number(self):
        lic = self.cleaned_data.get('license_number', '').strip().upper()
        if not re.match(LICENSE_REGEX, lic):
            raise forms.ValidationError("Please enter a valid license number format (e.g. KL-05-2021000892).")
        if Driver.objects.filter(license_number__iexact=lic).exists():
            raise forms.ValidationError(f"A driver with license number '{lic}' is already registered.")
        return lic

    def clean_registration_number(self):
        reg = self.cleaned_data.get('registration_number', '').strip().upper()
        if not re.match(VEHICLE_PLATE_REGEX, reg):
            raise forms.ValidationError("Please enter a valid vehicle plate format (e.g. KL-05-AT-4455).")
        if Driver.objects.filter(vehicle_number__iexact=reg).exists():
            raise forms.ValidationError(f"A vehicle with registration number '{reg}' is already registered.")
        return reg

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 12 and digits.startswith('91'):
            digits = digits[2:]
        if len(digits) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        if Driver.objects.filter(phone_number=phone).exists() or Driver.objects.filter(phone_number__endswith=digits).exists():
            raise forms.ValidationError(f"A driver with phone number '{phone}' is already registered.")
        return phone

    def clean_driver_photo(self):
        return validate_kyc_document(self.cleaned_data.get('driver_photo'), 'Driver Photo')

    def clean_license_doc(self):
        return validate_kyc_document(self.cleaned_data.get('license_doc'), 'Driving License Document')

    def clean_id_proof_doc(self):
        return validate_kyc_document(self.cleaned_data.get('id_proof_doc'), 'ID Proof Document')

    def clean_police_clearance_doc(self):
        return validate_kyc_document(self.cleaned_data.get('police_clearance_doc'), 'Police Clearance Certificate')

    def clean_rc_book_doc(self):
        return validate_kyc_document(self.cleaned_data.get('rc_book_doc'), 'RC Book Document')


class DriverKYCReviewForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['verification_status', 'verification_notes']
        widgets = {
            'verification_status': forms.Select(attrs={'class': 'form-select'}),
            'verification_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add administrative remarks, document check notes, or rejection reasons...'}),
        }


class TripRatingForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.Select(choices=[(i, f"{i} Stars - {'Excellent' if i==5 else 'Good' if i==4 else 'Average' if i==3 else 'Poor' if i==2 else 'Terrible'}") for i in range(5, 0, -1)], attrs={'class': 'form-select'})
    )
    driving_safety_rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.Select(choices=[(i, f"{i}/5") for i in range(5, 0, -1)], attrs={'class': 'form-select'})
    )
    vehicle_cleanliness_rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.Select(choices=[(i, f"{i}/5") for i in range(5, 0, -1)], attrs={'class': 'form-select'})
    )
    behavior_rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.Select(choices=[(i, f"{i}/5") for i in range(5, 0, -1)], attrs={'class': 'form-select'})
    )
    fare_honesty_rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.Select(choices=[(i, f"{i}/5") for i in range(5, 0, -1)], attrs={'class': 'form-select'})
    )

    class Meta:
        model = RatingReview
        fields = [
            'rating', 
            'driving_safety_rating', 
            'vehicle_cleanliness_rating', 
            'behavior_rating', 
            'fare_honesty_rating', 
            'review'
        ]
        widgets = {
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience to help fellow passengers stay safe...'}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'description', 'evidence_photo']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'minlength': 10, 'placeholder': 'Describe in detail what happened during your trip (min 10 characters)...'}),
            'evidence_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_description(self):
        desc = self.cleaned_data.get('description', '').strip()
        if len(desc) < 10:
            raise forms.ValidationError("Please provide a more detailed description (at least 10 characters).")
        return desc


class DriverSearchForm(forms.Form):
    query = forms.CharField(
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg', 
            'placeholder': 'Enter Vehicle Number (e.g. KL-05-AT-4455) or License No...',
            'id': 'vehicle-search-input',
            'autocomplete': 'off'
        })
    )


class ResetPasswordForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=100, 
        required=True,
        label="Username / Email / Mobile",
        widget=forms.TextInput(attrs={
            'class': 'form-control py-2', 
            'placeholder': 'Enter your registered Username, Email, or Mobile',
            'required': True
        })
    )
    new_password = forms.CharField(
        min_length=4,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-2 pe-5', 
            'placeholder': 'Enter New Password (min 4 chars)',
            'required': True,
            'id': 'id_new_password',
            'autocomplete': 'new-password'
        }),
        label="New Password"
    )
    confirm_password = forms.CharField(
        min_length=4,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-2 pe-5', 
            'placeholder': 'Confirm New Password',
            'required': True,
            'id': 'id_confirm_password',
            'autocomplete': 'new-password'
        }),
        label="Confirm Password"
    )

    def clean_username_or_email(self):
        ident = self.cleaned_data.get('username_or_email', '').strip()
        if not ident:
            raise forms.ValidationError("Please provide your registered username, email, or mobile number.")
        return ident

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')

        if p1:
            if len(p1) < 4:
                self.add_error('new_password', "Password must be at least 4 characters long.")
                raise forms.ValidationError("Password must be at least 4 characters long.")

        if p1 and p2:
            if p1 != p2:
                self.add_error('confirm_password', "Passwords do not match. Please re-enter carefully.")
                raise forms.ValidationError("Passwords do not match. Please re-enter carefully.")

        return cleaned_data


class IncidentReportForm(forms.Form):
    passenger_name = forms.CharField(
        max_length=100, 
        min_length=2,
        required=True,
        validators=[name_validator],
        label="Passenger Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Passenger Name', 'pattern': NAME_REGEX})
    )
    trip_id = forms.CharField(
        max_length=100, 
        required=False, 
        label="Trip ID",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TRP-88231 (Optional)'})
    )
    incident_type = forms.ChoiceField(
        choices=[
            ('ACCIDENT', 'Accident / Vehicle Collision'),
            ('HARASSMENT', 'Harassment / Safety Threat'),
            ('UNSAFE_DRIVING', 'Unsafe Driving / Speeding'),
            ('OTHER', 'Other Emergency'),
        ],
        label="Incident Type",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'minlength': 10, 'placeholder': 'Provide full description of the incident (min 10 characters)...'})
    )
    incident_date_time = forms.DateTimeField(
        required=False,
        label="Date & Time",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )

    def clean_passenger_name(self):
        name = self.cleaned_data.get('passenger_name', '').strip()
        if not re.match(NAME_REGEX, name):
            raise forms.ValidationError("Passenger name must contain only letters and spaces.")
        return name

    def clean_description(self):
        desc = self.cleaned_data.get('description', '').strip()
        if len(desc) < 10:
            raise forms.ValidationError("Incident description must be at least 10 characters.")
        return desc


class DriverProfileManagementForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        min_length=2,
        validators=[name_validator],
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Driver Full Name', 'pattern': NAME_REGEX})
    )
    email = forms.EmailField(
        required=False,
        label="Email (View Only)",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    phone_number = forms.CharField(
        max_length=20,
        validators=[phone_validator],
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': 'Contact Mobile Number'})
    )
    license_number = forms.CharField(
        max_length=50,
        required=False,
        validators=[license_validator],
        label="License Number",
        widget=forms.TextInput(attrs={'class': 'form-control font-monospace text-uppercase', 'placeholder': 'KL-05-2021000892'})
    )
    vehicle_number = forms.CharField(
        max_length=30,
        required=False,
        validators=[vehicle_plate_validator],
        label="Vehicle Registration Number",
        widget=forms.TextInput(attrs={'class': 'form-control font-monospace text-uppercase', 'placeholder': 'e.g. KL-05-AT-4455'})
    )
    vehicle_type = forms.ChoiceField(
        choices=[
            ('auto', 'Auto-Rickshaw'),
            ('taxi', 'Local Taxi (Hatchback/Sedan)'),
            ('cab', 'Cab / Car'),
            ('van', 'Passenger Van / Minibus'),
        ],
        required=False,
        label="Vehicle Category",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    vehicle_make_model = forms.CharField(
        max_length=100,
        required=False,
        label="Vehicle Make & Model",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bajaj RE Compact 4S'})
    )
    profile_photo = forms.ImageField(
        required=False,
        label="Driver Photo",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not re.match(NAME_REGEX, name):
            raise forms.ValidationError("Driver name must contain only letters and spaces.")
        return name

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 12 and digits.startswith('91'):
            digits = digits[2:]
        if len(digits) != 10:
            raise forms.ValidationError("Phone number must contain exactly 10 digits.")
        return phone

    def clean_license_number(self):
        lic = self.cleaned_data.get('license_number', '').strip().upper()
        if lic and not re.match(LICENSE_REGEX, lic):
            raise forms.ValidationError("Please enter a valid license format (e.g. KL-05-2021000892).")
        return lic

    def clean_vehicle_number(self):
        reg = self.cleaned_data.get('vehicle_number', '').strip().upper()
        if reg and not re.match(VEHICLE_PLATE_REGEX, reg):
            raise forms.ValidationError("Please enter a valid vehicle plate format (e.g. KL-05-AT-4455).")
        return reg


class PassengerProfileManagementForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        min_length=2,
        validators=[name_validator],
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': NAME_REGEX})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=20,
        validators=[phone_validator],
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'})
    )
    profile_photo = forms.ImageField(
        required=False,
        label="Profile Photo",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '').strip()
        if not re.match(NAME_REGEX, name):
            raise forms.ValidationError("Name must contain only letters and spaces.")
        return name

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 12 and digits.startswith('91'):
            digits = digits[2:]
        if len(digits) != 10:
            raise forms.ValidationError("Phone number must contain exactly 10 digits.")
        return phone
