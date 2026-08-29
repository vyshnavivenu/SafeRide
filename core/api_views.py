from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from .models import User, Driver, Passenger, Trip, SOSAlert, Complaint, IncidentReport
from .serializers import (
    DriverSerializer, TripSerializer, SOSAlertSerializer, 
    ComplaintSerializer, IncidentReportSerializer
)

class DriverListAPIView(APIView):
    """
    DRF Endpoint: List all verified drivers or search by plate/license number.
    GET /api/v1/drivers/?query=KL05AT4455
    """
    def get(self, request):
        query = request.query_params.get('query', '').strip()
        drivers = Driver.objects.all()
        if query:
            cleaned_q = query.upper().replace(" ", "").replace("-", "")
            drivers = drivers.filter(vehicle_number__icontains=cleaned_q) | drivers.filter(license_number__icontains=query)
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DriverVerificationAPIView(APIView):
    """
    DRF Endpoint: Retrieve verified driver safety profile via token (QR scan endpoint).
    GET /api/v1/drivers/<uuid:token>/verify/
    """
    def get(self, request, token):
        driver = get_object_or_404(Driver, verification_token=token)
        serializer = DriverSerializer(driver)
        return Response({
            'verified': driver.is_verified(),
            'driver': serializer.data,
            'reputation_score': driver.reputation_score,
            'average_rating': driver.average_rating,
            'total_trips': driver.total_trips
        }, status=status.HTTP_200_OK)


class SOSTriggerAPIView(APIView):
    """
    DRF Endpoint: Immediate 1-Touch Emergency Distress Broadcast.
    POST /api/v1/sos/trigger/
    """
    def post(self, request):
        lat = float(request.data.get('latitude', 9.6843))
        lng = float(request.data.get('longitude', 76.6853))
        location_name = request.data.get('location_name', 'Live GPS Distress Signal')
        trip_id = request.data.get('trip_id')
        emergency_note = request.data.get('emergency_note', '1-Touch Emergency Distress Beacon triggered.')

        passenger = request.user if (request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'PASSENGER') else None
        if not passenger:
            passenger = User.objects.filter(role=User.Role.PASSENGER).first() or User.objects.first()
        
        trip = None
        driver = None
        if trip_id:
            trip = Trip.objects.filter(trip_id=trip_id).first()
            if trip:
                driver = trip.driver
                trip.status = 'SOS_Triggered'
                trip.save()

        existing_alert = SOSAlert.objects.filter(
            passenger=passenger,
            status='Active'
        ).order_by('-timestamp').first()

        if existing_alert:
            existing_alert.latitude = lat
            existing_alert.longitude = lng
            existing_alert.location_name = location_name
            existing_alert.timestamp = timezone.now()
            existing_alert.admin_notes = f"{emergency_note} (DRF API Broadcast)"
            if driver and not existing_alert.driver:
                existing_alert.driver = driver
            if trip and not existing_alert.trip:
                existing_alert.trip = trip
            existing_alert.save()
            alert = existing_alert
        else:
            alert = SOSAlert.objects.create(
                passenger=passenger,
                driver=driver,
                trip=trip,
                latitude=lat,
                longitude=lng,
                location_name=location_name,
                status='Active',
                admin_notes=f"{emergency_note} (DRF API Broadcast)"
            )

        serializer = SOSAlertSerializer(alert)
        return Response({
            'success': True,
            'alert_id': str(alert.sos_id),
            'timestamp': alert.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'alert': serializer.data
        }, status=status.HTTP_200_OK)


class TripLocationAPIView(APIView):
    """
    DRF Endpoint: Live GPS Telemetry for ongoing passenger transit session.
    GET/POST /api/v1/trips/<str:trip_id>/location/
    """
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        return Response({
            'trip_id': trip.trip_id,
            'status': trip.status,
            'latitude': trip.live_latitude,
            'longitude': trip.live_longitude,
            'updated_at': trip.live_updated_at
        }, status=status.HTTP_200_OK)

    def post(self, request, trip_id):
        trip = get_object_or_404(Trip, trip_id=trip_id)
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        if lat is not None and lng is not None:
            trip.live_latitude = float(lat)
            trip.live_longitude = float(lng)
            trip.current_latitude = float(lat)
            trip.current_longitude = float(lng)
            trip.live_updated_at = timezone.now()
            trip.save(update_fields=['live_latitude', 'live_longitude', 'current_latitude', 'current_longitude', 'live_updated_at'])
            return Response({'success': True, 'trip_id': trip.trip_id}, status=status.HTTP_200_OK)
        return Response({'error': 'latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)


class IncidentReportAPIView(APIView):
    """
    DRF Endpoint: Log formal incident / safety misconduct report.
    POST /api/v1/incidents/report/
    """
    def post(self, request):
        passenger = request.user if (request.user.is_authenticated and hasattr(request.user, 'role')) else User.objects.filter(role=User.Role.PASSENGER).first() or User.objects.first()
        trip_id = request.data.get('trip_id')
        trip = Trip.objects.filter(trip_id=trip_id).first() if trip_id else None

        report = IncidentReport.objects.create(
            passenger=passenger,
            trip=trip,
            incident_type=request.data.get('incident_type', 'Unsafe Driving'),
            description=request.data.get('description', 'Safety Incident Report via DRF API'),
            status='Pending'
        )
        serializer = IncidentReportSerializer(report)
        return Response({'success': True, 'report': serializer.data}, status=status.HTTP_201_CREATED)

class VerifyDriverAPIView(APIView):
    """
    DRF Endpoint: Search and verify driver by plate or license query.
    GET /api/v1/verify-driver/?query=KL05AT4455 or /api/v1/verify-driver/<query>/
    """
    def get(self, request, query=None):
        search_term = (
            query or 
            request.query_params.get('query', '').strip() or 
            request.query_params.get('q', '').strip() or 
            request.query_params.get('vehicle_number', '').strip()
        )
        if not search_term:
            return Response({'error': 'Search query required'}, status=status.HTTP_400_BAD_REQUEST)

        cleaned_q = search_term.upper().replace(" ", "").replace("-", "")
        driver = None
        for d in Driver.objects.all():
            d_clean = (d.vehicle_number or '').upper().replace(" ", "").replace("-", "")
            if d_clean == cleaned_q or search_term.upper() in (d.vehicle_number or '').upper() or search_term.upper() in (d.license_number or '').upper():
                driver = d
                break

        if not driver:
            driver = Driver.objects.filter(
                Q(license_number__icontains=search_term) | Q(name__icontains=search_term) | Q(user__username__icontains=search_term)
            ).first()

        if not driver:
            return Response({'found': False, 'message': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DriverSerializer(driver)
        return Response({
            'found': True,
            'verified': driver.is_verified(),
            'driver': serializer.data
        }, status=status.HTTP_200_OK)


class TriggerSOSAPIView(SOSTriggerAPIView):
    """Alias for SOSTriggerAPIView."""
    pass


class ActiveSOSListAPIView(APIView):
    """
    DRF Endpoint: List currently active SOS distress incidents.
    GET /api/v1/sos/active/
    """
    def get(self, request):
        active_alerts = SOSAlert.objects.filter(status='Active').order_by('-timestamp')
        serializer = SOSAlertSerializer(active_alerts, many=True)
        return Response({
            'count': active_alerts.count(),
            'alerts': serializer.data
        }, status=status.HTTP_200_OK)

