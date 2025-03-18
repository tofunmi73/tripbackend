from django.urls import path
from .views import TripCreateView
from .views import geocode

urlpatterns = [
    path('trips/', TripCreateView.as_view(), name='trip-create'),
    path('geocode/', geocode, name='geocode'),
]