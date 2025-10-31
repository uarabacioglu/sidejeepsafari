import uuid
from django.db import models
from core.models.base import TourModel


class PickupTimeModel(models.Model):
    time = models.CharField(max_length=5, blank=False, null=False)

    class Meta:
        db_table = "times"

    def __str__(self) -> str:
        return str(self.time)


class DayModel(models.Model):
    name = models.CharField(
        max_length=3,
        blank=False,
        null=False,
    )
    number = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        db_table = "days"

    def __str__(self) -> str:
        return str(self.name)


class PeriodModel(models.Model):
    period_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    tour = models.ForeignKey(
        to=TourModel,
        on_delete=models.CASCADE,
        related_name="tour_periods",
    )

    title = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        default="High Season",
    )

    start_date = models.DateField(
        auto_now=False,
        blank=False,
        null=False,
    )

    end_date = models.DateField(
        auto_now=False,
        blank=False,
        null=False,
    )

    enabled_days = models.ManyToManyField(
        to=DayModel,
        blank=True,
    )

    pick_up_times = models.ManyToManyField(
        to=PickupTimeModel,
        blank=True,
    )

    adult_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=False,
        null=False,
        default=0.0,
    )

    child_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=False,
        null=False,
        default=0.0,
    )

    discount_rate = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="indirim oranı tüm katılımcıların toplam rezervasyon tutarında yüzdelik olarak düşülücek.",
    )

    is_active = models.BooleanField(
        default=True,
        blank=False,
        null=False,
    )

    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "periods"
        ordering = ("-date_added",)
        verbose_name = "Period"
        verbose_name_plural = "Periods"

    def __str__(self):
        return f"{self.tour.title}-{self.title}"
