from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from core.models.booking import BookingModel


@require_POST
def create_booking(request):
    if request.method == "POST":
        tour = request.POST.get("tour")
        tour_date = request.POST.get("tour_date")
        period_pricing = request.POST.get("period_pricing")
        adult_pax = request.POST.get("adults")
        child_pax = request.POST.get("children")
        hotel_name = request.POST.get("hotel_name")
        full_name = request.POST["full_name"]
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        booking = BookingModel(
            tour=tour,
            tour_date=tour_date,
            period_pricing=period_pricing,
            adults=adult_pax,
            children=child_pax,
            hotel_name=hotel_name,
            full_name=full_name,
            phone=phone,
            email=email,
            message=message,
        )
        adult_cost = tour.adult_cost * adult_pax
        child_cost = tour.child_cost * child_pax
        booking.total_cost = adult_cost + child_cost
        booking.save()
    else:
        redirect("/")
