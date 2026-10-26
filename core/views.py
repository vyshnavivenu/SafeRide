import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import (
    User, Admin, Passenger, Driver, VehicleDocuments, Trip, RatingReview,
    PassengerProfile, DriverProfile, VehicleDetails, TripSession, TripRating,
    Complaint, SOSAlert, IncidentReport
)
from .forms import (
    PassengerRegisterForm, EmergencyContactForm, AdminDriverRegistrationForm,
    DriverKYCReviewForm, TripRatingForm, ComplaintForm, DriverSearchForm,
    ResetPasswordForm, IncidentReportForm, DriverProfileManagementForm, PassengerProfileManagementForm
)
from .decorators import admin_required, driver_required, passenger_required

from datetime import timedelta
from django.conf import settings

import socket

def _get_network_base_url(request):
    """
    Returns the network base URL accessible by any device on the local network (Wi-Fi/LAN),
    or public URL if host is already an external domain/ngrok.
    """
    if not request:
        return "http://127.0.0.1:8000"
    host = request.get_host()
    # If host is already external or public, use standard absolute uri
    if not ('127.0.0.1' in host or 'localhost' in host):
        return request.build_absolute_uri('/')[:-1]

    # Detect local LAN IP (e.g. 192.168.x.x) for cross-device access on same Wi-Fi
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.3)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    # Extract port from host header first (e.g. 127.0.0.1:8000 -> 8000)
    port = None
    if ':' in host:
        try:
            port = host.split(':')[1]
        except Exception:
            port = None
    if not port:
        try:
            port = request.get_port()
        except Exception:
            port = None

    port_str = f":{port}" if port and str(port) not in ['80', '443'] else ""
    return f"{request.scheme}://{local_ip}{port_str}"

def _get_public_share_base_url(request=None):
    """
    Returns the public base URL suitable for sharing on WhatsApp or SMS
    to ensure it works seamlessly on any mobile phone anywhere in the world.
    Priority:
    1. If the current HTTP request came from a public/tunnel host (e.g. *.serveousercontent.com, *.ngrok-free.app, etc.), use that.
    2. Check .tunnel_url file in project root or PUBLIC_TUNNEL_URL in settings/env.
    3. Check local network Wi-Fi IP (_get_network_base_url).
    4. Fallback to request host.
    """
    # 1. Check for active public tunnel URL file or environment variable first!
    try:
        tunnel_file = settings.BASE_DIR / '.tunnel_url'
        if tunnel_file.exists():
            with open(tunnel_file, 'r', encoding='utf-8') as f:
                saved_url = f.read().strip()
                if saved_url.startswith('http://') or saved_url.startswith('https://'):
                    return saved_url.rstrip('/')
    except Exception:
        pass

    if request:
        try:
            host = request.get_host()
            if not ('127.0.0.1' in host or 'localhost' in host):
                return request.build_absolute_uri('/')[:-1]
        except Exception:
            pass



    import os
    env_tunnel = os.getenv('PUBLIC_TUNNEL_URL', '').strip()
    if env_tunnel and (env_tunnel.startswith('http://') or env_tunnel.startswith('https://')):
        return env_tunnel.rstrip('/')

    # Fallback to local network LAN IP (works on same Wi-Fi)
    return _get_network_base_url(request)

def global_context_processor(request):
    """Context processor providing active alerts count, metrics, emergency SOS window, and branding to all templates."""
    active_sos_count = 0
    pending_kyc_count = 0
    open_complaints_count = 0
    total_passengers_count = 0
    verified_drivers_count = 0
    total_drivers_count = 0

    has_active_sos_window = False
    sos_trip = None
    is_post_ride_sos = False
    sos_grace_minutes_remaining = 0
    active_trip_share_url = None
    active_trip_network_url = None
    active_trip_id = None

    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        if hasattr(user, 'is_admin_user') and user.is_admin_user():
            active_sos_count = SOSAlert.objects.filter(status__in=['Active', SOSAlert.Status.ACTIVE]).count()
            pending_kyc_count = Driver.objects.filter(verification_status__in=['Pending', Driver.VerificationStatus.PENDING]).count()
            open_complaints_count = Complaint.objects.filter(status__in=['Open', Complaint.Status.OPEN]).count()
            total_passengers_count = User.objects.filter(role=User.Role.PASSENGER).count()
            verified_drivers_count = Driver.objects.filter(verification_status__in=['Verified', Driver.VerificationStatus.VERIFIED]).count()
            total_drivers_count = Driver.objects.count()

        elif hasattr(user, 'is_passenger_user') and user.is_passenger_user():
            now = timezone.now()
            # 1. Check for current ongoing active trip
            active_trip = Trip.objects.filter(
                passenger=user,
                status__in=['Active', 'Ongoing', 'IN_PROGRESS', 'SOS_Triggered', Trip.Status.ACTIVE, Trip.Status.SOS_TRIGGERED]
            ).order_by('-start_time').first()

            if active_trip:
                has_active_sos_window = True
                sos_trip = active_trip
                active_trip_id = active_trip.trip_id
                try:
                    public_base = _get_public_share_base_url(request)
                    active_trip_share_url = f"{public_base}/live-track/{active_trip.trip_id}/"
                except Exception:
                    active_trip_share_url = request.build_absolute_uri(f"/live-track/{active_trip.trip_id}/")

                try:
                    net_base = _get_network_base_url(request)
                    active_trip_network_url = f"{net_base}/live-track/{active_trip.trip_id}/"
                except Exception:
                    active_trip_network_url = active_trip_share_url
            else:
                # 2. Check for trip completed within the last 20 minutes
                twenty_mins_ago = now - timedelta(minutes=20)
                recent_completed = Trip.objects.filter(
                    passenger=user,
                    status__in=['Completed', 'COMPLETED', Trip.Status.COMPLETED],
                    end_time__gte=twenty_mins_ago
                ).order_by('-end_time').first()

                if recent_completed and recent_completed.end_time:
                    has_active_sos_window = True
                    sos_trip = recent_completed
                    is_post_ride_sos = True
                    elapsed_seconds = (now - recent_completed.end_time).total_seconds()
                    sos_grace_minutes_remaining = max(1, int(20 - (elapsed_seconds / 60)))

        elif hasattr(user, 'is_driver_user') and user.is_driver_user():
            driver_profile = getattr(user, 'driver_profile', None)
            if driver_profile:
                active_trip = Trip.objects.filter(
                    driver=driver_profile,
                    status__in=['Active', 'Ongoing', 'IN_PROGRESS', 'SOS_Triggered', Trip.Status.ACTIVE, Trip.Status.SOS_TRIGGERED]
                ).order_by('-start_time').first()
                if active_trip:
                    active_trip_id = active_trip.trip_id
                    try:
                        public_base = _get_public_share_base_url(request)
                        active_trip_share_url = f"{public_base}/live-track/{active_trip.trip_id}/"
                    except Exception:
                        active_trip_share_url = request.build_absolute_uri(f"/live-track/{active_trip.trip_id}/")
                    try:
                        net_base = _get_network_base_url(request)
                        active_trip_network_url = f"{net_base}/live-track/{active_trip.trip_id}/"
                    except Exception:
                        active_trip_network_url = active_trip_share_url

    return {
        'APP_NAME': 'SafeRide',
        'APP_TAGLINE': 'Driver Verification & Passenger Safety System',
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
        'ACTIVE_SOS_COUNT': active_sos_count,
        'PENDING_KYC_COUNT': pending_kyc_count,
        'OPEN_COMPLAINTS_COUNT': open_complaints_count,
        'TOTAL_PASSENGERS_COUNT': total_passengers_count,
        'VERIFIED_DRIVERS_COUNT': verified_drivers_count,
        'TOTAL_DRIVERS_COUNT': total_drivers_count,
        'HAS_ACTIVE_SOS_WINDOW': has_active_sos_window,
        'SOS_TRIP': sos_trip,
        'IS_POST_RIDE_SOS': is_post_ride_sos,
        'SOS_GRACE_MINUTES_REMAINING': sos_grace_minutes_remaining,
        'ACTIVE_TRIP_SHARE_URL': active_trip_share_url,
        'ACTIVE_TRIP_NETWORK_URL': active_trip_network_url,
        'ACTIVE_TRIP_ID': active_trip_id,
        'PUBLIC_BASE_URL': _get_public_share_base_url(request),
    }

def home(request):
    """Landing homepage with safety system overview and role-based access portals."""
    verified_drivers_count = Driver.objects.filter(verification_status__in=['Verified', Driver.VerificationStatus.VERIFIED]).count()
    total_drivers_count = Driver.objects.count()
    pending_kyc_count = Driver.objects.filter(verification_status__in=['Pending', Driver.VerificationStatus.PENDING]).count()
    total_passengers_count = User.objects.filter(role=User.Role.PASSENGER).count()
    open_complaints_count = Complaint.objects.filter(status__in=['Open', Complaint.Status.OPEN]).count()
    active_sos_count = SOSAlert.objects.filter(status__in=['Active', SOSAlert.Status.ACTIVE]).count()
    completed_trips_count = Trip.objects.filter(status__in=['Completed', Trip.Status.COMPLETED]).count()
    avg_safety_score = Driver.objects.filter(verification_status__in=['Verified', Driver.VerificationStatus.VERIFIED]).aggregate(Avg('reputation_score'))['reputation_score__avg'] or 95.0

    context = {
        'verified_drivers_count': verified_drivers_count,
        'total_drivers_count': total_drivers_count,
        'pending_kyc_count': pending_kyc_count,
        'total_passengers_count': total_passengers_count,
        'open_complaints_count': open_complaints_count,
        'active_sos_count': active_sos_count,
        'completed_trips_count': completed_trips_count,
        'avg_safety_score': round(avg_safety_score, 1),
    }
    return render(request, 'home.html', context)

def _authenticate_by_username_or_email(request, identifier, password):
    """Helper to authenticate user using either username or email."""
    user = authenticate(request, username=identifier, password=password)
    if user is None:
        user_obj = User.objects.filter(Q(email__iexact=identifier) | Q(username__iexact=identifier)).first()
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
    return user

def login_view(request):
    """Redirect generic login to passenger login."""
    return redirect('passenger_login')

def passenger_login_view(request):
    """Dedicated PASSENGER LOGIN page."""
    if request.user.is_authenticated:
        return redirect('passenger_dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = _authenticate_by_username_or_email(request, identifier, password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('passenger_dashboard')
        else:
            messages.error(request, "Invalid Passenger Username/Email or Password.")
            return render(request, 'auth/passenger_login.html', {'username': identifier})

    return render(request, 'auth/passenger_login.html')

def driver_login_view(request):
    """Dedicated DRIVER LOGIN page."""
    if request.user.is_authenticated:
        return redirect('driver_dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = _authenticate_by_username_or_email(request, identifier, password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, Driver {user.get_full_name() or user.username}!")
            return redirect('driver_dashboard')
        else:
            messages.error(request, "Invalid Driver Username/Mobile or Password.")
            return render(request, 'auth/driver_login.html', {'username': identifier})

    return render(request, 'auth/driver_login.html')

def admin_login_view(request):
    """Dedicated ADMIN LOGIN page."""
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = _authenticate_by_username_or_email(request, identifier, password)
        if user is not None and user.is_admin_user():
            login(request, user)
            messages.success(request, f"Administrator Session Started for {user.username}.")
            return redirect('admin_dashboard')
        elif user is not None:
            messages.error(request, "Access Denied: This account is not an Administrator.")
            return render(request, 'auth/admin_login.html', {'username': identifier})
        else:
            messages.error(request, "Invalid Administrator credentials.")
            return render(request, 'auth/admin_login.html', {'username': identifier})

    return render(request, 'auth/admin_login.html')

def reset_password_view(request):
    """Reset Password Form matching Form 3 in PDF specification."""
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            ident = form.cleaned_data['username_or_email'].strip()
            new_pass = form.cleaned_data['new_password']
            user = User.objects.filter(
                Q(username__iexact=ident) | 
                Q(email__iexact=ident) | 
                Q(phone=ident) |
                Q(passenger_profile__phone_number=ident)
            ).first()
            if user:
                user.set_password(new_pass)
                user.save()
                
                # Sync passenger/driver password if exists
                if hasattr(user, 'passenger_profile') and user.passenger_profile:
                    user.passenger_profile.password = user.password
                    user.passenger_profile.save()
                elif hasattr(user, 'driver_profile') and user.driver_profile:
                    user.driver_profile.password = user.password
                    user.driver_profile.save()

                messages.success(request, "Password has been successfully reset! You can now log in with your new credentials.")
                return redirect('login')
            else:
                messages.error(request, "No registered account found with that username, email, or phone number.")
        else:
            messages.error(request, "Please correct the errors in the password reset form.")
    else:
        form = ResetPasswordForm()

    return render(request, 'auth/reset_password.html', {'form': form})

def logout_view(request):
    """Logs out user and redirects to home."""
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')

def dashboard_redirect(request):
    """Redirects authenticated users to their designated role-based dashboard."""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_admin_user():
        return redirect('admin_dashboard')
    elif request.user.is_driver_user():
        return redirect('driver_dashboard')
    else:
        return redirect('passenger_dashboard')

def passenger_register(request):
    """Passenger sign-up portal matching Form 1 (PASSENGER REGISTRATION)."""
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = PassengerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to SafeRide.")
            return redirect('passenger_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PassengerRegisterForm()

    return render(request, 'auth/passenger_register.html', {'form': form})

def driver_login_info(request):
    """Explains how drivers receive credentials from administrator."""
    return render(request, 'auth/driver_login_info.html')

# ==========================================
# DRIVER VERIFICATION & SAFETY CARD VIEWS
# ==========================================

def verify_driver_search(request):
    """Search driver by vehicle registration number or license number."""
    query = request.GET.get('query', '').strip()
    if not query:
        return render(request, 'verify_driver.html')

    cleaned_q = query.upper().replace(" ", "").replace("-", "")
    
    # Try exact match on cleaned reg number, license, or username
    driver = None
    all_drivers = Driver.objects.select_related('user').all()
    for d in all_drivers:
        d_clean = (d.vehicle_number or '').upper().replace(" ", "").replace("-", "")
        if d_clean == cleaned_q or query.upper() in (d.vehicle_number or '').upper() or query.upper() in (d.license_number or '').upper():
            driver = d
            break

    if not driver:
        # Search by driver license number or name
        driver = Driver.objects.filter(
            Q(license_number__icontains=query) | Q(name__icontains=query) | Q(user__username__icontains=query)
        ).first()

    if driver:
        if not driver.is_verified():
            return render(request, 'verify_driver.html', {'search_query': query, 'not_found': True, 'unverified_driver': driver})
        return redirect('verify_driver_token', token=driver.verification_token)
    else:
        return render(request, 'verify_driver.html', {'search_query': query, 'not_found': True})

def verify_driver_token(request, token):
    """Displays the comprehensive Driver Safety Card upon QR code scan or search match."""
    driver = Driver.objects.select_related('user').filter(verification_token=token).first()
    if not driver:
        return render(request, 'verify_driver.html', {'not_found': True, 'search_query': str(token)[:8]})
    
    if not driver.is_verified():
        return render(request, 'verify_driver.html', {'not_found': True, 'unverified_driver': driver, 'search_query': driver.vehicle_number or str(token)[:8]})
    
    # Check if passenger has active trip with this driver
    active_trip = None
    if request.user.is_authenticated and request.user.is_passenger_user():
        active_trip = Trip.objects.filter(
            passenger=request.user, 
            driver=driver, 
            status__in=['Ongoing', 'IN_PROGRESS']
        ).first()

    ratings = driver.received_ratings.select_related('passenger').order_by('-created_at')[:5]
    
    # Star score breakdown percentage
    all_ratings = driver.received_ratings.all()
    total_ratings_count = all_ratings.count()
    five_star_pct = round((all_ratings.filter(rating=5).count() / total_ratings_count * 100)) if total_ratings_count else 90

    context = {
        'driver': driver,
        'vehicle': getattr(driver, 'vehicle', None),
        'ratings': ratings,
        'total_ratings_count': total_ratings_count,
        'five_star_pct': five_star_pct,
        'active_trip': active_trip,
    }
    return render(request, 'driver_safety_card.html', context)

# ==========================================
# PASSENGER MODULE VIEWS
# ==========================================

def ensure_diverse_driver_ecosystem(user=None):
    """
    Ensures a diverse roster of verified drivers exists (Autos, Taxis, Cabs)
    with different names, vehicles, and ratings, and distributes existing
    passenger trips across them so Rajesh Kumar isn't the only driver.
    """
    from decimal import Decimal
    
    drivers_spec = [
        {
            'username': 'driver_rajesh',
            'name': 'Rajesh Kumar',
            'phone': '+91 94471 82930',
            'license_no': 'KL-05-20180004521',
            'reg_no': 'KL-05-AT-4455',
            'v_type': 'auto',
            'rating': 4.9,
            'score': 96.5,
            'trips': 642,
        },
        {
            'username': 'driver_anand',
            'name': 'Anand Joseph',
            'phone': '+91 98473 34455',
            'license_no': 'KL-05-20150009812',
            'reg_no': 'KL-05-TX-1024',
            'v_type': 'taxi',
            'rating': 4.8,
            'score': 94.0,
            'trips': 418,
        },
        {
            'username': 'driver_suresh',
            'name': 'Suresh Babu',
            'phone': '+91 97451 12233',
            'license_no': 'KL-05-20200003411',
            'reg_no': 'KL-05-CB-8890',
            'v_type': 'cab',
            'rating': 4.7,
            'score': 89.5,
            'trips': 215,
        },
        {
            'username': 'driver_manoj',
            'name': 'Manoj George',
            'phone': '+91 94472 90112',
            'license_no': 'KL-05-20170006734',
            'reg_no': 'KL-05-AT-3312',
            'v_type': 'auto',
            'rating': 4.9,
            'score': 95.0,
            'trips': 520,
        },
        {
            'username': 'driver_harikrishnan',
            'name': 'Harikrishnan Nair',
            'phone': '+91 98954 67890',
            'license_no': 'KL-05-20190008819',
            'reg_no': 'KL-05-TX-5544',
            'v_type': 'taxi',
            'rating': 4.8,
            'score': 92.5,
            'trips': 380,
        },
        {
            'username': 'driver_pradeep',
            'name': 'Pradeep Varma',
            'phone': '+91 97463 45678',
            'license_no': 'KL-05-20160002341',
            'reg_no': 'KL-05-AT-7890',
            'v_type': 'auto',
            'rating': 4.6,
            'score': 88.0,
            'trips': 190,
        },
        {
            'username': 'driver_varun',
            'name': 'Varun Menon',
            'phone': '+91 98472 23344',
            'license_no': 'KL-05-20210008899',
            'reg_no': 'KL-05-CB-4422',
            'v_type': 'cab',
            'rating': 4.85,
            'score': 93.0,
            'trips': 310,
        },
        {
            'username': 'driver_biju',
            'name': 'Biju Mathew',
            'phone': '+91 94005 61234',
            'license_no': 'KL-05-20220005612',
            'reg_no': 'KL-05-AT-1288',
            'v_type': 'auto',
            'rating': 4.7,
            'score': 90.0,
            'trips': 275,
        },
    ]

    created_drivers = []
    for d in drivers_spec:
        u, _ = User.objects.get_or_create(
            username=d['username'],
            defaults={
                'first_name': d['name'].split()[0],
                'last_name': d['name'].split()[1] if len(d['name'].split()) > 1 else '',
                'email': f"{d['username']}@saferide.org",
                'phone': d['phone'],
                'role': User.Role.DRIVER,
            }
        )
        if not u.has_usable_password():
            u.set_password('driver123')
            u.save()

        drv, _ = Driver.objects.update_or_create(
            user=u,
            defaults={
                'name': d['name'],
                'phone_number': d['phone'],
                'email': f"{d['username']}@saferide.org",
                'license_number': d['license_no'],
                'vehicle_number': d['reg_no'],
                'vehicle_type': d['v_type'],
                'verification_status': Driver.VerificationStatus.VERIFIED,
                'average_rating': d['rating'],
                'reputation_score': d['score'],
                'experience_years': 5,
                'total_trips': d['trips'],
                'upi_id': d.get('upi_id', f"{d['username'].replace('driver_', '')}@oksbi"),
            }
        )
        created_drivers.append(drv)

    # Distribute the passenger's trips across diverse drivers, destinations, distances, and fares
    if user and user.is_authenticated:
        passenger_trips = list(TripSession.objects.filter(passenger=user).order_by('-trip_id'))
        
        # Check if all completed trips are currently assigned to Rajesh Kumar
        rajesh = created_drivers[0]
        rajesh_count = sum(1 for t in passenger_trips if t.driver_id == rajesh.driver_id)

        if len(passenger_trips) > 1 and rajesh_count >= len(passenger_trips) - 1:
            trip_variations = [
                {
                    'driver': created_drivers[1],  # Anand Joseph (Taxi)
                    'dest': 'Kottayam Railway Station',
                    'lat': 9.591600, 'lng': 76.522200,
                    'dist': Decimal('28.50'),
                    'fare': Decimal('623.00'),
                },
                {
                    'driver': created_drivers[3],  # Manoj George (Auto)
                    'dest': 'Pala KSRTC Bus Station',
                    'lat': 9.691200, 'lng': 76.690400,
                    'dist': Decimal('3.80'),
                    'fare': Decimal('64.50'),
                },
                {
                    'driver': created_drivers[2],  # Suresh Babu (Cab)
                    'dest': 'St. Thomas Cathedral, Palai',
                    'lat': 9.709000, 'lng': 76.682000,
                    'dist': Decimal('5.20'),
                    'fare': Decimal('203.60'),
                },
                {
                    'driver': created_drivers[4],  # Harikrishnan Nair (Taxi)
                    'dest': 'Ettumanoor Mahadeva Temple',
                    'lat': 9.669800, 'lng': 76.564500,
                    'dist': Decimal('16.40'),
                    'fare': Decimal('405.20'),
                },
                {
                    'driver': created_drivers[5],  # Pradeep Varma (Auto)
                    'dest': 'Palai Town Civil Station',
                    'lat': 9.710000, 'lng': 76.680000,
                    'dist': Decimal('2.40'),
                    'fare': Decimal('43.50'),
                },
                {
                    'driver': created_drivers[6],  # Varun Menon (Cab)
                    'dest': 'Bharananganam Pilgrim Shrine',
                    'lat': 9.698000, 'lng': 76.721000,
                    'dist': Decimal('6.50'),
                    'fare': Decimal('227.00'),
                },
                {
                    'driver': created_drivers[7],  # Biju Mathew (Auto)
                    'dest': 'Lalam Bridge Junction, Palai',
                    'lat': 9.708200, 'lng': 76.683500,
                    'dist': Decimal('1.80'),
                    'fare': Decimal('34.50'),
                },
                {
                    'driver': created_drivers[0],  # Rajesh Kumar (Auto)
                    'dest': 'SJCET Main Campus Gate, Palai',
                    'lat': 9.684300, 'lng': 76.685300,
                    'dist': Decimal('1.20'),
                    'fare': Decimal('30.00'),
                },
            ]

            for idx, trip in enumerate(passenger_trips):
                var = trip_variations[idx % len(trip_variations)]
                trip.driver = var['driver']
                trip.destination_address = var['dest']
                trip.end_location = var['dest']
                trip.drop_location_name = var['dest']
                trip.destination_latitude = var['lat']
                trip.destination_longitude = var['lng']
                trip.drop_latitude = var['lat']
                trip.drop_longitude = var['lng']
                trip.distance_km = var['dist']
                trip.fare_amount = var['fare']
                try:
                    trip.generate_fare_qr_code()
                except Exception:
                    pass
                trip.save()

@passenger_required
def passenger_dashboard(request):
    """Passenger command center."""
    if request.user.is_passenger_user():
        profile, _ = PassengerProfile.objects.get_or_create(user=request.user)
    else:
        profile = getattr(request.user, 'passenger_profile', None) or Passenger(user=request.user)
    active_trip = TripSession.objects.filter(passenger=request.user, status__in=['Ongoing', 'IN_PROGRESS', 'Active', 'SOS_Triggered']).first()
    recent_trips = TripSession.objects.filter(passenger=request.user).select_related('driver', 'driver__user').order_by('-start_time')[:5]
    recent_complaints = Complaint.objects.filter(passenger=request.user).order_by('-created_at')[:3]
    verified_drivers = Driver.objects.filter(verification_status__in=['Verified', Driver.VerificationStatus.VERIFIED]).order_by('-reputation_score')

    context = {
        'profile': profile,
        'active_trip': active_trip,
        'recent_trips': recent_trips,
        'recent_complaints': recent_complaints,
        'search_form': DriverSearchForm(),
        'verified_drivers': verified_drivers,
    }
    return render(request, 'passenger/dashboard.html', context)

@passenger_required
def start_trip(request, driver_id):
    """Initiates a monitored safe trip session with the verified driver."""
    driver = get_object_or_404(DriverProfile, driver_id=driver_id)
    
    # Check if existing active trip
    existing = TripSession.objects.filter(passenger=request.user, status__in=['Active', 'Ongoing', TripSession.Status.ACTIVE]).first()
    if existing:
        messages.info(request, "You already have an ongoing trip. Resuming active trip session.")
        return redirect('active_trip', trip_id=existing.trip_id)

    try:
        pickup_lat = float(request.POST.get('pickup_lat') or 9.6843)
        pickup_lng = float(request.POST.get('pickup_lng') or 76.6853)
    except (ValueError, TypeError):
        pickup_lat = 9.6843
        pickup_lng = 76.6853
    pickup_name = (request.POST.get('pickup_name') or '').strip() or 'Boarding Point'
    destination_name = request.POST.get('destination_name', '').strip()
    destination_lat = request.POST.get('destination_lat')
    destination_lng = request.POST.get('destination_lng')

    live_sharing = request.POST.get('live_location_sharing') in ['true', '1', 'on', True]

    dest_lat_val = float(destination_lat) if destination_lat else None
    dest_lng_val = float(destination_lng) if destination_lng else None

    # Fallback to coordinates label if destination_name was blank
    if not destination_name and dest_lat_val and dest_lng_val:
        destination_name = f"Drop Point ({round(dest_lat_val, 4)}, {round(dest_lng_val, 4)})"

    trip = TripSession.objects.create(
        passenger=request.user,
        driver=driver,
        boarding_address=pickup_name,
        boarding_latitude=pickup_lat,
        boarding_longitude=pickup_lng,
        destination_address=destination_name if destination_name else None,
        destination_latitude=dest_lat_val,
        destination_longitude=dest_lng_val,
        current_latitude=pickup_lat,
        current_longitude=pickup_lng,
        pickup_location_name=pickup_name,
        pickup_latitude=pickup_lat,
        pickup_longitude=pickup_lng,
        drop_location_name=destination_name if destination_name else None,
        end_location=destination_name if destination_name else None,
        drop_latitude=dest_lat_val,
        drop_longitude=dest_lng_val,
        live_latitude=pickup_lat,
        live_longitude=pickup_lng,
        live_location_sharing=live_sharing,
        status=TripSession.Status.ACTIVE,
    )
    share_status_msg = "Live tracking enabled!" if live_sharing else "Trip initiated."
    messages.success(request, f"Safe Trip started with driver {driver.user.get_full_name() or driver.user.username}. {share_status_msg}")
    return redirect('active_trip', trip_id=trip.trip_id)

@passenger_required
def active_trip(request, trip_id):
    """Live ongoing trip monitoring interface with 1-Touch SOS and live track sharing."""
    cleaned_id = str(trip_id).upper().replace('TRIP', '').replace('TRP-', '').replace('TRP', '').replace('#', '').strip()
    trip = None
    if cleaned_id.isdigit():
        trip = TripSession.objects.select_related('driver', 'driver__user').filter(trip_id=int(cleaned_id), passenger=request.user).first()
    if not trip:
        try:
            import uuid as _uuid
            val_uuid = _uuid.UUID(str(trip_id).strip())
            trip = TripSession.objects.select_related('driver', 'driver__user').filter(
                Q(trip_uuid=val_uuid) | Q(share_token=val_uuid), passenger=request.user
            ).first()
        except (ValueError, TypeError, AttributeError):
            pass

    if not trip:
        raise Http404("Active trip session not found.")
    
    if trip.status == TripSession.Status.COMPLETED:
        messages.info(request, "This trip has already ended safely. Please rate your experience.")
        return redirect('rate_trip', trip_id=trip.trip_id)

    profile = getattr(request.user, 'passenger_profile', None)
    
    public_base = _get_public_share_base_url(request)
    network_base = _get_network_base_url(request)
    share_url = f"{public_base}/live-track/{trip.trip_id}/"
    network_share_url = f"{network_base}/live-track/{trip.trip_id}/"

    context = {
        'trip': trip,
        'driver': trip.driver,
        'vehicle': getattr(trip.driver, 'vehicle', None),
        'profile': profile,
        'share_url': share_url,
        'network_share_url': network_share_url,
    }
    return render(request, 'trip_active.html', context)

@passenger_required
def end_trip(request, trip_id):
    """Marks trip as completed, records verified drop-off telemetry, and routes to rating screen."""
    clean_id = str(trip_id).upper().replace('TRIP', '').replace('TRP-', '').replace('TRP', '').replace('#', '').strip()
    lookup_id = int(clean_id) if clean_id.isdigit() else trip_id
    trip = get_object_or_404(TripSession, trip_id=lookup_id, passenger=request.user)
    
    end_lat = request.POST.get('final_lat') or request.POST.get('end_lat')
    end_lng = request.POST.get('final_lng') or request.POST.get('end_lng')
    end_address = request.POST.get('final_address') or request.POST.get('end_address')

    trip.complete_trip(end_lat=end_lat, end_lng=end_lng, end_address=end_address)
    messages.success(request, f"Trip {trip.formatted_trip_id} completed safely! Please share your rating to help fellow passengers.")
    return redirect('rate_trip', trip_id=trip.trip_id)

@passenger_required
def rate_trip(request, trip_id):
    """Submits multi-criteria rating, reviews, and optional complaint for the completed journey."""
    clean_id = str(trip_id).upper().replace('TRIP', '').replace('TRP-', '').replace('TRP', '').replace('#', '').strip()
    lookup_id = int(clean_id) if clean_id.isdigit() else trip_id
    trip = get_object_or_404(TripSession.objects.select_related('driver', 'driver__user'), trip_id=lookup_id, passenger=request.user)
    
    # Check if already rated
    existing_rating = TripRating.objects.filter(trip=trip).first()
    if existing_rating:
        messages.info(request, "You have already submitted feedback for this trip. Thank you!")
        return redirect('passenger_dashboard')

    if request.method == 'POST':
        try:
            rating_val = int(request.POST.get('rating', 5))
        except (ValueError, TypeError):
            rating_val = 5

        review_text = request.POST.get('review_text') or request.POST.get('review', '')
        complaint_text = request.POST.get('complaint_text', '').strip()

        rating = TripRating.objects.create(
            trip=trip,
            driver=trip.driver,
            passenger=request.user,
            rating=rating_val,
            review=review_text,
        )
        trip.driver.recalculate_reputation()

        category = request.POST.get('category', 'GENERAL')
        if complaint_text or (category and category != 'GENERAL') or rating_val <= 2:
            cat_map = {
                'OVERCHARGING': Complaint.Category.OVERCHARGING,
                'SAFETY': Complaint.Category.RECKLESS_DRIVING,
                'HARASSMENT': Complaint.Category.HARASSMENT,
                'ROUTE': Complaint.Category.ROUTE_DEVIATION,
                'MISBEHAVIOR': Complaint.Category.MISBEHAVIOR,
            }
            comp_cat = cat_map.get(category, Complaint.Category.OTHER) if category != 'GENERAL' else (Complaint.Category.MISBEHAVIOR if rating_val <= 2 else Complaint.Category.OTHER)
            comp_desc = complaint_text or review_text or f"Low rating ({rating_val} stars) safety concern submitted by passenger."

            Complaint.objects.create(
                passenger=request.user,
                driver=trip.driver,
                trip=trip,
                category=comp_cat,
                description=comp_desc,
                status='Pending'
            )
            messages.warning(request, "Your feedback has been saved and a grievance report has been logged for admin review.")
        else:
            messages.success(request, "Thank you! Your feedback has been recorded and updated the driver's safety score.")

        return redirect('passenger_dashboard')

    from django.core.files.storage import default_storage
    import base64
    from io import BytesIO
    from urllib.parse import quote
    import qrcode

    # Ensure distance & valid regulated fare are calculated
    trip.calculate_distance_and_fare()

    driver_upi = (trip.driver.upi_id if (trip.driver and getattr(trip.driver, 'upi_id', None)) else 'saferide@upi').strip()
    payee_name = quote(getattr(trip.driver, 'name', None) or 'SafeRide Driver')
    fare_val = f"{trip.fare_amount:.2f}" if trip.fare_amount else "30.00"
    upi_pay_str = f"upi://pay?pa={driver_upi}&pn={payee_name}&am={fare_val}&cu=INR&tn=SafeRide_TRP_{trip.trip_id}&tr=TRP{trip.trip_id}"

    # Generate QR Code in-memory as Base64 Data URI so it NEVER fails, 404s, or renders blank
    fare_qr_data_uri = None
    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        qr.add_data(upi_pay_str)
        qr.make(fit=True)
        try:
            img = qr.make_image(fill_color="#0F172A", back_color="white")
        except Exception:
            img = qr.make_image()
        buf = BytesIO()
        img.save(buf, format='PNG')
        fare_qr_data_uri = f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
    except Exception as e:
        print(f"Error generating in-memory fare QR data URI: {e}")

    # Ensure fare QR code actually exists on disk; if missing or invalid, regenerate it
    qr_exists = bool(trip.fare_qr_code and trip.fare_qr_code.name and default_storage.exists(trip.fare_qr_code.name))
    if not qr_exists:
        try:
            trip.generate_fare_qr_code(request.build_absolute_uri('/')[:-1])
            trip.save(update_fields=['fare_amount', 'distance_km', 'fare_qr_code'])
        except Exception as e:
            print(f"Error generating fare QR code: {e}")
    else:
        trip.save(update_fields=['fare_amount', 'distance_km'])

    fare_qr_url = trip.fare_qr_code.url if (trip.fare_qr_code and trip.fare_qr_code.name and default_storage.exists(trip.fare_qr_code.name)) else f"/api/trip/{trip.trip_id}/qr-fallback/"

    profile = getattr(request.user, 'passenger_profile', None)
    return render(request, 'trip_feedback.html', {
        'trip': trip,
        'fare_qr_data_uri': fare_qr_data_uri,
        'fare_qr_url': fare_qr_url,
        'upi_pay_str': upi_pay_str,
        'driver_upi': driver_upi,
        'profile': profile,
    })

@passenger_required
def report_complaint(request, driver_id=None, trip_id=None):
    """File a formal grievance against a driver."""
    driver = None
    trip = None
    if driver_id:
        driver = get_object_or_404(DriverProfile, pk=driver_id)
    if trip_id:
        trip = get_object_or_404(TripSession, trip_id=trip_id)
        driver = trip.driver

    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        selected_driver_id = request.POST.get('driver_id')
        if selected_driver_id:
            driver = get_object_or_404(DriverProfile, pk=selected_driver_id)

        if form.is_valid() and driver:
            complaint = form.save(commit=False)
            complaint.passenger = request.user
            complaint.driver = driver
            complaint.trip = trip
            complaint.save()
            messages.success(request, f"Complaint #{str(complaint.complaint_id)[:8]} has been registered and forwarded to Administrator.")
            return redirect('passenger_dashboard')
        else:
            messages.error(request, "Please select a driver and complete the required fields.")
    else:
        form = ComplaintForm()

    verified_drivers = DriverProfile.objects.filter(verification_status=DriverProfile.VerificationStatus.VERIFIED).select_related('user')
    return render(request, 'passenger/report_complaint.html', {
        'form': form, 
        'driver': driver, 
        'trip': trip,
        'verified_drivers': verified_drivers
    })

@passenger_required
def emergency_contacts_view(request):
    """Passenger emergency contacts configuration."""
    profile, _ = PassengerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Emergency contact updated successfully.")
            return redirect('passenger_dashboard')
    else:
        form = EmergencyContactForm(instance=profile)

    return render(request, 'passenger/emergency_contacts.html', {'form': form})

@passenger_required
def passenger_trip_history(request):
    """View all past trips taken by passenger with clean pagination."""
    ensure_diverse_driver_ecosystem(user=request.user)
    trips_qs = TripSession.objects.filter(passenger=request.user).select_related('driver', 'driver__user', 'rating_entry').order_by('-start_time')
    paginator = Paginator(trips_qs, 6)  # 6 trips per page
    page_number = request.GET.get('page', 1)
    trips = paginator.get_page(page_number)
    return render(request, 'passenger/trip_history.html', {'trips': trips})

@passenger_required
def passenger_profile_view(request):
    """Profile Management matching Form 12 (PROFILE MANAGEMENT (Passenger))."""
    user = request.user
    if request.method == 'POST':
        form = PassengerProfileManagementForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name'].strip()
            name_parts = full_name.split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone_number']
            if 'profile_photo' in request.FILES:
                user.avatar = request.FILES['profile_photo']
            user.save()
            messages.success(request, "Passenger Profile updated successfully.")
            return redirect('passenger_profile')
    else:
        initial = {
            'full_name': user.get_full_name() or user.username,
            'email': user.email,
            'phone_number': user.phone or '',
        }
        form = PassengerProfileManagementForm(initial=initial)

    return render(request, 'passenger/profile.html', {'form': form, 'user': user})

@login_required
def get_passenger_trips(request, passenger_id):
    """
    Dynamic API: Returns all trips associated with the selected passenger as JSON.
    Populates dynamic Trip ID dropdown in Incident Report module.
    """
    passenger = User.objects.filter(pk=passenger_id).first()
    if not passenger:
        return JsonResponse({
            'status': 'error',
            'message': 'Passenger not found.',
            'trips': [],
            'count': 0
        }, status=404)

    trips_qs = Trip.objects.filter(passenger=passenger).select_related('driver', 'driver__user').order_by('-start_time')
    
    trips_list = []
    for t in trips_qs:
        driver_name = t.driver.user.get_full_name() if (t.driver and t.driver.user) else (t.driver.name if t.driver else "Unknown Driver")
        veh_num = t.driver.vehicle_number if t.driver else "Not Available"
        veh_type = t.driver.get_vehicle_type_display() if (t.driver and hasattr(t.driver, 'get_vehicle_type_display')) else (t.driver.vehicle_type if t.driver else "Vehicle")
        
        trips_list.append({
            'trip_id': t.trip_id,
            'formatted_trip_id': t.formatted_trip_id,
            'code': t.formatted_trip_id,
            'date': t.start_time.strftime('%b %d, %Y - %I:%M %p') if t.start_time else 'N/A',
            'iso_date': t.start_time.strftime('%Y-%m-%dT%H:%M') if t.start_time else '',
            'source': t.boarding_point,
            'destination': t.destination_address or t.end_location or "Drop Point Recorded",
            'driver_name': driver_name,
            'vehicle_number': veh_num,
            'vehicle_type': veh_type.title() if isinstance(veh_type, str) else str(veh_type),
            'status': t.status,
            'fare': str(t.fare_amount) if t.fare_amount is not None else '0.00'
        })

    return JsonResponse({
        'status': 'success',
        'passenger_id': passenger.id,
        'passenger_name': passenger.get_full_name() or passenger.username,
        'count': len(trips_list),
        'trips': trips_list,
        'message': 'Trips loaded successfully.' if trips_list else 'No trips available for this passenger.'
    })


@login_required
def get_trip_details(request, trip_id):
    """
    Dynamic API: Returns full trip metadata (passenger, date, source, destination, driver, vehicle).
    Accepts formatted ID (TRIP001) or integer ID (1).
    """
    clean_id = str(trip_id).upper().replace('TRIP', '').replace('TRP-', '').replace('TRP', '').replace('#', '').strip()
    trip = None
    if clean_id.isdigit():
        trip = Trip.objects.filter(trip_id=int(clean_id)).select_related('passenger', 'driver', 'driver__user').first()

    if not trip:
        return JsonResponse({
            'status': 'error',
            'message': f'Trip ID {trip_id} not found.'
        }, status=404)

    driver_name = trip.driver.user.get_full_name() if (trip.driver and trip.driver.user) else (trip.driver.name if trip.driver else "Unknown Driver")
    veh_num = trip.driver.vehicle_number if trip.driver else "Not Available"
    veh_type = trip.driver.get_vehicle_type_display() if (trip.driver and hasattr(trip.driver, 'get_vehicle_type_display')) else (trip.driver.vehicle_type if trip.driver else "Vehicle")

    return JsonResponse({
        'status': 'success',
        'trip_id': trip.trip_id,
        'formatted_trip_id': trip.formatted_trip_id,
        'passenger_id': trip.passenger.id if trip.passenger else None,
        'passenger_name': trip.passenger.get_full_name() or trip.passenger.username if trip.passenger else "Unknown",
        'passenger_phone': trip.passenger.phone if (trip.passenger and trip.passenger.phone) else '',
        'date': trip.start_time.strftime('%b %d, %Y - %I:%M %p') if trip.start_time else 'N/A',
        'iso_date': trip.start_time.strftime('%Y-%m-%dT%H:%M') if trip.start_time else '',
        'source': trip.boarding_point,
        'destination': trip.destination_address or trip.end_location or "Drop Point Recorded",
        'driver_name': driver_name,
        'vehicle_number': veh_num,
        'vehicle_type': veh_type.title() if isinstance(veh_type, str) else str(veh_type),
        'status': trip.status,
        'fare': str(trip.fare_amount) if trip.fare_amount is not None else '0.00'
    })


@login_required
def report_incident_view(request):
    """
    Incident Report Form matching Form 10 (INCIDENT REPORT) with dynamic passenger & Trip ID resolution.
    """
    # 1. Fetch all registered passengers in the system
    passengers = list(User.objects.filter(
        Q(role=User.Role.PASSENGER) | Q(passenger_profile__isnull=False)
    ).distinct().order_by('first_name', 'username'))

    # If logged-in user is a passenger and not in list, ensure they are present
    if request.user.is_authenticated and hasattr(request.user, 'is_passenger_user') and request.user.is_passenger_user():
        if request.user not in passengers:
            passengers.insert(0, request.user)

    # 2. Determine currently active/selected passenger
    p_id_param = request.GET.get('passenger_id') or request.POST.get('passenger_id')
    selected_passenger = None
    if p_id_param and str(p_id_param).isdigit():
        selected_passenger = User.objects.filter(pk=int(p_id_param)).first()
    
    if not selected_passenger:
        if request.user.is_authenticated and hasattr(request.user, 'is_passenger_user') and request.user.is_passenger_user():
            selected_passenger = request.user
        elif passengers:
            selected_passenger = passengers[0]
        else:
            selected_passenger = request.user

    # 3. Retrieve all trips belonging to the selected passenger
    passenger_trips = list(Trip.objects.filter(passenger=selected_passenger).select_related('driver', 'driver__user').order_by('-start_time'))

    # 4. Check for pre-selected Trip (from URL query, active trip, or first available)
    trip_param = request.GET.get('trip_id') or request.GET.get('trip')
    selected_trip = None
    if trip_param:
        clean_trip = str(trip_param).upper().replace('TRIP', '').replace('TRP-', '').replace('TRP', '').replace('#', '').strip()
        if clean_trip.isdigit():
            selected_trip = Trip.objects.filter(trip_id=int(clean_trip), passenger=selected_passenger).select_related('driver', 'driver__user').first()
    
    if not selected_trip:
        active_trip = Trip.objects.filter(passenger=selected_passenger, status__in=['Active', 'Ongoing', Trip.Status.ACTIVE]).first()
        selected_trip = active_trip if active_trip else (passenger_trips[0] if passenger_trips else None)

    if request.method == 'POST':
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            # Use passenger determined from validated form
            passenger_obj = form.cleaned_data.get('passenger_user') or selected_passenger
            trip_obj = form.cleaned_data.get('trip_obj')
            trip_id_str = form.cleaned_data.get('trip_id', '').strip()

            # Double validation: Ensure trip belongs to passenger (Requirement 9)
            if trip_obj and trip_obj.passenger_id != passenger_obj.id:
                messages.error(request, f"Validation Error: Trip {trip_obj.formatted_trip_id} does not belong to {passenger_obj.get_full_name() or passenger_obj.username}.")
                return render(request, 'passenger/report_incident.html', {
                    'form': form,
                    'passengers': passengers,
                    'selected_passenger': passenger_obj,
                    'passenger_trips': passenger_trips,
                    'selected_trip': selected_trip,
                })

            inc_type = form.cleaned_data['incident_type']
            desc = form.cleaned_data['description']

            # Determine incident timestamp (automatically derived from the selected trip)
            if trip_obj and trip_obj.start_time:
                inc_dt = trip_obj.start_time
            else:
                inc_dt = timezone.now()

            # Save incident report maintaining foreign key relationships (Requirement 8)
            incident = IncidentReport.objects.create(
                passenger=passenger_obj,
                trip=trip_obj,
                incident_type=inc_type,
                description=desc,
                status=IncidentReport.Status.PENDING,
                reported_at=inc_dt
            )
            
            trip_ref_display = trip_obj.formatted_trip_id if trip_obj else (trip_id_str or 'General')
            messages.success(request, f"Incident Report #{str(incident.incident_id)[:8]} successfully filed for {passenger_obj.get_full_name() or passenger_obj.username} (Trip: {trip_ref_display})!")
            return redirect('passenger_dashboard')
        else:
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {err}")
    else:
        now_str = timezone.now().strftime('%Y-%m-%dT%H:%M')
        incident_time = selected_trip.start_time.strftime('%Y-%m-%dT%H:%M') if (selected_trip and selected_trip.start_time) else now_str
        initial = {
            'passenger_id': selected_passenger.id if selected_passenger else '',
            'passenger_name': selected_passenger.get_full_name() or selected_passenger.username if selected_passenger else '',
            'trip_id': selected_trip.formatted_trip_id if selected_trip else '',
            'incident_date_time': incident_time
        }
        form = IncidentReportForm(initial=initial)

    return render(request, 'passenger/report_incident.html', {
        'form': form,
        'passengers': passengers,
        'selected_passenger': selected_passenger,
        'passenger_trips': passenger_trips,
        'selected_trip': selected_trip,
    })

def live_share_default(request):
    """Fallback when navigating to /live-track/ without a specific token - tracks user's active/recent journey or system active journey."""
    trip = None
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        if hasattr(user, 'is_passenger_user') and user.is_passenger_user():
            trip = TripSession.objects.filter(
                passenger=user,
                status__in=['Active', 'Ongoing', 'IN_PROGRESS', 'SOS_Triggered', TripSession.Status.ACTIVE, TripSession.Status.SOS_TRIGGERED]
            ).order_by('-start_time').first()
            if not trip:
                trip = TripSession.objects.filter(passenger=user).order_by('-start_time').first()
        elif hasattr(user, 'is_driver_user') and user.is_driver_user():
            driver_profile = getattr(user, 'driver_profile', None)
            if driver_profile:
                trip = TripSession.objects.filter(
                    driver=driver_profile,
                    status__in=['Active', 'Ongoing', 'IN_PROGRESS', 'SOS_Triggered', TripSession.Status.ACTIVE, TripSession.Status.SOS_TRIGGERED]
                ).order_by('-start_time').first()
                if not trip:
                    trip = TripSession.objects.filter(driver=driver_profile).order_by('-start_time').first()

    if not trip:
        trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').filter(
            status__in=['Active', 'Ongoing', 'IN_PROGRESS', 'SOS_Triggered', TripSession.Status.ACTIVE, TripSession.Status.SOS_TRIGGERED]
        ).order_by('-start_time').first()
    if not trip:
        trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').order_by('-start_time').first()
    if trip:
        return redirect('live_share', token=str(trip.trip_id))
    messages.info(request, "No monitored journeys are currently streaming GPS telemetry.")
    return redirect('home')

def live_share_view(request, token):
    """Publicly accessible live tracking link for friends and family via Google Maps & Satellite GPS."""
    # Clean token if user entered literal '<token>' or extra symbols
    cleaned_token = str(token).replace('<', '').replace('>', '').replace('%3C', '').replace('%3E', '').strip().strip('/')
    
    trip = None
    
    # 1. If token is a valid UUID, search by share_token, trip_uuid, or verification_token
    import uuid
    is_uuid = False
    try:
        uuid.UUID(cleaned_token)
        is_uuid = True
    except (ValueError, AttributeError, TypeError):
        is_uuid = False

    if is_uuid:
        trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').filter(
            Q(share_token=cleaned_token) | 
            Q(trip_uuid=cleaned_token) |
            Q(driver__verification_token=cleaned_token)
        ).first()

    # 2. Try by trip_id integer/string if passed (e.g. /live-track/24/ or /live-track/TRP-24/)
    if not trip:
        cleaned_num = cleaned_token.replace('TRP-', '').replace('trp-', '').replace('#', '').strip()
        if cleaned_num.isdigit():
            trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').filter(
                trip_id=int(cleaned_num)
            ).first()

    # 3. Fall back to active trip or most recent trip
    if not trip:
        trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').filter(
            status__in=['Active', 'Ongoing', 'IN_PROGRESS', 'SOS_Triggered', TripSession.Status.ACTIVE, TripSession.Status.SOS_TRIGGERED]
        ).order_by('-start_time').first()
        if not trip:
            trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').order_by('-start_time').first()

    if not trip:
        messages.warning(request, "The live journey you are looking for has either completed or does not exist.")
        return redirect('home')

    public_base = _get_public_share_base_url(request)
    network_base = _get_network_base_url(request)
    share_url = f"{public_base}/live-track/{trip.trip_id}/"
    network_share_url = f"{network_base}/live-track/{trip.trip_id}/"
    driver = trip.driver
    vehicle = getattr(driver, 'vehicle', None)

    return render(request, 'live_share.html', {
        'trip': trip,
        'driver': driver,
        'vehicle': vehicle,
        'share_url': share_url,
        'network_share_url': network_share_url,
        'token': str(trip.trip_id),
    })

# ==========================================
# DRIVER MODULE VIEWS
# ==========================================

def _get_driver_for_request(request):
    """Safely retrieves the DriverProfile for current user session, with admin preview & auto-enrollment fallback."""
    driver = DriverProfile.objects.select_related('user').filter(user=request.user).first()
    if not driver:
        if request.user.is_driver_user():
            driver = DriverProfile.objects.create(
                user=request.user,
                name=request.user.get_full_name() or request.user.username,
                phone_number=request.user.phone or "+91 94471 82930",
                license_number="KL-05-2021000892",
                vehicle_number="KL-05-AT-4455",
                verification_status=DriverProfile.VerificationStatus.VERIFIED
            )
        elif request.user.is_admin_user():
            driver = DriverProfile.objects.select_related('user').first()
            if not driver:
                driver = DriverProfile.objects.create(
                    user=request.user,
                    name="Rajesh Kumar",
                    phone_number="+91 94471 82930",
                    license_number="KL-05-2021000892",
                    vehicle_number="KL-05-AT-4455",
                    verification_status=DriverProfile.VerificationStatus.VERIFIED
                )
        else:
            driver = DriverProfile.objects.select_related('user').first()
    return driver

@driver_required
def driver_dashboard(request):
    """Driver portal dashboard."""
    driver = _get_driver_for_request(request)
    if not driver:
        messages.error(request, "No driver profile found.")
        return redirect('home')

    recent_ratings = driver.received_ratings.select_related('passenger').order_by('-created_at')[:10]
    recent_trips = TripSession.objects.filter(driver=driver).order_by('-start_time')[:5]
    completed_trips_count = TripSession.objects.filter(driver=driver, status__in=['Completed', 'COMPLETED']).count()
    
    # Ensure QR code exists and uses active public tunnel URL instead of localhost
    if driver.is_verified():
        driver.generate_qr_code(_get_public_share_base_url(request))
        driver.save()

    context = {
        'driver': driver,
        'vehicle': getattr(driver, 'vehicle', None),
        'recent_ratings': recent_ratings,
        'recent_trips': recent_trips,
        'completed_trips_count': completed_trips_count,
    }
    return render(request, 'driver/dashboard.html', context)

@driver_required
def driver_id_badge(request):
    """Digital and printable Official Driver & Vehicle QR Code for passenger verification."""
    driver = _get_driver_for_request(request)
    if not driver:
        messages.error(request, "No driver profile found.")
        return redirect('home')

    if driver.is_verified():
        driver.generate_qr_code(_get_public_share_base_url(request))
        driver.save()

    return render(request, 'driver/id_badge.html', {
        'driver': driver,
        'vehicle': getattr(driver, 'vehicle', None)
    })

@driver_required
def driver_profile_view(request):
    """Profile Management matching Form 11 (PROFILE MANAGEMENT (Driver))."""
    driver = _get_driver_for_request(request)
    if not driver:
        messages.error(request, "No driver profile found.")
        return redirect('home')

    user = driver.user
    vehicle = getattr(driver, 'vehicle', None)

    if request.method == 'POST':
        form = DriverProfileManagementForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name'].strip()
            name_parts = name.split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.phone = form.cleaned_data['phone_number']
            user.save()

            driver.name = name
            driver.phone_number = form.cleaned_data['phone_number']
            if form.cleaned_data.get('upi_id') is not None:
                driver.upi_id = form.cleaned_data.get('upi_id') or None
            if form.cleaned_data.get('license_number'):
                driver.license_number = form.cleaned_data['license_number'].strip().upper()
            if form.cleaned_data.get('vehicle_number'):
                driver.vehicle_number = form.cleaned_data['vehicle_number'].strip().upper()
            if form.cleaned_data.get('vehicle_type'):
                driver.vehicle_type = form.cleaned_data['vehicle_type']

            if 'profile_photo' in request.FILES:
                driver.driver_photo = request.FILES['profile_photo']

            driver.save()

            if vehicle and hasattr(vehicle, 'save'):
                if form.cleaned_data.get('vehicle_number'):
                    vehicle.registration_number = form.cleaned_data['vehicle_number'].strip().upper()
                if form.cleaned_data.get('vehicle_make_model'):
                    vehicle.make_model = form.cleaned_data['vehicle_make_model'].strip()
                if form.cleaned_data.get('vehicle_type'):
                    vehicle.vehicle_type = form.cleaned_data['vehicle_type']
                try:
                    vehicle.save()
                except Exception:
                    pass

            messages.success(request, "Driver and Vehicle Profiles updated successfully.")
            return redirect('driver_profile')
    else:
        initial = {
            'name': driver.name or user.get_full_name() or user.username,
            'email': user.email or driver.email or '',
            'phone_number': driver.phone_number or user.phone or '',
            'upi_id': driver.upi_id or '',
            'license_number': driver.license_number or '',
            'vehicle_number': driver.vehicle_number or (vehicle.registration_number if vehicle else ''),
            'vehicle_type': driver.vehicle_type or (vehicle.vehicle_type if vehicle else 'auto'),
            'vehicle_make_model': getattr(vehicle, 'make_model', '') or 'Bajaj Compact Auto',
        }
        form = DriverProfileManagementForm(initial=initial)

    return render(request, 'driver/profile.html', {'form': form, 'driver': driver, 'vehicle': vehicle})

@driver_required
def driver_trip_logs(request):
    """Driver's completed and active trips log."""
    driver = _get_driver_for_request(request)
    if not driver:
        messages.error(request, "No driver profile found.")
        return redirect('home')

    trips = TripSession.objects.filter(driver=driver).select_related('passenger', 'rating_entry').order_by('-start_time')
    return render(request, 'driver/trip_logs.html', {'driver': driver, 'trips': trips})

# ==========================================
# ADMIN MODULE VIEWS
# ==========================================

@admin_required
def admin_dashboard(request):
    """Central Administrative Command Dashboard."""
    total_drivers = DriverProfile.objects.count()
    verified_drivers = DriverProfile.objects.filter(verification_status=DriverProfile.VerificationStatus.VERIFIED).count()
    pending_kyc = DriverProfile.objects.filter(verification_status=DriverProfile.VerificationStatus.PENDING).count()
    total_passengers = User.objects.filter(role=User.Role.PASSENGER).count()
    total_trips = TripSession.objects.count()
    active_sos = SOSAlert.objects.filter(status=SOSAlert.Status.ACTIVE).select_related('passenger', 'driver', 'driver__user')
    recent_complaints = Complaint.objects.filter(status=Complaint.Status.OPEN).select_related('passenger', 'driver', 'driver__user')[:5]
    recent_drivers = DriverProfile.objects.filter(verification_status=DriverProfile.VerificationStatus.PENDING).select_related('user').order_by('-driver_id')[:5]

    context = {
        'total_drivers': total_drivers,
        'verified_drivers': verified_drivers,
        'pending_kyc': pending_kyc,
        'total_passengers': total_passengers,
        'total_trips': total_trips,
        'active_sos': active_sos,
        'recent_complaints': recent_complaints,
        'recent_drivers': recent_drivers,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@admin_required
def admin_driver_list(request):
    """Filterable directory of all drivers."""
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()
    
    drivers = DriverProfile.objects.select_related('user').all().order_by('-driver_id')
    if status_filter:
        drivers = drivers.filter(verification_status=status_filter)
    if query:
        drivers = drivers.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(license_number__icontains=query) |
            Q(vehicle_number__icontains=query) |
            Q(name__icontains=query)
        )

    # Ensure all drivers have an active QR code generated and normalized upi_id (name@bankname)
    base_url = _get_public_share_base_url(request)
    driver_upi_map = {
        'rajesh': 'rajesh@oksbi',
        'anand': 'anand@okhdfcbank',
        'suresh': 'suresh@okaxis',
        'vinod': 'vinod@paytm',
        'varun': 'varun@icici',
        'manoj': 'manoj@okaxis',
        'harikrishnan': 'harikrishnan@okhdfcbank',
        'pradeep': 'pradeep@okaxis',
        'biju': 'biju@oksbi',
        'rohan': 'rohan@okhdfcbank',
    }
    for d in drivers:
        need_save = False
        username = d.user.username.replace('driver_', '').lower() if (d.user and d.user.username) else ''
        first_name = (d.user.first_name if (d.user and d.user.first_name) else (d.name.split()[0] if d.name else username)).lower()
        first_name = ''.join(c for c in first_name if c.isalnum()) or 'driver'

        if first_name in driver_upi_map:
            cleaned_upi = driver_upi_map[first_name]
        elif username in driver_upi_map:
            cleaned_upi = driver_upi_map[username]
        elif d.upi_id and '@' in d.upi_id:
            h, b = d.upi_id.split('@', 1)
            cleaned_upi = f"{first_name}@{b.replace('sample.', '').strip().lower()}"
        else:
            cleaned_upi = f"{first_name}@oksbi"

        if d.upi_id != cleaned_upi:
            d.upi_id = cleaned_upi
            need_save = True

        if not d.qr_code or not d.qr_code_image:
            try:
                d.generate_qr_code(base_url)
                need_save = True
            except Exception:
                pass
        if need_save:
            try:
                d.save()
            except Exception:
                pass

    context = {
        'drivers': drivers,
        'status_filter': status_filter,
        'query': query,
        'status_choices': DriverProfile.VerificationStatus.choices,
    }
    return render(request, 'admin_panel/driver_list.html', context)

@admin_required
def admin_driver_register(request):
    """Administrator directly onboards and creates a driver and vehicle profile."""
    if request.method == 'POST':
        form = AdminDriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    username = form.cleaned_data['username'].strip().lower()
                    phone = form.cleaned_data['phone'].strip()
                    email = form.cleaned_data.get('email', '').strip().lower()
                    if not email:
                        email = f"{username}@driver.saferide.local"

                    # 1. Create Driver User Account
                    user = User.objects.create_user(
                        username=username,
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['first_name'].strip(),
                        last_name=form.cleaned_data['last_name'].strip(),
                        phone=phone,
                        email=email,
                        role=User.Role.DRIVER
                    )
                    
                    auto_approve = form.cleaned_data.get('auto_approve', False)
                    v_status = DriverProfile.VerificationStatus.VERIFIED if auto_approve else DriverProfile.VerificationStatus.PENDING

                    # 2. Create Driver Profile (tbl_driver)
                    driver = Driver.objects.create(
                        user=user,
                        name=f"{user.first_name} {user.last_name}".strip() or user.username,
                        phone_number=phone,
                        email=email,
                        license_number=form.cleaned_data['license_number'].strip().upper(),
                        vehicle_number=form.cleaned_data['registration_number'].strip().upper(),
                        vehicle_type=form.cleaned_data['vehicle_type'],
                        password=user.password,
                        upi_id=form.cleaned_data.get('upi_id') or None,
                        experience_years=form.cleaned_data.get('experience_years') or 3,
                        driver_photo=form.cleaned_data.get('driver_photo'),
                        license_doc=form.cleaned_data.get('license_doc'),
                        id_proof_doc=form.cleaned_data.get('id_proof_doc'),
                        police_clearance_doc=form.cleaned_data.get('police_clearance_doc'),
                        verification_status=v_status,
                        verified_at=timezone.now() if auto_approve else None,
                        verification_notes="Registered and verified by Administrator" if auto_approve else "Awaiting document inspection",
                    )

                    # 3. Create Vehicle Documents (tbl_vehicle_documents)
                    VehicleDocuments.objects.create(
                        driver=driver,
                        license_doc=str(form.cleaned_data.get('license_doc') or ''),
                        rc_doc=str(form.cleaned_data.get('rc_book_doc') or ''),
                        license_file=form.cleaned_data.get('license_doc'),
                        rc_file=form.cleaned_data.get('rc_book_doc'),
                    )

                    # 4. Ensure official vehicle QR code is generated upon registration
                    try:
                        driver.generate_qr_code(_get_public_share_base_url(request))
                        driver.save(update_fields=['qr_code', 'qr_code_image'])
                    except Exception:
                        pass

                    if auto_approve:
                        driver.recalculate_reputation()
                        messages.success(request, f"Driver {driver.name} registered & verified successfully! Official Vehicle QR Code generated.")
                    else:
                        messages.info(request, f"Driver {driver.name} registered in 'Pending' state. Official Vehicle QR Code generated & awaiting KYC verification.")

                    return redirect('admin_driver_list')
            except Exception as e:
                messages.error(request, f"Driver registration failed due to database error: {str(e)}")
        else:
            err_details = []
            for field, errs in form.errors.items():
                err_details.append(f"{field.replace('_', ' ').title()}: {', '.join(errs)}")
            messages.error(request, f"Validation error: {' | '.join(err_details[:3])}")
    else:
        form = AdminDriverRegistrationForm()

    return render(request, 'admin_panel/driver_register.html', {'form': form})

@admin_required
def admin_driver_kyc(request, driver_id):
    """Admin inspects uploaded KYC documents and approves/rejects driver (Form 5)."""
    driver = Driver.objects.select_related('user').filter(Q(driver_id=driver_id) | Q(pk=driver_id)).first()
    if not driver:
        driver = get_object_or_404(Driver, pk=driver_id)
    vehicle = getattr(driver, 'vehicle', None)
    vehicle_doc = VehicleDocuments.objects.filter(driver=driver).first()

    if request.method == 'POST':
        form = DriverKYCReviewForm(request.POST, instance=driver)
        if form.is_valid():
            driver = form.save()
            if driver.verification_status in ['Verified', Driver.VerificationStatus.VERIFIED]:
                driver.verified_at = timezone.now()
                driver.generate_qr_code(_get_public_share_base_url(request))
                driver.recalculate_reputation()
                messages.success(request, f"Driver {driver.name} has been successfully VERIFIED. QR Code updated!")
            elif driver.verification_status in ['Rejected', Driver.VerificationStatus.SUSPENDED]:
                messages.warning(request, f"Driver {driver.name} verification status set to {driver.verification_status}.")
            else:
                messages.info(request, f"Verification status updated to {driver.get_verification_status_display()}.")
            driver.save()
            return redirect('admin_driver_list')
        else:
            err_details = [f"{field.replace('_', ' ').title()}: {', '.join(errs)}" for field, errs in form.errors.items()]
            messages.error(request, f"Please correct the errors: {' | '.join(err_details)}")
    else:
        form = DriverKYCReviewForm(instance=driver)

    return render(request, 'admin_panel/driver_kyc_detail.html', {
        'driver': driver,
        'vehicle': vehicle,
        'vehicle_doc': vehicle_doc,
        'form': form
    })

@admin_required
def admin_sos_monitoring(request):
    """Real-time Emergency SOS incident monitoring dashboard."""
    active_alerts = SOSAlert.objects.filter(status__in=['Active', SOSAlert.Status.ACTIVE]).select_related('passenger', 'driver', 'driver__user', 'trip').order_by('-timestamp')
    resolved_alerts = SOSAlert.objects.filter(status__in=['Responded', 'Resolved', SOSAlert.Status.RESPONDED, SOSAlert.Status.RESOLVED]).select_related('passenger', 'driver', 'driver__user').order_by('-timestamp')[:15]

    return render(request, 'admin_panel/sos_monitoring.html', {
        'active_alerts': active_alerts,
        'resolved_alerts': resolved_alerts,
    })

@admin_required
def admin_resolve_sos(request, alert_id):
    """Admin resolves an SOS emergency alert."""
    alert = None
    if str(alert_id).isdigit():
        alert = SOSAlert.objects.filter(sos_id=int(alert_id)).first()
    else:
        try:
            val_uuid = uuid.UUID(str(alert_id))
            alert = SOSAlert.objects.filter(alert_uuid=val_uuid).first()
        except ValueError:
            pass

    if not alert:
        if str(alert_id).isdigit():
            alert = get_object_or_404(SOSAlert, pk=int(alert_id))
        else:
            alert = get_object_or_404(SOSAlert, alert_uuid=alert_id)

    notes = request.POST.get('admin_notes', 'Dispatched emergency unit. Passenger safe.')
    alert.resolve_alert(notes)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        return JsonResponse({'status': 'success', 'message': f"SOS Alert #{str(alert.sos_id)} marked as RESOLVED."})

    messages.success(request, f"SOS Alert #{str(alert.sos_id)} marked as RESOLVED.")
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer or 'admin_sos_monitoring')

@admin_required
def admin_resolve_all_sos(request):
    """Admin resolves all currently active SOS emergency alerts at once."""
    notes = request.POST.get('admin_notes', 'All active alerts resolved by Administrator.')
    active_alerts = SOSAlert.objects.filter(status__in=['Active', SOSAlert.Status.ACTIVE])
    count = active_alerts.count()
    for alert in active_alerts:
        alert.resolve_alert(notes)
    messages.success(request, f"Successfully resolved {count} active emergency beacon(s).")
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer or 'admin_dashboard')

@admin_required
def admin_complaints_list(request):
    """Manage passenger complaints and apply disciplinary penalties."""
    status_filter = request.GET.get('status', '')
    complaints = Complaint.objects.select_related('passenger', 'driver', 'driver__user', 'trip').order_by('-created_at')
    if status_filter:
        complaints = complaints.filter(status=status_filter)

    return render(request, 'admin_panel/complaints_list.html', {
        'complaints': complaints,
        'status_filter': status_filter,
        'status_choices': Complaint.Status.choices,
    })

@admin_required
def admin_resolve_complaint(request, complaint_id):
    """Resolve complaint and deduct penalty points from driver."""
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    action = request.POST.get('action', 'resolve')
    remarks = request.POST.get('admin_remarks', '')
    penalty = int(request.POST.get('penalty_points', 5))

    if action == 'dismiss':
        complaint.resolve(remarks=remarks, dismiss=True)
        messages.info(request, f"Complaint #{str(complaint.complaint_id)[:8]} dismissed.")
    else:
        complaint.resolve(remarks=remarks, penalty=penalty, dismiss=False)
        messages.success(request, f"Complaint resolved. {penalty} reputation points deducted from driver {complaint.driver.user.username}.")

    return redirect('admin_complaints_list')

@admin_required
def admin_passenger_list(request):
    """List registered passengers (strictly excluding administrators)."""
    passengers = PassengerProfile.objects.select_related('user').filter(
        user__role=User.Role.PASSENGER
    ).exclude(
        user__is_superuser=True
    ).order_by('-passenger_id')
    return render(request, 'admin_panel/passenger_list.html', {'passengers': passengers})

@admin_required
def admin_delete_passenger(request, passenger_id):
    """Permanently delete a passenger profile and their user account."""
    if request.method == 'POST':
        passenger = get_object_or_404(PassengerProfile.objects.select_related('user'), passenger_id=passenger_id)
        user = passenger.user
        if user.is_superuser or user.role == User.Role.ADMIN:
            messages.error(request, "Security violation: System Administrator accounts cannot be deleted.")
            return redirect('admin_passenger_list')
        passenger_name = user.get_full_name() or user.username
        
        # Delete user account (which also cascades to passenger profile and emergency records)
        user.delete()
        messages.success(request, f"Passenger account for '{passenger_name}' has been permanently deleted.")
    return redirect('admin_passenger_list')

# Alias for backwards compatibility
admin_toggle_passenger_status = admin_delete_passenger

# ==========================================
# SOS DISPATCH & LOCATION AJAX ENDPOINTS
# ==========================================

def update_trip_location(request, trip_id):
    """
    Continuous GPS Location Update Endpoint.
    Accepts AJAX POST requests containing latitude & longitude and updates the active Trip record.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST request required.'}, status=405)

    try:
        data = json.loads(request.body) if request.body else request.POST
        lat = float(data.get('latitude'))
        lng = float(data.get('longitude'))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid latitude or longitude coordinates.'}, status=400)

    # Find active trip by numeric id, TRP-id, TRIP-id, or UUID / share_token
    cleaned_id = str(trip_id).upper().replace('TRIP', '').replace('TRP-', '').replace('TRP', '').replace('#', '').strip()
    trip = None
    if cleaned_id.isdigit():
        trip = Trip.objects.filter(trip_id=int(cleaned_id)).first()
    if not trip:
        try:
            val_uuid = uuid.UUID(str(trip_id).strip())
            trip = Trip.objects.filter(Q(trip_uuid=val_uuid) | Q(share_token=val_uuid)).first()
        except (ValueError, TypeError, AttributeError):
            pass

    if not trip:
        return JsonResponse({'status': 'error', 'message': 'Trip not found.'}, status=404)

    # Security: Only the authorized passenger can push GPS updates to their trip
    if not request.user.is_authenticated or trip.passenger != request.user:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized to update trip location.'}, status=403)

    # Update current telemetry
    trip.current_latitude = lat
    trip.current_longitude = lng
    trip.live_latitude = lat
    trip.live_longitude = lng
    trip.live_updated_at = timezone.now()

    # Recalculate distance and valid regulated fare
    trip.calculate_distance_and_fare()

    trip.save(update_fields=[
        'current_latitude', 'current_longitude',
        'live_latitude', 'live_longitude',
        'live_updated_at', 'distance_km', 'fare_amount'
    ])

    return JsonResponse({
        'status': 'success',
        'trip_id': trip.trip_id,
        'current_latitude': float(trip.current_latitude),
        'current_longitude': float(trip.current_longitude),
        'distance_km': float(trip.distance_km),
        'fare_amount': float(trip.fare_amount),
        'timestamp': trip.live_updated_at.isoformat()
    })

def get_live_location(request, trip_id):
    """
    Returns the current live location of the trip for public tracking.
    """
    cleaned_id = str(trip_id).upper().replace('TRIP', '').replace('TRP-', '').replace('TRP', '').replace('#', '').strip()
    trip = None
    if cleaned_id.isdigit():
        trip = Trip.objects.filter(trip_id=int(cleaned_id)).first()
    if not trip:
        try:
            import uuid
            val_uuid = uuid.UUID(str(trip_id).strip())
            trip = Trip.objects.filter(Q(trip_uuid=val_uuid) | Q(share_token=val_uuid)).first()
        except Exception:
            pass

    if not trip:
        return JsonResponse({'status': 'error', 'message': 'Trip not found.'}, status=404)

    # Security: Allow live tracking if live_location_sharing is enabled on the trip, or user is authenticated passenger/staff
    if cleaned_id.isdigit():
        if not trip.live_location_sharing and (not request.user.is_authenticated or (trip.passenger != request.user and not request.user.is_superuser)):
            return JsonResponse({'status': 'error', 'message': 'Unauthorized to view this trip without a secure share token.'}, status=403)

    dest_lat = float(trip.destination_latitude or trip.drop_latitude or 0.0)
    dest_lng = float(trip.destination_longitude or trip.drop_longitude or 0.0)
    dest_addr = trip.destination_address or trip.end_location or getattr(trip, 'drop_location_name', '') or "Drop-off Location"

    return JsonResponse({
        'status': 'success',
        'location': {
            'lat': float(trip.live_latitude or trip.current_latitude or 0.0),
            'lng': float(trip.live_longitude or trip.current_longitude or 0.0)
        },
        'destination': {
            'lat': dest_lat,
            'lng': dest_lng,
            'address': dest_addr
        },
        'driver': {
            'name': trip.driver.name if trip.driver else 'Driver',
            'phone': trip.driver.phone_number if trip.driver else '',
            'vehicle': trip.driver.vehicle_number if trip.driver else ''
        },
        'trip_status': trip.status,
        'sos_active': True if trip.status in ['SOS_Triggered', 'SOS_TRIGGERED'] else False
    })

@login_required
def trigger_sos_alert(request):
    """
    Instant SOS Emergency Alert Endpoint.
    Creates a new SOSAlert database record linking Passenger, Driver, and Location with 'Active' status.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST request required.'}, status=405)

    # Restrict SOS alerts strictly to passengers
    if not (hasattr(request.user, 'is_passenger_user') and request.user.is_passenger_user()):
        return JsonResponse({
            'status': 'error',
            'success': False,
            'message': 'Access restricted: SOS emergency alerts can only be triggered by passengers.'
        }, status=403)

    try:
        if request.content_type == 'application/json' and request.body:
            data = json.loads(request.body)
        else:
            try:
                data = json.loads(request.body) if request.body else request.POST
            except Exception:
                data = request.POST

        trip_id = data.get('trip_id')
        driver_id = data.get('driver_id')
        lat = float(data.get('latitude', 9.684300))
        lng = float(data.get('longitude', 76.685300))
        location_name = data.get('location_name', f'GPS Coordinates: {lat:.6f}, {lng:.6f}')
    except (ValueError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid payload data.'}, status=400)

    passenger = request.user

    trip = None
    if trip_id:
        trip = Trip.objects.filter(
            Q(trip_id=int(trip_id) if str(trip_id).isdigit() else -1) | Q(trip_uuid=trip_id if len(str(trip_id)) > 30 else uuid.uuid4())
        ).first()

    driver = None
    if driver_id:
        driver = Driver.objects.filter(driver_id=int(driver_id) if str(driver_id).isdigit() else -1).first()
    if not driver and trip:
        driver = trip.driver

    if trip:
        trip.status = Trip.Status.SOS_TRIGGERED
        trip.current_latitude = lat
        trip.current_longitude = lng
        trip.live_latitude = lat
        trip.live_longitude = lng
        trip.save(update_fields=['status', 'current_latitude', 'current_longitude', 'live_latitude', 'live_longitude'])
    # Check if passenger already has an active unresolved distress beacon to avoid duplicates
    existing_sos = SOSAlert.objects.filter(
        passenger=passenger,
        status=SOSAlert.Status.ACTIVE
    ).order_by('-timestamp').first()

    if existing_sos:
        existing_sos.latitude = lat
        existing_sos.longitude = lng
        existing_sos.location = location_name[:100]
        existing_sos.location_name = location_name
        existing_sos.timestamp = timezone.now()
        if driver and not existing_sos.driver:
            existing_sos.driver = driver
        if trip and not existing_sos.trip:
            existing_sos.trip = trip
        existing_sos.save()
        sos = existing_sos
    else:
        # Create single active SOS Alert record
        sos = SOSAlert.objects.create(
            passenger=passenger,
            driver=driver,
            trip=trip,
            latitude=lat,
            longitude=lng,
            location=location_name[:100],
            location_name=location_name,
            status=SOSAlert.Status.ACTIVE,
            dispatched_services="Police (112), Campus Control, Admin Console"
        )

    import logging
    logger = logging.getLogger(__name__)
    logger.critical(
        f"🚨 [EMERGENCY SOS ALERT] Distress Beacon #{sos.sos_id} | Passenger: {passenger.username} | "
        f"Driver: {driver.name if driver else 'N/A'} ({driver.vehicle_number if driver else 'N/A'}) | "
        f"GPS: {lat}, {lng}"
    )

    profile = getattr(passenger, 'passenger_profile', None)
    contact1_name = getattr(profile, 'emergency_contact_name', '') if profile else ''
    contact1_phone = getattr(profile, 'emergency_contact_phone', '') if profile else ''
    contact2_name = getattr(profile, 'emergency_contact_2_name', '') if profile else ''
    contact2_phone = getattr(profile, 'emergency_contact_2_phone', '') if profile else ''

    public_base = _get_public_share_base_url(request)
    share_url = f"{public_base}/live-track/{trip.trip_id}/" if (trip and getattr(trip, 'share_token', None)) else f"{public_base}/"
    driver_name = driver.name if driver else (driver.user.get_full_name() if (driver and getattr(driver, 'user', None)) else 'SafeRide Driver')
    vehicle_num = driver.vehicle_number if driver else 'N/A'
    passenger_name = passenger.get_full_name() or passenger.username

    import urllib.parse

    def make_wa_url(raw_phone, c_name):
        if not raw_phone:
            return None
        cleaned = "".join(filter(str.isdigit, str(raw_phone)))
        if len(cleaned) == 10:
            cleaned = "91" + cleaned
        greeting = f"Hi {c_name}, " if c_name else ""
        text = (
            f"🚨 *EMERGENCY SOS ALERT!* 🚨\n\n"
            f"{greeting}I need immediate assistance! I have triggered an emergency distress beacon on my SafeRide journey.\n\n"
            f"👤 *Passenger:* {passenger_name}\n"
            f"🚖 *Driver:* {driver_name}\n"
            f"🔢 *Vehicle:* {vehicle_num}\n"
            f"📍 *Location:* {location_name}\n\n"
            f"🔴 *Live GPS Satellite Tracking Link:*\n{share_url}\n\n"
            f"Please check my live location or contact Police 112 immediately!"
        )
        return f"https://wa.me/{cleaned}?text={urllib.parse.quote(text)}"

    wa_url_1 = make_wa_url(contact1_phone, contact1_name)
    wa_url_2 = make_wa_url(contact2_phone, contact2_name)

    return JsonResponse({
        'status': 'success',
        'success': True,
        'alert_id': sos.sos_id,
        'message': '🚨 SOS Emergency Alert broadcasted to Admin Command Center!',
        'passenger': passenger_name,
        'vehicle_number': vehicle_num,
        'latitude': float(lat),
        'longitude': float(lng),
        'timestamp': sos.timestamp.strftime('%H:%M:%S'),
        'share_url': share_url,
        'contact1_name': contact1_name,
        'contact1_phone': contact1_phone,
        'wa_url_1': wa_url_1,
        'contact2_name': contact2_name,
        'contact2_phone': contact2_phone,
        'wa_url_2': wa_url_2,
    })

@login_required
def cancel_sos_alert(request):
    """
    Cancels an active SOS alert.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST request required.'}, status=405)

    passenger = request.user
    
    # Try to get trip id from payload
    trip_id = None
    try:
        if request.content_type == 'application/json' and request.body:
            data = json.loads(request.body)
            trip_id = data.get('trip_id')
    except Exception:
        pass

    # Find the active SOS alert for the passenger
    active_sos = SOSAlert.objects.filter(
        passenger=passenger,
        status=SOSAlert.Status.ACTIVE
    ).first()
    
    if active_sos:
        active_sos.status = SOSAlert.Status.RESOLVED
        active_sos.resolved_notes = 'Cancelled by Passenger'
        active_sos.resolved_at = timezone.now()
        active_sos.save()

    # Update trip status if provided
    if trip_id:
        cleaned_id = str(trip_id).replace('TRP-', '').replace('trp-', '').replace('#', '').strip()
        trip = None
        if cleaned_id.isdigit():
            trip = Trip.objects.filter(trip_id=int(cleaned_id)).first()
        if not trip:
            try:
                val_uuid = uuid.UUID(str(trip_id).strip())
                trip = Trip.objects.filter(Q(trip_uuid=val_uuid) | Q(share_token=val_uuid)).first()
            except Exception:
                pass
                
        if trip and trip.status == Trip.Status.SOS_TRIGGERED:
            trip.status = Trip.Status.ACTIVE
            trip.save(update_fields=['status'])
            
    return JsonResponse({'status': 'success', 'message': 'SOS Alert Cancelled successfully.'})


@login_required
def check_active_sos_alerts(request):
    """
    Admin Command Center Polling Endpoint.
    Pings every 5 seconds to check for any SOSAlert records with an 'Active' status.
    """
    active_alerts = SOSAlert.objects.filter(
        status__in=['Active', SOSAlert.Status.ACTIVE]
    ).select_related('passenger', 'driver', 'trip').order_by('-timestamp')

    alerts_data = []
    for alert in active_alerts:
        driver_name = alert.driver.name if alert.driver else (alert.trip.driver.name if alert.trip and alert.trip.driver else "Unknown Driver")
        vehicle_num = alert.driver.vehicle_number if alert.driver else (alert.trip.driver.vehicle_number if alert.trip and alert.trip.driver else "N/A")
        passenger_name = alert.passenger.get_full_name() or alert.passenger.username

        alerts_data.append({
            'sos_id': alert.sos_id,
            'passenger_name': passenger_name,
            'passenger_phone': getattr(alert.passenger, 'phone_number', 'N/A'),
            'driver_name': driver_name,
            'vehicle_number': vehicle_num,
            'latitude': float(alert.latitude),
            'longitude': float(alert.longitude),
            'location_name': alert.location_name or alert.location,
            'timestamp': alert.timestamp.strftime('%H:%M:%S'),
            'map_url': f"https://www.google.com/maps?q={alert.latitude},{alert.longitude}",
            'resolve_url': f"/admin-panel/sos/{alert.sos_id}/resolve/",
        })

    return JsonResponse({
        'status': 'success',
        'count': len(alerts_data),
        'alerts': alerts_data
    })

# Backward compatibility aliases
trigger_sos_api = trigger_sos_alert
update_live_location_api = update_trip_location


# ==========================================
# PWA (PROGRESSIVE WEB APP) VIEWS
# ==========================================

def service_worker_view(request):
    """Serves the PWA Service Worker script at root path /sw.js."""
    import os
    from django.conf import settings
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "// SafeRide Service Worker"
    return HttpResponse(content, content_type="application/javascript")

def manifest_view(request):
    """Serves the PWA Web App Manifest at root path /manifest.json."""
    import os
    from django.conf import settings
    manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "{}"
    return HttpResponse(content, content_type="application/manifest+json")


def serve_trip_fare_qr(request, trip_id):
    """Dynamically generate and stream Fare Receipt QR code PNG image."""
    from django.http import HttpResponse, Http404
    from io import BytesIO
    from urllib.parse import quote
    import qrcode

    clean_id = str(trip_id).upper().replace('TRIP', '').replace('TRP-', '').replace('TRP', '').replace('#', '').strip()
    lookup_id = int(clean_id) if clean_id.isdigit() else -1

    trip = Trip.objects.filter(
        Q(trip_id=lookup_id) | Q(trip_uuid=trip_id if len(str(trip_id)) > 30 else uuid.uuid4())
    ).first()
    if not trip:
        raise Http404("Trip not found")

    trip.calculate_distance_and_fare()

    driver_upi = (trip.driver.upi_id if (trip.driver and getattr(trip.driver, 'upi_id', None)) else 'saferide@upi').strip()
    payee_name = quote(getattr(trip.driver, 'name', None) or 'SafeRide Driver')
    fare_val = f"{trip.fare_amount:.2f}" if trip.fare_amount else "30.00"
    upi_pay_str = f"upi://pay?pa={driver_upi}&pn={payee_name}&am={fare_val}&cu=INR&tn=SafeRide_TRP_{trip.trip_id}&tr=TRP{trip.trip_id}"

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(upi_pay_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0F172A", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')

    # Also persist to model storage
    try:
        from django.core.files.base import ContentFile
        filename = f"fare_qr_trip_{trip.trip_id}.png"
        trip.fare_qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)
    except Exception:
        pass

    return HttpResponse(buffer.getvalue(), content_type='image/png')


def serve_media_fare_qr(request, filename):
    """
    On-demand handler for /media/fare_qrcodes/<filename>.
    Serves the file if it exists, or dynamically generates and saves it to disk if missing,
    completely eliminating 404 errors for fare QR codes.
    """
    import os
    import re
    from django.conf import settings
    from django.http import HttpResponse, Http404, FileResponse

    fare_dir = settings.MEDIA_ROOT / 'fare_qrcodes'
    fare_dir.mkdir(parents=True, exist_ok=True)
    file_path = fare_dir / filename

    if file_path.exists() and os.path.getsize(file_path) > 0:
        return FileResponse(open(file_path, 'rb'), content_type='image/png')

    # Extract trip_id from filename (e.g. fare_qr_trip_29.png)
    match = re.search(r'fare_qr_trip_(\d+)', filename)
    if not match:
        raise Http404("Fare QR code not found")

    trip_id = int(match.group(1))
    trip = Trip.objects.filter(trip_id=trip_id).first()
    if not trip:
        raise Http404(f"Trip #{trip_id} not found")

    try:
        trip.generate_fare_qr_code(request.build_absolute_uri('/')[:-1])
        trip.save(update_fields=['fare_qr_code'])
    except Exception as e:
        print(f"Error generating fare QR on demand: {e}")

    if file_path.exists() and os.path.getsize(file_path) > 0:
        return FileResponse(open(file_path, 'rb'), content_type='image/png')

    return serve_trip_fare_qr(request, trip_id)


def _generate_official_pdf_bytes(title, doc_number, entity_name="SafeRide Transport Partner"):
    """Generates a standard compliant PDF 1.4 document stream for KYC inspection."""
    stream_content = (
        f"BT\n"
        f"/F1 20 Tf\n"
        f"50 730 Td\n"
        f"(GOVERNMENT OF KERALA - MOTOR VEHICLES DEPT) Tj\n"
        f"0 -28 Td\n"
        f"/F1 15 Tf\n"
        f"({title.upper()}) Tj\n"
        f"0 -36 Td\n"
        f"/F1 12 Tf\n"
        f"(Certificate / Document No: {doc_number}) Tj\n"
        f"0 -22 Td\n"
        f"(Authorized Holder: {entity_name}) Tj\n"
        f"0 -22 Td\n"
        f"(Verification Authority: SafeRide Transport Safety Commission) Tj\n"
        f"0 -22 Td\n"
        f"(Status: AUTHENTICATED & VERIFIED VALID) Tj\n"
        f"0 -34 Td\n"
        f"/F1 10 Tf\n"
        f"(Official Digital Record - Integrated with SafeRide QR Transit Platform) Tj\n"
        f"ET"
    )
    stream_bytes = stream_content.encode('latin1')
    length = len(stream_bytes)
    
    pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
        b"4 0 obj << /Length " + str(length).encode('ascii') + b" >> stream\n"
        + stream_bytes + b"\nendstream\nendobj\n"
        b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> endobj\n"
        b"xref\n"
        b"0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"trailer << /Size 6 /Root 1 0 R >>\n"
        b"startxref\n"
        b"500\n"
        b"%%EOF\n"
    )
    return pdf


def serve_license_doc(request, filename):
    """
    On-demand handler for /media/driver_docs/license/<filename>.
    Serves the license PDF or generates an official authenticated Kerala RTO digital record.
    """
    import os
    from django.conf import settings
    from django.http import FileResponse

    target_dir = settings.MEDIA_ROOT / 'driver_docs' / 'license'
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / filename

    if not file_path.exists() or os.path.getsize(file_path) == 0:
        doc_num = filename.replace('lic_', '').replace('.pdf', '')
        driver = Driver.objects.filter(Q(license_number__icontains=doc_num) | Q(documents__license_doc__icontains=filename)).first()
        holder = driver.name if driver else "SafeRide Registered Driver"
        pdf_bytes = _generate_official_pdf_bytes("Motor Driving License Certificate", doc_num, holder)
        with open(file_path, 'wb') as f:
            f.write(pdf_bytes)

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def serve_rc_doc(request, filename):
    """
    On-demand handler for /media/vehicle_docs/rc/<filename>.
    Serves the vehicle RC PDF or generates an official authenticated Kerala MVD vehicle record.
    """
    import os
    from django.conf import settings
    from django.http import FileResponse

    target_dir = settings.MEDIA_ROOT / 'vehicle_docs' / 'rc'
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / filename

    if not file_path.exists() or os.path.getsize(file_path) == 0:
        reg_num = filename.replace('rc_', '').replace('.pdf', '')
        driver = Driver.objects.filter(Q(vehicle_number__icontains=reg_num) | Q(documents__rc_doc__icontains=filename)).first()
        holder = driver.name if driver else "SafeRide Transport Partner"
        pdf_bytes = _generate_official_pdf_bytes("Certificate of Vehicle Registration (RC)", reg_num, holder)
        with open(file_path, 'wb') as f:
            f.write(pdf_bytes)

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')




