from django.urls import path
from core.views.booking_process import create_booking
from core.views.tour_listing import tour_listing
from core.views.tour_detail import tour_detail


urlpatterns = [
    path("tours/", tour_listing, name="tour_listing"),
    path("tours/<slug:slug>/", tour_detail, name="tour_detail"),
    path("tours/<slug:slug>/book/", create_booking, name="create_booking"),
]
