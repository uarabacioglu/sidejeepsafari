from django.urls import path
from core.views.tour_listing import tour_listing
from core.views.tour_single import tour_single

urlpatterns = [
    path("tours/", tour_listing, name="tour_listing"),
    path("tours/<uuid:tour_id>/", tour_single, name="tour_single"),
]
