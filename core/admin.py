from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from core.models.base import TourModel
from core.models.booking import BookingModel
from core.models.images import ImageModel
from core.models.payment import PaymentModel
from core.models.periods import DayModel, PeriodModel, PickupTimeModel
from core.models.thumbnail import ThumbnailModel
from core.models.contens import (
    HighlightTexts,
    InclusiveTexts,
    ExclusiveTexts,
    WhatKnowModel,
    WhatBringModel,
)


class TomorrowFilter(admin.SimpleListFilter):
    title = "Yarınki Rezervasyonlar"
    parameter_name = "tomorrow"

    def lookups(self, request, model_admin):
        return (("yes", "Yarın"),)

    def queryset(self, request, queryset):
        tomorrow = timezone.now().date() + timedelta(days=1)
        if self.value() == "yes":
            return queryset.filter(tour_date=tomorrow)


class AfterTomorrowFilter(admin.SimpleListFilter):
    title = "Öbürgünkü Rezervasyonlar"
    parameter_name = "aftertomorrow"

    def lookups(self, request, model_admin):
        return (("yes", "Öbürgün"),)

    def queryset(self, request, queryset):
        aftertomorrow = timezone.now().date() + timedelta(days=2)
        if self.value() == "yes":
            return queryset.filter(tour_date=aftertomorrow)


class BookingAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    sortable_by = [
        "date_created",
    ]
    list_display = (
        "date_created",
        "tour_date",
        "total_cost",
        "status",
    )
    # readonly_fields = ["totalPayment"]
    list_filter = (TomorrowFilter, AfterTomorrowFilter, "tour_date", "status")
    list_editable = ("status",)

    def total_cost(self, obj):
        return obj.total_cost()

    total_cost.short_description = "Total Payment"


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "booking",
        "amount",
        "currency",
        "status",
    ]


class PickupTimeAdmin(admin.ModelAdmin):
    fields = ("time",)
    search_fields = ("time",)


class ThumbnailInline(admin.StackedInline):
    model = ThumbnailModel
    extra = 0


class ImageInline(admin.StackedInline):
    model = ImageModel
    extra = 0


class PeriodAdmin(admin.ModelAdmin):
    model = PeriodModel


class PeriodInline(admin.StackedInline):
    model = PeriodModel
    extra = 0
    autocomplete_fields = [
        "pick_up_times",
    ]


## BASE MODEL !!
class TourAdmin(admin.ModelAdmin):
    model = TourModel

    # prepopulated_fields = {"slug": ["title"]}

    inlines = [
        ThumbnailInline,
        ImageInline,
        PeriodInline,
    ]

    # autocomplete_fields = [
    #     "included",
    #     "excluded",
    #     "what_to_know",
    #     "what_to_bring",
    # ]

    # actions = [""]

    # search_fields = ("title",)

    # list_display = (
    #     "title",
    #     "is_active",
    # )

    # list_editable = ("is_active",)


admin.site.register(PickupTimeModel, PickupTimeAdmin)
admin.site.register(DayModel)
admin.site.register(ImageModel)
admin.site.register(ThumbnailModel)
admin.site.register(PeriodModel, PeriodAdmin)
admin.site.register(TourModel, TourAdmin)
admin.site.register(PaymentModel, PaymentAdmin)
admin.site.register(BookingModel, BookingAdmin)
admin.site.register(HighlightTexts)
admin.site.register(InclusiveTexts)
admin.site.register(ExclusiveTexts)
admin.site.register(WhatKnowModel)
admin.site.register(WhatBringModel)
