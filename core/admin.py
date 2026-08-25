from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import (
    User, Admin as AdminModel, Passenger, Driver, VehicleDocuments,
    Trip, RatingReview, Complaint, SOSAlert, IncidentReport
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('SafeRide Role & Profile', {'fields': ('role', 'phone', 'avatar')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('SafeRide Role & Profile', {'fields': ('role', 'phone', 'avatar')}),
    )

@admin.register(AdminModel)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'name', 'email')
    search_fields = ('name', 'email')

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('passenger_id', 'name', 'email', 'phone_number', 'emergency_contact_1_phone', 'is_active_account', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'user__username')
    actions = ['suspend_passenger_account', 'activate_passenger_account']

    def is_active_account(self, obj):
        return obj.user.is_active if obj.user else True
    is_active_account.boolean = True
    is_active_account.short_description = "Account Active"

    def suspend_passenger_account(self, request, queryset):
        for p in queryset:
            if p.user:
                p.user.is_active = False
                p.user.save()
        self.message_user(request, f"{queryset.count()} passenger account(s) suspended.")
    suspend_passenger_account.short_description = "Suspend Selected Passenger Accounts"

    def activate_passenger_account(self, request, queryset):
        for p in queryset:
            if p.user:
                p.user.is_active = True
                p.user.save()
        self.message_user(request, f"{queryset.count()} passenger account(s) activated.")
    activate_passenger_account.short_description = "Activate Selected Passenger Accounts"

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('driver_id', 'name', 'phone_number', 'vehicle_number', 'vehicle_type', 'verification_status', 'reputation_score', 'average_rating', 'total_trips', 'qr_code_preview')
    list_filter = ('verification_status', 'vehicle_type')
    search_fields = ('name', 'email', 'phone_number', 'license_number', 'vehicle_number', 'user__username')
    actions = ['approve_verification', 'reject_verification', 'suspend_driver', 'reset_pending']

    def qr_code_preview(self, obj):
        img_src = obj.qr_code_image.url if obj.qr_code_image else obj.qr_code
        if img_src:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: contain; border-radius: 4px; border: 1px solid #ddd;" />', img_src)
        return "No QR"
    qr_code_preview.short_description = "QR Code"

    def approve_verification(self, request, queryset):
        for driver in queryset:
            driver.verification_status = Driver.VerificationStatus.VERIFIED
            driver.save()
            driver.recalculate_reputation()
        self.message_user(request, f"{queryset.count()} driver(s) verified, QR codes generated, and safety reputation updated.")
    approve_verification.short_description = "Approve & Generate QR Code (Verified)"

    def reject_verification(self, request, queryset):
        queryset.update(verification_status=Driver.VerificationStatus.REJECTED)
        self.message_user(request, f"{queryset.count()} driver(s) rejected.")
    reject_verification.short_description = "Reject KYC Verification (Rejected)"

    def suspend_driver(self, request, queryset):
        queryset.update(verification_status=Driver.VerificationStatus.SUSPENDED)
        self.message_user(request, f"{queryset.count()} driver(s) suspended.")
    suspend_driver.short_description = "Suspend Selected Drivers (Suspended)"

    def reset_pending(self, request, queryset):
        queryset.update(verification_status=Driver.VerificationStatus.PENDING)
        self.message_user(request, f"{queryset.count()} driver(s) reset to Pending status.")
    reset_pending.short_description = "Reset Status to Pending"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_verified():
            obj.recalculate_reputation()

@admin.register(VehicleDocuments)
class VehicleDocumentsAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'driver', 'license_doc', 'rc_doc', 'uploaded_at')
    search_fields = ('driver__name', 'driver__vehicle_number', 'driver__license_number')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('trip_id', 'passenger', 'driver', 'status', 'start_location', 'start_time', 'end_time')
    list_filter = ('status', 'start_time')
    search_fields = ('trip_id', 'passenger__username', 'passenger__email', 'driver__name', 'driver__vehicle_number')

@admin.register(RatingReview)
class RatingReviewAdmin(admin.ModelAdmin):
    list_display = ('rating_id', 'trip', 'driver', 'passenger', 'rating', 'driving_safety_rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('driver__name', 'passenger__username', 'review')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_id', 'category', 'driver', 'passenger', 'status', 'penalty_points_deducted', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('driver__name', 'passenger__username', 'description')

@admin.register(SOSAlert)
class SOSAlertAdmin(admin.ModelAdmin):
    list_display = ('sos_id', 'passenger', 'driver', 'status', 'location', 'latitude', 'longitude', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('passenger__username', 'driver__name', 'location')

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('incident_id', 'passenger', 'trip', 'incident_type', 'status', 'reported_at')
    list_filter = ('status', 'incident_type', 'reported_at')
    search_fields = ('passenger__username', 'description', 'incident_type')
