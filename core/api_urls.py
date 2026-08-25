from django.urls import path
from . import api_views

urlpatterns = [
    path('verify-driver/', api_views.VerifyDriverAPIView.as_view(), name='api_verify_driver'),
    path('verify-driver/<str:query>/', api_views.VerifyDriverAPIView.as_view(), name='api_verify_driver_param'),
    path('sos/trigger/', api_views.TriggerSOSAPIView.as_view(), name='api_sos_trigger'),
    path('sos/active/', api_views.ActiveSOSListAPIView.as_view(), name='api_sos_active'),
]
