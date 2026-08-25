from rest_framework import serializers
from .models import (
    User, Passenger, Driver, VehicleDocuments, Trip, 
    RatingReview, Complaint, SOSAlert, IncidentReport
)

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'role']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class PassengerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Passenger
        fields = [
            'passenger_id', 'user', 'name', 'email', 'phone_number', 
            'emergency_contact_1_name', 'emergency_contact_1_phone',
            'emergency_contact_2_name', 'emergency_contact_2_phone',
            'created_at'
        ]


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = [
            'driver_id', 'user', 'name', 'phone_number', 'email',
            'license_number', 'vehicle_number', 'vehicle_type',
            'verification_status', 'reputation_score', 'average_rating',
            'total_trips', 'experience_years', 'verification_token',
            'qr_code', 'verified_at'
        ]


class TripSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(read_only=True)
    passenger = UserSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = [
            'trip_id', 'passenger', 'driver', 'status', 'start_time', 'end_time',
            'start_location', 'end_location', 'live_latitude', 'live_longitude',
            'live_updated_at', 'share_token'
        ]


class SOSAlertSerializer(serializers.ModelSerializer):
    passenger = UserSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = SOSAlert
        fields = [
            'sos_id', 'passenger', 'driver', 'trip', 'latitude', 
            'longitude', 'location_name', 'status', 'timestamp', 'admin_notes'
        ]


class RatingReviewSerializer(serializers.ModelSerializer):
    passenger = UserSerializer(read_only=True)

    class Meta:
        model = RatingReview
        fields = [
            'rating_id', 'trip', 'driver', 'passenger', 'rating', 
            'review', 'driving_safety_rating', 'vehicle_cleanliness_rating',
            'behavior_rating', 'fare_honesty_rating', 'created_at'
        ]


class ComplaintSerializer(serializers.ModelSerializer):
    passenger = UserSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Complaint
        fields = [
            'complaint_id', 'trip', 'passenger', 'driver', 'category',
            'description', 'status', 'created_at', 'penalty_points_deducted',
            'admin_remarks', 'resolved_at'
        ]


class IncidentReportSerializer(serializers.ModelSerializer):
    passenger = UserSerializer(read_only=True)

    class Meta:
        model = IncidentReport
        fields = [
            'incident_id', 'incident_uuid', 'passenger', 'trip',
            'incident_type', 'description', 'status', 'reported_at'
        ]
