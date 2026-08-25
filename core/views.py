import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
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
                is_post_ride_sos = False
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

@passenger_required
def passenger_dashboard(request):
    """Passenger command center."""
    profile, _ = PassengerProfile.objects.get_or_create(user=request.user)
    active_trip = TripSession.objects.filter(passenger=request.user, status__in=['Ongoing', 'IN_PROGRESS']).first()
    recent_trips = TripSession.objects.filter(passenger=request.user).select_related('driver', 'driver__user').order_by('-start_time')[:5]
    recent_complaints = Complaint.objects.filter(passenger=request.user).order_by('-created_at')[:3]

    context = {
        'profile': profile,
        'active_trip': active_trip,
        'recent_trips': recent_trips,
        'recent_complaints': recent_complaints,
        'search_form': DriverSearchForm(),
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

    pickup_lat = float(request.POST.get('pickup_lat', 9.6843))
    pickup_lng = float(request.POST.get('pickup_lng', 76.6853))
    pickup_name = request.POST.get('pickup_name', 'Current Boarding Point')
    destination_name = request.POST.get('destination_name', '')
    destination_lat = request.POST.get('destination_lat')
    destination_lng = request.POST.get('destination_lng')

    trip = TripSession.objects.create(
        passenger=request.user,
        driver=driver,
        boarding_address=pickup_name,
        boarding_latitude=pickup_lat,
        boarding_longitude=pickup_lng,
        destination_address=destination_name if destination_name else None,
        destination_latitude=float(destination_lat) if destination_lat else None,
        destination_longitude=float(destination_lng) if destination_lng else None,
        current_latitude=pickup_lat,
        current_longitude=pickup_lng,
        pickup_location_name=pickup_name,
        pickup_latitude=pickup_lat,
        pickup_longitude=pickup_lng,
        live_latitude=pickup_lat,
        live_longitude=pickup_lng,
        status=TripSession.Status.ACTIVE,
    )
    messages.success(request, f"Safe Trip started with driver {driver.user.get_full_name() or driver.user.username}. Live tracking enabled!")
    return redirect('active_trip', trip_id=trip.trip_id)

@passenger_required
def active_trip(request, trip_id):
    """Live ongoing trip monitoring interface with 1-Touch SOS and live track sharing."""
    trip = get_object_or_404(TripSession.objects.select_related('driver', 'driver__user'), trip_id=trip_id, passenger=request.user)
    
    if trip.status == TripSession.Status.COMPLETED:
        messages.info(request, "This trip has already ended safely. Please rate your experience.")
        return redirect('rate_trip', trip_id=trip.trip_id)

    profile = getattr(request.user, 'passenger_profile', None)
    
    context = {
        'trip': trip,
        'driver': trip.driver,
        'vehicle': getattr(trip.driver, 'vehicle', None),
        'profile': profile,
        'share_url': request.build_absolute_uri(f"/live-track/{trip.share_token}/"),
    }
    return render(request, 'trip_active.html', context)

@passenger_required
def end_trip(request, trip_id):
    """Marks trip as completed and routes to rating screen."""
    trip = get_object_or_404(TripSession, trip_id=trip_id, passenger=request.user)
    trip.complete_trip()
    messages.success(request, "Trip completed safely! Please share your rating to help fellow passengers.")
    return redirect('rate_trip', trip_id=trip.trip_id)

@passenger_required
def rate_trip(request, trip_id):
    """Submits multi-criteria rating, reviews, and optional complaint for the completed journey."""
    trip = get_object_or_404(TripSession.objects.select_related('driver', 'driver__user'), trip_id=trip_id, passenger=request.user)
    
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
            driving_safety_rating=int(request.POST.get('driving_safety_rating', rating_val)),
            vehicle_cleanliness_rating=int(request.POST.get('vehicle_cleanliness_rating', rating_val)),
            behavior_rating=int(request.POST.get('behavior_rating', rating_val)),
            fare_honesty_rating=int(request.POST.get('fare_honesty_rating', rating_val)),
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

    return render(request, 'trip_feedback.html', {'trip': trip})

@passenger_required
def report_complaint(request, driver_id=None, trip_id=None):
    """File a formal grievance against a driver."""
    driver = None
    trip = None
    if driver_id:
        driver = get_object_or_404(DriverProfile, id=driver_id)
    if trip_id:
        trip = get_object_or_404(TripSession, trip_id=trip_id)
        driver = trip.driver

    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        selected_driver_id = request.POST.get('driver_id')
        if selected_driver_id:
            driver = get_object_or_404(DriverProfile, id=selected_driver_id)

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
            messages.success(request, "Emergency contacts updated successfully.")
            return redirect('passenger_dashboard')
    else:
        form = EmergencyContactForm(instance=profile)

    return render(request, 'passenger/emergency_contacts.html', {'form': form})

@passenger_required
def passenger_trip_history(request):
    """View all past trips taken by passenger with clean pagination."""
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

@passenger_required
def report_incident_view(request):
    """Incident Report Form matching Form 10 (INCIDENT REPORT)."""
    if request.method == 'POST':
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            p_name = form.cleaned_data['passenger_name']
            trip_ref = form.cleaned_data.get('trip_id')
            inc_type = form.cleaned_data['incident_type']
            desc = form.cleaned_data['description']
            
            trip_obj = None
            if trip_ref:
                trip_obj = TripSession.objects.filter(trip_id__istartswith=trip_ref.replace('TRP-', '')).first()

            incident = IncidentReport.objects.create(
                passenger=request.user,
                trip=trip_obj,
                incident_type=inc_type,
                description=desc,
                status=IncidentReport.Status.PENDING
            )
            messages.success(request, f"Incident Report #{str(incident.incident_id)[:8]} has been submitted and escalated to safety administration.")
            return redirect('passenger_dashboard')
    else:
        initial = {
            'passenger_name': request.user.get_full_name() or request.user.username,
            'incident_date_time': timezone.now().strftime('%Y-%m-%dT%H:%M')
        }
        form = IncidentReportForm(initial=initial)

    return render(request, 'passenger/report_incident.html', {'form': form})

def live_share_default(request):
    """Fallback when navigating to /live-track/ without a specific token - tracks most recent journey."""
    trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').order_by('-start_time').first()
    if trip:
        return redirect('live_share', token=trip.share_token)
    messages.info(request, "No active monitored journeys are currently streaming GPS telemetry.")
    return redirect('home')

def live_share_view(request, token):
    """Publicly accessible live tracking link for friends and family via Google Maps & Satellite GPS."""
    # Clean token if user entered literal '<token>' or extra symbols
    cleaned_token = str(token).replace('<', '').replace('>', '').replace('%3C', '').replace('%3E', '').strip()
    
    trip = None
    
    # 1. If token is a valid UUID, search by share_token or verification_token
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
            Q(driver__verification_token=cleaned_token)
        ).first()

    # 2. Try by trip_id integer/string if passed (e.g. /live-track/24/ or /live-track/TRP-24/)
    if not trip and (cleaned_token.isdigit() or cleaned_token.startswith('TRP-')):
        try:
            trip_id_num = int(cleaned_token.replace('TRP-', ''))
            trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').filter(
                trip_id=trip_id_num
            ).first()
        except ValueError:
            pass

    # 3. If token was placeholder '<token>' or not found, fall back to most recent trip
    if not trip:
        trip = TripSession.objects.select_related('passenger', 'driver', 'driver__user').order_by('-start_time').first()
        if not trip:
            messages.warning(request, "The live journey you are looking for has either completed or does not exist.")
            return redirect('home')

    return render(request, 'live_share.html', {
        'trip': trip,
        'driver': trip.driver,
        'vehicle': getattr(trip.driver, 'vehicle', None)
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
    
    # Ensure QR code exists if verified
    if driver.is_verified() and not driver.qr_code:
        driver.generate_qr_code(request.build_absolute_uri('/')[:-1])
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
    """Digital and printable Driver ID verification badge with QR code."""
    driver = _get_driver_for_request(request)
    if not driver:
        messages.error(request, "No driver profile found.")
        return redirect('home')

    if driver.is_verified() and not driver.qr_code:
        driver.generate_qr_code(request.build_absolute_uri('/')[:-1])
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
            if form.cleaned_data.get('license_number'):
                driver.license_number = form.cleaned_data['license_number'].strip().upper()
            if form.cleaned_data.get('vehicle_number'):
                driver.vehicle_number = form.cleaned_data['vehicle_number'].strip().upper()
            if form.cleaned_data.get('vehicle_type'):
                driver.vehicle_type = form.cleaned_data['vehicle_type']

            if 'profile_photo' in request.FILES:
                driver.driver_photo = request.FILES['profile_photo']

            driver.save()

            if vehicle:
                if form.cleaned_data.get('vehicle_number'):
                    vehicle.registration_number = form.cleaned_data['vehicle_number'].strip().upper()
                if form.cleaned_data.get('vehicle_make_model'):
                    vehicle.make_model = form.cleaned_data['vehicle_make_model'].strip()
                if form.cleaned_data.get('vehicle_type'):
                    vehicle.vehicle_type = form.cleaned_data['vehicle_type']
                vehicle.save()

            messages.success(request, "Driver and Vehicle Profiles updated successfully.")
            return redirect('driver_profile')
    else:
        initial = {
            'name': driver.name or user.get_full_name() or user.username,
            'email': user.email or driver.email or '',
            'phone_number': driver.phone_number or user.phone or '',
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
    recent_drivers = DriverProfile.objects.select_related('user').order_by('-driver_id')[:5]

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
            # Create Driver User Account
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data.get('email', ''),
                role=User.Role.DRIVER
            )
            
            auto_approve = form.cleaned_data.get('auto_approve', False)
            v_status = DriverProfile.VerificationStatus.VERIFIED if auto_approve else DriverProfile.VerificationStatus.PENDING

            # Create Driver Profile (tbl_driver)
            driver = Driver.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}".strip() or user.username,
                phone_number=user.phone or '',
                email=user.email or '',
                license_number=form.cleaned_data['license_number'],
                vehicle_number=form.cleaned_data['registration_number'].upper(),
                vehicle_type=form.cleaned_data['vehicle_type'],
                password=user.password,
                experience_years=form.cleaned_data['experience_years'],
                driver_photo=form.cleaned_data.get('driver_photo'),
                license_doc=form.cleaned_data.get('license_doc'),
                id_proof_doc=form.cleaned_data.get('id_proof_doc'),
                police_clearance_doc=form.cleaned_data.get('police_clearance_doc'),
                verification_status=v_status,
                verified_at=timezone.now() if auto_approve else None,
                verification_notes="Registered and verified by Administrator" if auto_approve else "Awaiting document inspection",
            )

            # Create Vehicle Documents (tbl_vehicle_documents)
            VehicleDocuments.objects.create(
                driver=driver,
                license_doc=str(form.cleaned_data.get('license_doc') or ''),
                rc_doc=str(form.cleaned_data.get('rc_book_doc') or ''),
                license_file=form.cleaned_data.get('license_doc'),
                rc_file=form.cleaned_data.get('rc_book_doc'),
            )

            if auto_approve:
                driver.generate_qr_code(request.build_absolute_uri('/')[:-1])
                driver.save()
                driver.recalculate_reputation()
                messages.success(request, f"Driver {user.get_full_name()} registered & verified successfully! QR Code generated.")
            else:
                messages.info(request, f"Driver {user.get_full_name()} registered in 'Pending' state. Complete document verification to approve.")

            return redirect('admin_driver_list')
        else:
            messages.error(request, "Please fix the errors in the registration form.")
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
                driver.generate_qr_code(request.build_absolute_uri('/')[:-1])
                driver.recalculate_reputation()
                messages.success(request, f"Driver {driver.name} has been successfully VERIFIED. QR Code updated!")
            elif driver.verification_status in ['Rejected', Driver.VerificationStatus.SUSPENDED]:
                messages.warning(request, f"Driver {driver.name} verification status set to {driver.verification_status}.")
            else:
                messages.info(request, f"Verification status updated to {driver.get_verification_status_display()}.")
            driver.save()
            return redirect('admin_driver_list')
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
    messages.success(request, f"SOS Alert #{str(alert.sos_id)} marked as RESOLVED.")
    return redirect('admin_sos_monitoring')

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
    """List registered passengers."""
    passengers = PassengerProfile.objects.select_related('user').all().order_by('-passenger_id')
    return render(request, 'admin_panel/passenger_list.html', {'passengers': passengers})

@admin_required
def admin_toggle_passenger_status(request, passenger_id):
    """Suspend or reactivate a passenger account."""
    passenger = get_object_or_404(PassengerProfile.objects.select_related('user'), passenger_id=passenger_id)
    user = passenger.user
    user.is_active = not user.is_active
    user.save()
    status_text = "Activated" if user.is_active else "Suspended"
    messages.success(request, f"Passenger {user.get_full_name() or user.username} account has been {status_text}.")
    return redirect('admin_passenger_list')

# ==========================================
# SOS DISPATCH & LOCATION AJAX ENDPOINTS
# ==========================================

@login_required
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

    # Find active trip by numeric id or UUID
    trip = Trip.objects.filter(
        Q(trip_id=int(trip_id) if str(trip_id).isdigit() else -1) | Q(trip_uuid=trip_id if len(str(trip_id)) > 30 else uuid.uuid4())
    ).first()

    if not trip:
        return JsonResponse({'status': 'error', 'message': 'Trip not found.'}, status=404)

    # Update current telemetry
    trip.current_latitude = lat
    trip.current_longitude = lng
    trip.live_latitude = lat
    trip.live_longitude = lng
    trip.live_updated_at = timezone.now()
    trip.save(update_fields=['current_latitude', 'current_longitude', 'live_latitude', 'live_longitude', 'live_updated_at'])

    return JsonResponse({
        'status': 'success',
        'trip_id': trip.trip_id,
        'current_latitude': float(trip.current_latitude),
        'current_longitude': float(trip.current_longitude),
        'timestamp': trip.live_updated_at.isoformat()
    })


@login_required
def trigger_sos_alert(request):
    """
    Instant SOS Emergency Alert Endpoint.
    Creates a new SOSAlert database record linking Passenger, Driver, and Location with 'Active' status.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST request required.'}, status=405)

    try:
        data = json.loads(request.body) if request.body else request.POST
        trip_id = data.get('trip_id')
        driver_id = data.get('driver_id')
        lat = float(data.get('latitude', 9.684300))
        lng = float(data.get('longitude', 76.685300))
        location_name = data.get('location_name', f'GPS Coordinates: {lat:.6f}, {lng:.6f}')
    except (ValueError, TypeError, json.JSONDecodeError):
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

    return JsonResponse({
        'status': 'success',
        'success': True,
        'alert_id': sos.sos_id,
        'message': '🚨 SOS Emergency Alert broadcasted to Admin Command Center!',
        'passenger': passenger.get_full_name() or passenger.username,
        'vehicle_number': driver.vehicle_number if driver else 'N/A',
        'latitude': float(lat),
        'longitude': float(lng),
        'timestamp': sos.timestamp.strftime('%H:%M:%S')
    })


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

def offline_view(request):
    """Displays the PWA offline dead-zone fallback screen."""
    return render(request, 'offline.html')

