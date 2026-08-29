import os
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saferide_project.settings')
import django
django.setup()

from django.test import Client
from core.models import (
    User, Admin, Passenger, Driver, VehicleDocuments,
    Trip, RatingReview, Complaint, SOSAlert, IncidentReport
)

def run_diagnostics():
    print("=" * 80)
    print("           SAFERIDE FULL PROJECT HEALTH & INTEGRITY REPORT            ")
    print("=" * 80)

    results = []

    def log_check(category, name, passed, details=""):
        status_str = " [PASS] " if passed else " [FAIL] "
        results.append((category, name, passed, details))
        print(f"{status_str} | {category:18s} | {name:32s} | {details}")

    # 1. Database Table Checks
    print("\n--- 1. DATABASE & MODELS INTEGRITY ---")
    try:
        user_cnt = User.objects.count()
        log_check("Database", "tbl_user (Users)", user_cnt > 0, f"{user_cnt} accounts active")

        admin_cnt = Admin.objects.count()
        log_check("Database", "tbl_admin (Admin)", admin_cnt > 0, f"{admin_cnt} admins")

        pass_cnt = Passenger.objects.count()
        log_check("Database", "tbl_passenger (Passengers)", pass_cnt > 0, f"{pass_cnt} passengers")

        driver_cnt = Driver.objects.count()
        log_check("Database", "tbl_driver (Drivers)", driver_cnt >= 10, f"{driver_cnt} drivers registered")

        trip_cnt = Trip.objects.count()
        log_check("Database", "tbl_trip (Trips)", True, f"{trip_cnt} trips logged")

        sos_cnt = SOSAlert.objects.count()
        log_check("Database", "tbl_sos_alert (SOS Alerts)", True, f"{sos_cnt} alerts")

        comp_cnt = Complaint.objects.count()
        log_check("Database", "tbl_complaint (Complaints)", True, f"{comp_cnt} complaints")

        doc_cnt = VehicleDocuments.objects.count()
        log_check("Database", "tbl_vehicle_documents (Docs)", doc_cnt > 0, f"{doc_cnt} vehicle records")
    except Exception as e:
        log_check("Database", "Database Connection", False, str(e))

    # 2. Authentication Checks
    print("\n--- 2. AUTHENTICATION & LOGIN FLOWS ---")
    client = Client()

    # Admin Login
    admin_login = client.login(username='admin', password='admin123')
    log_check("Auth", "Admin Login (admin/admin123)", admin_login, "Success" if admin_login else "Failed")
    client.logout()

    # Passenger Login
    pass_login = client.login(username='vyshnavi', password='passenger123')
    log_check("Auth", "Passenger Login (vyshnavi)", pass_login, "Success" if pass_login else "Failed")
    client.logout()

    # Driver Logins (All 10 Drivers)
    all_drivers = Driver.objects.all()
    driver_success = 0
    for d in all_drivers:
        if client.login(username=d.user.username, password='driver123'):
            driver_success += 1
        client.logout()
    log_check("Auth", "Driver Logins (driver123)", driver_success == all_drivers.count(), f"{driver_success}/{all_drivers.count()} drivers authenticated")

    # 3. Public Pages & HTTP Status
    print("\n--- 3. PUBLIC PAGES & ENDPOINTS ---")
    public_urls = [
        ('/', 'Home Landing Page'),
        ('/login/passenger/', 'Passenger Login Page'),
        ('/login/driver/', 'Driver Login Page'),
        ('/secure-admin-portal/login/', 'Admin Login Page'),
        ('/register/passenger/', 'Passenger Register Page'),
        ('/reset-password/', 'Reset Password Page'),
        ('/verify/', 'Driver Verification Search'),
    ]
    for url, desc in public_urls:
        res = client.get(url)
        log_check("Public Page", desc, res.status_code == 200, f"HTTP {res.status_code}")

    # Driver Public Verification Card
    first_verified_driver = Driver.objects.filter(verification_status=Driver.VerificationStatus.VERIFIED).first()
    if first_verified_driver:
        verify_url = f"/verify/{first_verified_driver.verification_token}/"
        res = client.get(verify_url)
        log_check("Public Page", f"Verified Driver Card ({first_verified_driver.vehicle_number})", res.status_code == 200, f"HTTP {res.status_code}")

    # 4. Passenger Module (Protected Routes)
    print("\n--- 4. PASSENGER PORTAL MODULE ---")
    client.login(username='vyshnavi', password='passenger123')
    passenger_urls = [
        ('/passenger/dashboard/', 'Passenger Hub / Dashboard'),
        ('/passenger/trip-history/', 'Passenger Trip History'),
        ('/passenger/emergency-contacts/', 'Emergency Contacts'),
        ('/passenger/profile/', 'Passenger Profile Settings'),
        ('/passenger/incident/report/', 'Incident Report Form'),
        ('/passenger/complaint/report/', 'Complaint Filing Form'),
    ]
    for url, desc in passenger_urls:
        res = client.get(url)
        log_check("Passenger Module", desc, res.status_code == 200, f"HTTP {res.status_code}")
    client.logout()

    # 5. Driver Module (Protected Routes)
    print("\n--- 5. DRIVER PORTAL MODULE ---")
    client.login(username='driver_rajesh', password='driver123')
    driver_urls = [
        ('/driver/dashboard/', 'Driver Dashboard'),
        ('/driver/id-badge/', 'Driver Vehicle QR Code'),
        ('/driver/qr-code/', 'Driver Vehicle QR Code (Alias)'),
        ('/driver/trip-logs/', 'Driver Trip Logs'),
        ('/driver/profile/', 'Driver Profile & Vehicle Specs'),
    ]
    for url, desc in driver_urls:
        res = client.get(url)
        log_check("Driver Module", desc, res.status_code == 200, f"HTTP {res.status_code}")
    client.logout()

    # 6. Admin Command Center (Protected Routes)
    print("\n--- 6. ADMIN COMMAND CENTER MODULE ---")
    client.login(username='admin', password='admin123')
    admin_urls = [
        ('/admin-panel/dashboard/', 'Admin Overview Dashboard'),
        ('/admin-panel/drivers/', 'Driver Verification & KYC List'),
        ('/admin-panel/sos-monitoring/', 'Real-time SOS Emergency Center'),
        ('/admin-panel/complaints/', 'Passenger Complaints Center'),
        ('/admin-panel/passengers/', 'Registered Passenger List'),
    ]
    for url, desc in admin_urls:
        res = client.get(url)
        log_check("Admin Module", desc, res.status_code == 200, f"HTTP {res.status_code}")
    client.logout()

    # 7. REST API Endpoints
    print("\n--- 7. REST APIS & AJAX SERVICES ---")
    res = client.get('/api/v1/drivers/')
    log_check("REST API", "GET /api/v1/drivers/", res.status_code == 200, f"HTTP {res.status_code} ({len(res.json())} drivers returned)")

    import json
    client.login(username='vyshnavi', password='passenger123')
    res = client.post('/api/sos/trigger/', data=json.dumps({'latitude': 9.6843, 'longitude': 76.6853, 'location_name': 'Test SafeRide Health Check Beacon'}), content_type='application/json')
    log_check("REST API", "POST /api/sos/trigger/ (Distress)", res.status_code == 200, f"HTTP {res.status_code} (Success: {res.json().get('success')})")
    client.logout()

    # Summary
    print("\n" + "=" * 80)
    total_checks = len(results)
    passed_checks = sum(1 for r in results if r[2])
    failed_checks = total_checks - passed_checks
    print(f"DIAGNOSTIC SUMMARY: {passed_checks}/{total_checks} CHECKS PASSED ({(passed_checks/total_checks)*100:.1f}%)")
    if failed_checks == 0:
        print("[SUCCESS] ALL SYSTEMS OPERATIONAL: SafeRide is 100% fully functional!")
    else:
        print(f"[WARNING] {failed_checks} ISSUES DETECTED: Review log output above.")
    print("=" * 80)

if __name__ == '__main__':
    run_diagnostics()
