# core/views/booking_process.py (sen nereye koyduysan)

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt

from core.models.base import TourModel
from core.models.periods import PeriodModel
from core.models.booking import BookingModel


def add_cors_headers(response):
    """Add CORS headers to response"""
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@csrf_exempt
def create_booking(request, slug):
    # Handle CORS preflight OPTIONS request
    if request.method == "OPTIONS":
        response = JsonResponse({})
        return add_cors_headers(response)
    
    # Only allow POST for actual booking
    if request.method != "POST":
        response = JsonResponse({"detail": "Method not allowed."}, status=405)
        return add_cors_headers(response)
    
    # --- JSON body parse ---
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        response = JsonResponse({"detail": "Invalid JSON body."}, status=400)
        return add_cors_headers(response)

    # --- Turu slug ile bul ---
    tour = get_object_or_404(TourModel, slug=slug, is_active=True)

    # --- Body'den field'lar ---
    period_id = payload.get("period_id")
    tour_date_str = payload.get("tour_date")
    pick_up_time = payload.get("pick_up_time")

    full_name = payload.get("full_name")
    email = payload.get("email")
    phone = payload.get("phone")
    adults = payload.get("adults", 1)
    children = payload.get("children", 0)
    hotel_name = payload.get("hotel_name")
    message = payload.get("message", "")

    selected_curreny = payload.get("selected_curreny", "EUR")

    # --- Zorunlu alan kontrolü ---
    required_fields = {
        "period_id": period_id,
        "tour_date": tour_date_str,
        "pick_up_time": pick_up_time,
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "hotel_name": hotel_name,
    }
    missing = [k for k, v in required_fields.items() if not v]
    if missing:
        response = JsonResponse(
            {"detail": f"Missing required fields: {', '.join(missing)}"},
            status=400,
        )
        return add_cors_headers(response)

    # --- Tarih parse ---
    tour_date = parse_date(tour_date_str)
    if not tour_date:
        response = JsonResponse(
            {"detail": "tour_date must be in YYYY-MM-DD format."},
            status=400,
        )
        return add_cors_headers(response)

    # --- Adults / children integer parse ---
    try:
        adults = int(adults)
        if adults <= 0:
            raise ValueError
    except (TypeError, ValueError):
        response = JsonResponse(
            {"detail": "adults must be a positive integer."},
            status=400,
        )
        return add_cors_headers(response)

    try:
        children = int(children)
        if children < 0:
            raise ValueError
    except (TypeError, ValueError):
        response = JsonResponse(
            {"detail": "children must be a non-negative integer."},
            status=400,
        )
        return add_cors_headers(response)

    # --- Period doğrulama ---
    period = PeriodModel.objects.filter(
        period_id=period_id, tour=tour, is_active=True
    ).first()
    if not period:
        response = JsonResponse(
            {"detail": "Invalid period_id for this tour."},
            status=400,
        )
        return add_cors_headers(response)

    # tarih aralık kontrolü
    if (period.start_date and tour_date < period.start_date) or (
        period.end_date and tour_date > period.end_date
    ):
        response = JsonResponse(
            {"detail": "Selected tour_date is not within this period range."},
            status=400,
        )
        return add_cors_headers(response)

    # --- Pickup time doğrulama (BURASI DÜZELTİLDİ) ---
    valid_pickup_times = [t.time for t in period.pick_up_times.all()]
    if pick_up_time not in valid_pickup_times:
        response = JsonResponse(
            {
                "detail": "Invalid pick_up_time for this period.",
                "valid_times": valid_pickup_times,
            },
            status=400,
        )
        return add_cors_headers(response)

    # --- Integer fiyat snapshot ---
    adult_price = int(period.adult_price or 0)
    child_price = int(period.child_price or 0)
    discount_rate = period.discount_rate  # int or None

    # --- Fiyat hesaplama ---
    total_cost = adult_price * adults
    if children > 0:
        total_cost += child_price * children

    if discount_rate:
        total_cost = total_cost * (100 - int(discount_rate)) // 100

    # --- KAYIT ---
    booking = BookingModel.objects.create(
        tour=tour,
        period=period,
        tour_date=tour_date,
        pick_up_time=pick_up_time,
        full_name=full_name,
        email=email,
        phone=phone,
        adults=adults,
        children=children if children > 0 else None,
        hotel_name=hotel_name,
        message=message or "",
        adult_price=adult_price,
        child_price=child_price if children > 0 else None,
        discount_rate=discount_rate,
        total_cost=total_cost,
        selected_curreny=selected_curreny,
    )

    response = JsonResponse(
        {
            "booking_id": str(booking.booking_id),
            "status": booking.status,
            "tour": {
                "id": str(tour.tour_id),
                "slug": tour.slug,
                "title": tour.title,
            },
            "period_id": str(period.period_id),
            "tour_date": str(booking.tour_date),
            "pick_up_time": booking.pick_up_time,
            "adults": booking.adults,
            "children": booking.children,
            "total_cost": booking.total_cost,
            "currency": booking.selected_curreny,
        },
        status=201,
        json_dumps_params={"ensure_ascii": False},
    )
    return add_cors_headers(response)
