import uuid
from django.db import models
from django.conf import settings
from core.models.base import TourModel


class BookingModel(models.Model):
    STATUS_CHOICES = (
        ("approved", "Approved"),
        ("created", "Created"),
        ("canceled", "Canceled"),
        ("changed", "Changed"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("paid", "Paid"),
        ("pay_later", "Pay Later"),
        ("refunded", "Refunded"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created",
        blank=False,
        null=False,
    )

    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    tour = models.ForeignKey(
        to=TourModel,
        on_delete=models.CASCADE,
        related_name="tourbookings",
        null=False,
        blank=False,
    )

    tour_date = models.DateField(
        blank=False,
        null=False,
    )

    pick_up_time = models.CharField(
        max_length=5,
        blank=False,
        null=False,
    )

    full_name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )

    email = models.EmailField(
        max_length=150,
        blank=False,
        null=False,
    )

    phone = models.CharField(
        max_length=25,
        blank=False,
        null=False,
    )

    adults = models.PositiveIntegerField(
        blank=False,
        null=False,
        default=1,
    )

    children = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    hotel_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )

    message = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        default="",
    )

    total_cost = models.DecimalField(
        max_digits=6, decimal_places=2, blank=False, null=False
    )

    selected_curreny = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        default="EUR",
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)
        db_table = "bookings"
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return str(self.booking_id)

    # def final_payment(self, period):
    #     if period.discount_rate:
    #         return (self.adults * period.adult_price) + (
    #             self.children * period.child_price
    #         ) / 100 * (100 - period.discount_rate)
    #     else:
    #         return (self.adults * period.adult_price) + (
    #             self.children * period.child_price
    #         )
