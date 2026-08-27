from django.urls import path
from . import views, api_views

urlpatterns = [
    # Public & Auth Views
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/passenger/', views.passenger_login_view, name='passenger_login'),
    path('login/driver/', views.driver_login_view, name='driver_login'),
    path('secure-admin-portal/login/', views.admin_login_view, name='admin_login'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('register/passenger/', views.passenger_register, name='passenger_register'),
    path('driver-info/', views.driver_login_info, name='driver_login_info'),

    # Driver Verification & Safety Card
    path('verify/', views.verify_driver_search, name='verify_driver_search'),
    path('verify/<uuid:token>/', views.verify_driver_token, name='verify_driver_token'),

    # Passenger Module
    path('passenger/', views.passenger_dashboard, name='passenger_root'),
    path('passenger/dashboard/', views.passenger_dashboard, name='passenger_dashboard'),
    path('passenger/profile/', views.passenger_profile_view, name='passenger_profile'),
    path('passenger/start-trip/<int:driver_id>/', views.start_trip, name='start_trip'),
    path('passenger/trip/<str:trip_id>/', views.active_trip, name='active_trip'),
    path('passenger/trip/<str:trip_id>/end/', views.end_trip, name='end_trip'),
    path('passenger/trip/<str:trip_id>/rate/', views.rate_trip, name='rate_trip'),
    path('passenger/trip/<str:trip_id>/feedback/', views.rate_trip, name='submit_feedback'),
    path('passenger/complaint/report/', views.report_complaint, name='report_complaint'),
    path('passenger/complaint/report/<int:driver_id>/', views.report_complaint, name='report_complaint_driver'),
    path('passenger/incident/report/', views.report_incident_view, name='report_incident'),
    path('passenger/emergency-contacts/', views.emergency_contacts_view, name='emergency_contacts'),
    path('passenger/trip-history/', views.passenger_trip_history, name='passenger_trip_history'),
    path('live-track/', views.live_share_default, name='live_share_default'),
    path('live-track/<str:token>/', views.live_share_view, name='live_share'),

    # Driver Module
    path('driver/', views.driver_dashboard, name='driver_root'),
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver/profile/', views.driver_profile_view, name='driver_profile'),
    path('driver/id-badge/', views.driver_id_badge, name='driver_id_badge'),
    path('driver/qr-code/', views.driver_id_badge, name='driver_qr_code'),
    path('driver/trip-logs/', views.driver_trip_logs, name='driver_trip_logs'),

    # Admin Command Center
    path('admin-panel/', views.admin_dashboard, name='admin_panel_root'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/drivers/', views.admin_driver_list, name='admin_driver_list'),
    path('admin-panel/drivers/register/', views.admin_driver_register, name='admin_driver_register'),
    path('admin-panel/drivers/<int:driver_id>/kyc/', views.admin_driver_kyc, name='admin_driver_kyc'),
    path('admin-panel/sos-monitoring/', views.admin_sos_monitoring, name='admin_sos_monitoring'),
    path('admin-panel/sos/<str:alert_id>/resolve/', views.admin_resolve_sos, name='admin_resolve_sos'),
    path('admin-panel/complaints/', views.admin_complaints_list, name='admin_complaints_list'),
    path('admin-panel/complaints/<str:complaint_id>/resolve/', views.admin_resolve_complaint, name='admin_resolve_complaint'),
    path('admin-panel/passengers/', views.admin_passenger_list, name='admin_passenger_list'),
    path('admin-panel/passengers/<int:passenger_id>/toggle-status/', views.admin_toggle_passenger_status, name='admin_toggle_passenger_status'),

    # AJAX & Location Endpoints
    path('api/sos/trigger/', views.trigger_sos_alert, name='trigger_sos_alert'),
    path('api/trip/<str:trip_id>/update-location/', views.update_trip_location, name='update_trip_location'),
    path('api/trip/<str:trip_id>/location/', views.update_trip_location, name='update_trip_location_alias'),
    path('api/admin/sos/active/', views.check_active_sos_alerts, name='check_active_sos_alerts'),
    path('track/<str:token>/', views.live_share_view, name='live_share_trip_track_alias'),

    # Django REST Framework (DRF) Endpoints
    path('api/v1/drivers/', api_views.DriverListAPIView.as_view(), name='api_driver_list'),
    path('api/v1/drivers/<uuid:token>/verify/', api_views.DriverVerificationAPIView.as_view(), name='api_driver_verify'),
    path('api/v1/sos/trigger/', api_views.SOSTriggerAPIView.as_view(), name='api_sos_trigger'),
    path('api/v1/trips/<str:trip_id>/location/', api_views.TripLocationAPIView.as_view(), name='api_trip_location'),
    path('api/v1/incidents/report/', api_views.IncidentReportAPIView.as_view(), name='api_incident_report'),

    # PWA (Progressive Web App) Endpoints
    path('sw.js', views.service_worker_view, name='pwa_service_worker'),
    path('manifest.json', views.manifest_view, name='pwa_manifest'),
    path('offline/', views.offline_view, name='pwa_offline'),
]
