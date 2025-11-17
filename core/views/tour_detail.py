from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from core.models.base import TourModel


@require_GET
def tour_detail(request, slug):
    """
    Tour detail:
    - get_object_or_404 ile alınır
    - thumbnail zorunlu → null check yok
    - request.build_absolute_uri direkt dict içinde kullanılır
    - ilişkiler optimize edilmiş şekilde fetch edilir
    """

    tour = (
        TourModel.objects.select_related("tour_thumbnail")  # OneToOne: thumbnail
        .prefetch_related(
            "tour_images",  # 1-N images
            "tour_periods__enabled_days",  # Period M2M
            "tour_periods__pick_up_times",  # Period M2M
            "highlights",
            "included",
            "excluded",
            "what_to_know",
            "what_to_bring",
        )
        .filter(is_active=True)
    )

    # --- GET SAFE ---
    tour = get_object_or_404(tour, slug=slug)

    # --- Local fields (M2M hariç) ---
    data = model_to_dict(tour)
    data["tour_id"] = str(tour.tour_id)

    # --- Thumbnail (zorunlu → direkt erişiyoruz) ---
    thumb = tour.tour_thumbnail
    data["thumbnail"] = {
        "image": request.build_absolute_uri(thumb.image.url),
        "alt_text": thumb.alt_text,
    }

    # --- Images ---
    images = []
    for img in tour.tour_images.all():
        images.append(
            {
                "image_id": str(img.image_id),
                "image": request.build_absolute_uri(img.image.url),
                "alt_text": img.alt_text,
                "date_added": img.date_added.isoformat() if img.date_added else None,
                "date_edited": img.date_edited.isoformat() if img.date_edited else None,
            }
        )
    data["images"] = images

    # --- Periods ---
    periods = []
    for p in tour.tour_periods.all():
        periods.append(
            {
                "period_id": str(p.period_id),
                "title": p.title,
                "start_date": p.start_date.isoformat() if p.start_date else None,
                "end_date": p.end_date.isoformat() if p.end_date else None,
                "adult_price": float(p.adult_price) if p.adult_price else None,
                "child_price": float(p.child_price) if p.child_price else None,
                "discount_rate": p.discount_rate,
                "is_active": p.is_active,
                "enabled_days": [
                    {"name": d.name, "number": d.number} for d in p.enabled_days.all()
                ],
                "pickup_times": [str(t.time) for t in p.pick_up_times.all()],
                "date_added": p.date_added.isoformat() if p.date_added else None,
                "date_edited": p.date_edited.isoformat() if p.date_edited else None,
            }
        )
    data["periods"] = periods

    # --- M2M Text Fields ---
    data["highlights"] = list(tour.highlights.values_list("text", flat=True))
    data["included"] = list(tour.included.values_list("text", flat=True))
    data["excluded"] = list(tour.excluded.values_list("text", flat=True))
    data["what_to_know"] = list(tour.what_to_know.values_list("text", flat=True))
    data["what_to_bring"] = list(tour.what_to_bring.values_list("text", flat=True))

    # --- Review fields (varsa ekle) ---
    if hasattr(tour, "review_count"):
        data["review_count"] = str(tour.review_count)
    if hasattr(tour, "review_rate"):
        data["average_rating"] = str(tour.review_rate)

    return JsonResponse(data, json_dumps_params={"ensure_ascii": False})
