from django.http import JsonResponse
from django.views.decorators.http import require_GET
from core.models.base import TourModel


@require_GET
def tour_listing(request):

    tours = (
        TourModel.objects.filter(is_active=True)
        .select_related("tour_thumbnail")
        .prefetch_related("tour_periods")
    )

    tours_data = []

    for tour in tours:

        thumbnail_obj = getattr(tour, "tour_thumbnail", None)

        thumbnail_data = None

        if thumbnail_obj and thumbnail_obj.image:
            thumbnail_data = {
                "image": request.build_absolute_uri(thumbnail_obj.image.url),
                "alt_text": thumbnail_obj.alt_text,
            }

        min_adult_price = None

        periods = tour.tour_periods.all()

        if periods.exists():
            prices = [
                pricing.adult_price
                for pricing in periods
                if hasattr(pricing, "adult_price") and pricing.adult_price is not None
            ]
            if prices:
                min_adult_price = min(prices)

        tours_data.append(
            {
                "tour_id": str(tour.tour_id),
                "title": tour.title,
                "slug": tour.slug,
                "short_description": tour.short_description,
                "thumbnail": thumbnail_data,
                "min_adult_price": min_adult_price,
                "review_count": str(tour.review_count),
                "average_rating": str(tour.review_rate),
            }
        )

    return JsonResponse(
        data=tours_data,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )
