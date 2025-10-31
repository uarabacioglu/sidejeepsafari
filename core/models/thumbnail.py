import uuid
import PIL
from django.db import models
from core.models.base import TourModel


def thumbnail_image_upload_path(instance, filename):
    return f"thumbnails/{instance.tour.tour_id}/{filename}"


class ThumbnailModel(models.Model):
    image_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    image = models.ImageField(
        upload_to=thumbnail_image_upload_path,
        blank=False,
        null=False,
    )

    alt_text = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

    tour = models.OneToOneField(
        to=TourModel,
        on_delete=models.CASCADE,
        related_name="tour_thumbnail",
    )

    class Meta:
        db_table = "thumbnail"
        verbose_name = "Thumbnail"
        verbose_name_plural = "Thumbnail"

    def __str__(self):
        return str(self.image)

    def save(self, *args, **kwargs):
        """Resmi yeniden boyutlandır ve kaydet."""
        super().save(*args, **kwargs)

        if self.image:
            image_path = self.image.path
            try:
                img = PIL.Image.open(image_path)

                if img.format not in ["JPEG", "JPG", "PNG"]:
                    raise ValueError("Unsupported image format.")

                width, height = img.size
                target_width = 800

                if width > target_width:
                    h_coefficient = width / target_width
                    target_height = height / h_coefficient
                    img = img.resize((int(target_width), int(target_height)))
                    img.save(image_path, quality=100)

                img.close()

            except Exception as e:
                print(f"Error processing image for ThumbnailModel: {e}")
