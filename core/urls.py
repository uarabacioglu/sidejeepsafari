from django.urls import path
from core.views.booking_process import create_booking
from core.views.tour_listing import tour_listing
from core.views.tour_single import tour_single


urlpatterns = [
    path("tours/", tour_listing, name="tour_listing"),
    path("tours/<uuid:tour_id>/", tour_single, name="tour_single"),
    path("booking-create/", create_booking, name="create_booking"),
]
