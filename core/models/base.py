import uuid
from django.db import models
from autoslug import AutoSlugField
from core.models.contens import (
    HighlightTexts,
    InclusiveTexts,
    ExclusiveTexts,
    WhatKnowModel,
    WhatBringModel,
)


class TourModel(models.Model):
    tour_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    # İçerik
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )

    slug = AutoSlugField(
        unique=True,
        populate_from="title",
        max_length=355,
    )

    short_description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
    )

    highlights = models.ManyToManyField(
        HighlightTexts,
        blank=True,
    )

    full_description = models.TextField(
        max_length=3000,
        blank=True,
        null=True,
    )

    included = models.ManyToManyField(
        InclusiveTexts,
        blank=True,
    )

    excluded = models.ManyToManyField(
        ExclusiveTexts,
        blank=True,
    )

    what_to_know = models.ManyToManyField(
        WhatKnowModel,
        blank=True,
    )

    what_to_bring = models.ManyToManyField(
        WhatBringModel,
        blank=True,
    )

    # Formla ilgili sınırlamalar
    min_participant_for_a_booking = models.PositiveIntegerField(
        help_text="Bir rezervasyon için minimum katılımcı",
        blank=False,
        null=False,
        default=1,
    )

    max_participants_for_a_booking = models.PositiveIntegerField(
        default=15,
        blank=False,
        null=False,
        help_text="Bir rezervasyon için maximum katılımcı",
    )

    # Katılımcı tanımlamaları
    adult_age_start = models.PositiveIntegerField(
        blank=False,
        null=False,
        help_text="Yetiskin yasi baslangic",
        default=12,
    )

    adult_age_end = models.PositiveIntegerField(
        blank=False,
        null=False,
        help_text="Yetiskin yasi bitis",
        default=99,
    )

    adult_min_participant = models.PositiveIntegerField(
        blank=False,
        null=False,
        help_text="Bir rezervasyonda kabul edilecek MINimum yetiskin sayisi",
        default=1,
    )

    adult_max_participant = models.PositiveIntegerField(
        blank=False,
        null=False,
        help_text="Bir rezervasyonda kabul edilecek MAXimum yetiskin sayisi",
        default=10,
    )

    # Child
    child_age_start = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Cocuk yasi baslangic",
        default=3,
    )

    child_age_end = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Cocuk yasi bitis",
        default=11,
    )

    child_min_participant = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Bir rezervasyonda kabul edilecek MINimum cocuk sayisi",
        default=0,
    )

    child_max_participant = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Bir rezervasyonda kabul edilecek MAXimum cocuk sayisi",
        default=10,
    )

    duration = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="Tur suresi",
        default="6-7 hours",
    )

    pickup_description = models.TextField(
        max_length=2000,
        blank=False,
        null=False,
        default="All hotels in Side area",
    )

    is_active = models.BooleanField(
        default=True,
        blank=False,
        null=False,
    )

    date_added = models.DateTimeField(auto_now_add=False)
    date_edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_added",)
        verbose_name = "Tour"
        verbose_name_plural = "Tours"
        db_table = "tours"

    def __str__(self):
        return str(self.title)
