import uuid
from django.db import models
from core.models.booking import BookingModel


class PaymentModel(models.Model):
    STATUS_CHOICES = (
        ("approved", "Approved"),
        ("created", "Created"),
        ("failed", "Failed"),
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("refund", "Refund"),
    )

    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("iyzico", "Iyzico"),
        ("paypal", "Paypal"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created",
        blank=False,
        null=False,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="cash",
        blank=False,
        null=False,
    )

    # user = models.ForeignKey(
    #     to=settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     # TODO payment user!
    #     related_name="paypaluser",
    #     blank=True,
    #     null=True,
    # )

    payment_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    payer_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
    )

    currency = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        default="EUR",
    )

    booking = models.OneToOneField(
        to=BookingModel,
        on_delete=models.CASCADE,
        related_name="bookingpayment",
        blank=False,
        null=False,
    )

    booking_uuid = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )

    tour_date = models.DateField(
        blank=False,
        null=False,
    )

    customer_full_name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )

    customer_phone = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )

    customer_email = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )

    date_added = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payments"

    def __str__(self):
        return f"{self.booking.full_name}"
