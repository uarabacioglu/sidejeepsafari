from django.http import JsonResponse
from core.models.base import TourModel


def tour_listing(request):
    qs = (
        TourModel.objects.all()
        .filter(is_active=True)
        .select_related()
        .prefetch_related(
            "tour_images",
            "tour_periods",
            "highlights",
            "included",
            "excluded",
            "what_to_know",
            "what_to_bring",
        )
    )

    tours = []
    for t in qs:
        # ManyToMany text lists
        highlights = [h.text for h in t.highlights.all()]
        included = [i.text for i in t.included.all()]
        excluded = [e.text for e in t.excluded.all()]
        what_to_know = [w.text for w in t.what_to_know.all()]
        what_to_bring = [b.text for b in t.what_to_bring.all()]
        # Thumbnail (OneToOne)
        thumbnail = None
        if hasattr(t, "tour_thumbnail") and t.tour_thumbnail is not None:
            thumb = t.tour_thumbnail
            thumbnail = {
                "image_id": str(thumb.image_id),
                "image_url": thumb.image.url if getattr(thumb, "image", None) else None,
                "alt_text": thumb.alt_text,
            }

        # Images (FK reverse)
        images = [
            {
                "image_id": str(img.image_id),
                "image_url": img.image.url if getattr(img, "image", None) else None,
                "alt_text": img.alt_text,
            }
            for img in t.tour_images.all()
        ]

        # Periods (FK reverse)
        periods = [
            {
                "period_id": str(p.period_id),
                "title": p.title,
                "start_date": p.start_date.isoformat() if p.start_date else None,
                "end_date": p.end_date.isoformat() if p.end_date else None,
                "adult_price": (
                    str(p.adult_price)
                    if getattr(p, "adult_price", None) is not None
                    else None
                ),
                "child_price": (
                    str(p.child_price)
                    if getattr(p, "child_price", None) is not None
                    else None
                ),
                "is_active": p.is_active,
            }
            for p in t.tour_periods.all()
        ]

        tours.append(
            {
                "tour_id": str(t.tour_id),
                "title": t.title,
                "slug": t.slug,
                "short_description": t.short_description,
                "full_description": t.full_description,
                "highlights": highlights,
                "included": included,
                "excluded": excluded,
                "what_to_know": what_to_know,
                "what_to_bring": what_to_bring,
                "duration": t.duration,
                "pickup_description": t.pickup_description,
                "thumbnail": thumbnail,
                "images": images,
                "periods": periods,
                "date_added": (
                    t.date_added.isoformat() if getattr(t, "date_added", None) else None
                ),
                "date_edited": (
                    t.date_edited.isoformat()
                    if getattr(t, "date_edited", None)
                    else None
                ),
                "is_active": t.is_active,
            }
        )

    return JsonResponse({"tours": tours})
