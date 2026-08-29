import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
import django
django.setup()

from core.models import User, Passenger, Driver
from core.forms import (
    PassengerRegisterForm, AdminDriverRegistrationForm,
    ResetPasswordForm, TripRatingForm, ComplaintForm, IncidentReportForm
)

def run_validation_tests():
    print("=" * 80)
    print("            SAFERIDE FORM & MODEL VALIDATION AUDIT             ")
    print("=" * 80)

    tests_run = 0
    tests_passed = 0

    def assert_valid(test_name, condition, error_detail=""):
        nonlocal tests_run, tests_passed
        tests_run += 1
        if condition:
            tests_passed += 1
            print(f" [PASS] | {test_name}")
        else:
            print(f" [FAIL] | {test_name} -> {error_detail}")

    # --- 1. Passenger Registration Validations ---
    print("\n--- 1. PASSENGER REGISTRATION FORM VALIDATIONS ---")
    
    # 1.1 Mismatched Passwords
    form = PassengerRegisterForm(data={
        'first_name': 'Test', 'last_name': 'User', 'email': 'unique1@test.com',
        'phone': '+91 9111111111', 'username': 'test_unique_1',
        'password1': 'pass1234', 'password2': 'differentpass'
    })
    assert_valid("Rejects mismatched passwords", not form.is_valid() and 'password2' in form.errors or '__all__' in form.errors, form.errors.as_text())

    # 1.2 Duplicate Email
    existing_p = Passenger.objects.first()
    form = PassengerRegisterForm(data={
        'first_name': 'Test', 'last_name': 'User', 'email': existing_p.email,
        'phone': '+91 9111111112', 'username': 'test_unique_2',
        'password1': 'pass1234', 'password2': 'pass1234'
    })
    assert_valid("Rejects already registered email", not form.is_valid() and 'email' in form.errors, form.errors.as_text())

    # 1.3 Duplicate Phone
    form = PassengerRegisterForm(data={
        'first_name': 'Test', 'last_name': 'User', 'email': 'unique3@test.com',
        'phone': existing_p.phone_number, 'username': 'test_unique_3',
        'password1': 'pass1234', 'password2': 'pass1234'
    })
    assert_valid("Rejects already registered phone number", not form.is_valid() and 'phone' in form.errors, form.errors.as_text())

    # 1.4 Password too short (< 4 chars)
    form = PassengerRegisterForm(data={
        'first_name': 'Test', 'last_name': 'User', 'email': 'unique4@test.com',
        'phone': '+91 9111111114', 'username': 'test_unique_4',
        'password1': '12', 'password2': '12'
    })
    assert_valid("Rejects password under minimum length", not form.is_valid() and ('password1' in form.errors or 'password2' in form.errors), form.errors.as_text())

    # 1.5 Valid Passenger Registration
    form = PassengerRegisterForm(data={
        'first_name': 'Valid', 'last_name': 'Passenger', 'email': 'valid_unique_99@test.com',
        'phone': '+91 9111999888', 'username': 'valid_unique_99',
        'password1': 'validpass123', 'password2': 'validpass123',
        'emergency_contact_1_name': 'Parent Name', 'emergency_contact_1_phone': '+91 9876543210'
    })
    assert_valid("Accepts valid complete passenger registration data", form.is_valid(), form.errors.as_text())

    # 1.6 Reject Names with Digits/Symbols
    form = PassengerRegisterForm(data={
        'first_name': 'Rahul123', 'last_name': 'User', 'email': 'unique5@test.com',
        'phone': '+91 9111111115', 'username': 'test_unique_5',
        'password1': 'validpass123', 'password2': 'validpass123'
    })
    assert_valid("Rejects passenger name with digits/special characters", not form.is_valid() and 'first_name' in form.errors, form.errors.as_text())

    # 1.7 Reject Invalid Phone Format
    form = PassengerRegisterForm(data={
        'first_name': 'Rahul', 'last_name': 'User', 'email': 'unique6@test.com',
        'phone': '12345', 'username': 'test_unique_6',
        'password1': 'validpass123', 'password2': 'validpass123'
    })
    assert_valid("Rejects invalid short phone number", not form.is_valid() and 'phone' in form.errors, form.errors.as_text())

    # --- 2. Admin Driver Registration Validations ---
    print("\n--- 2. DRIVER REGISTRATION VALIDATIONS ---")
    existing_d = Driver.objects.first()

    # 2.1 Duplicate License Number
    form = AdminDriverRegistrationForm(data={
        'username': 'driver_new_test', 'password': 'driver123', 'first_name': 'New', 'last_name': 'Driver',
        'phone': '+91 9999999991', 'license_number': existing_d.license_number,
        'experience_years': 5, 'registration_number': 'KL-05-ZZ-0001', 'vehicle_type': 'auto'
    })
    assert_valid("Rejects duplicate driver license number", not form.is_valid() and 'license_number' in form.errors, form.errors.as_text())

    # 2.2 Duplicate Vehicle Registration Number
    form = AdminDriverRegistrationForm(data={
        'username': 'driver_new_test2', 'password': 'driver123', 'first_name': 'New', 'last_name': 'Driver',
        'phone': '+91 9999999992', 'license_number': 'KL-05-9999999999',
        'experience_years': 5, 'registration_number': existing_d.vehicle_number, 'vehicle_type': 'taxi'
    })
    assert_valid("Rejects duplicate vehicle registration number", not form.is_valid() and 'registration_number' in form.errors, form.errors.as_text())

    # 2.3 Duplicate Driver Username
    form = AdminDriverRegistrationForm(data={
        'username': existing_d.user.username, 'password': 'driver123', 'first_name': 'New', 'last_name': 'Driver',
        'phone': '+91 9999999993', 'license_number': 'KL-05-8888888888',
        'experience_years': 5, 'registration_number': 'KL-05-ZZ-0003', 'vehicle_type': 'cab'
    })
    assert_valid("Rejects duplicate driver username", not form.is_valid() and 'username' in form.errors, form.errors.as_text())

    # 2.4 Reject Invalid Vehicle Plate Format
    form = AdminDriverRegistrationForm(data={
        'username': 'driver_plate_test', 'password': 'driver123', 'first_name': 'Raj', 'last_name': 'Kumar',
        'phone': '+91 9447000222', 'license_number': 'KL-05-20220001122',
        'experience_years': 4, 'registration_number': 'INVALID-PLATE-12345', 'vehicle_type': 'auto'
    })
    assert_valid("Rejects invalid vehicle plate format", not form.is_valid() and 'registration_number' in form.errors, form.errors.as_text())

    # 2.5 Valid Driver Registration Data
    form = AdminDriverRegistrationForm(data={
        'username': 'driver_valid_unique', 'password': 'driver123', 'first_name': 'Sunil', 'last_name': 'Kumar',
        'phone': '+91 9447000111', 'license_number': 'KL-05-20220007788',
        'experience_years': 6, 'registration_number': 'KL-05-AT-0099', 'vehicle_type': 'auto'
    })
    assert_valid("Accepts valid complete driver registration data", form.is_valid(), form.errors.as_text())

    # --- 3. Password Reset Form Validations ---
    print("\n--- 3. PASSWORD RESET FORM VALIDATIONS ---")

    # 3.1 Mismatched new passwords
    form = ResetPasswordForm(data={
        'username_or_email': 'vyshnavi', 'new_password': 'newpassword123', 'confirm_password': 'mismatchpassword'
    })
    assert_valid("Rejects mismatched reset passwords", not form.is_valid(), form.errors.as_text())

    # 3.2 Short new password (< 4 chars)
    form = ResetPasswordForm(data={
        'username_or_email': 'vyshnavi', 'new_password': '12', 'confirm_password': '12'
    })
    assert_valid("Rejects reset password under minimum length", not form.is_valid(), form.errors.as_text())

    # 3.3 Valid reset password
    form = ResetPasswordForm(data={
        'username_or_email': 'vyshnavi', 'new_password': 'newSecurePass123', 'confirm_password': 'newSecurePass123'
    })
    assert_valid("Accepts valid matching reset password", form.is_valid(), form.errors.as_text())

    # --- 4. Trip Feedback & Rating Form Validations ---
    print("\n--- 4. TRIP FEEDBACK & RATING VALIDATIONS ---")
    
    # 4.1 Valid multi-factor rating
    form = TripRatingForm(data={
        'rating': 5, 'driving_safety_rating': 5, 'vehicle_cleanliness_rating': 4,
        'behavior_rating': 5, 'fare_honesty_rating': 5, 'review': 'Smooth safe trip!'
    })
    assert_valid("Accepts valid 1-5 star ratings and review text", form.is_valid(), form.errors.as_text())

    # 4.2 Invalid rating range
    form = TripRatingForm(data={
        'rating': 10, 'driving_safety_rating': 5, 'vehicle_cleanliness_rating': 4,
        'behavior_rating': 5, 'fare_honesty_rating': 5, 'review': ''
    })
    assert_valid("Rejects out-of-range rating numbers", not form.is_valid(), form.errors.as_text())

    # --- 5. Complaint & Incident Form Validations ---
    print("\n--- 5. COMPLAINT & INCIDENT REPORT VALIDATIONS ---")

    # 5.1 Valid Complaint
    form = ComplaintForm(data={
        'category': 'OVERCHARGING', 'description': 'Refused to charge standard meter fare.'
    })
    assert_valid("Accepts valid complaint category & description", form.is_valid(), form.errors.as_text())

    # 5.2 Short Complaint Description (< 10 chars)
    form = ComplaintForm(data={'category': 'OVERCHARGING', 'description': 'Too bad'})
    assert_valid("Rejects complaint with description under 10 chars", not form.is_valid() and 'description' in form.errors, form.errors.as_text())

    # 5.3 Valid Incident Report
    form = IncidentReportForm(data={
        'passenger_name': 'Vyshnavi Venu', 'incident_type': 'UNSAFE_DRIVING',
        'description': 'Driver was overtaking on sharp turn dangerously.'
    })
    assert_valid("Accepts valid safety incident report", form.is_valid(), form.errors.as_text())

    # 5.4 Reject Passenger Name with Numbers in Incident Report
    form = IncidentReportForm(data={
        'passenger_name': 'Passenger123', 'incident_type': 'UNSAFE_DRIVING',
        'description': 'Driver was overtaking on sharp turn dangerously.'
    })
    assert_valid("Rejects incident report with numbers in passenger name", not form.is_valid() and 'passenger_name' in form.errors, form.errors.as_text())

    # Summary
    print("\n" + "=" * 80)
    print(f"VALIDATION AUDIT SUMMARY: {tests_passed}/{tests_run} TESTS PASSED ({(tests_passed/tests_run)*100:.1f}%)")
    if tests_passed == tests_run:
        print("All form, field, and model validations are 100% CORRECT and verified!")
    print("=" * 80)

if __name__ == '__main__':
    run_validation_tests()
