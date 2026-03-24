from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Service(models.Model):
    class IconChoice(models.TextChoices):
        ADVICE = "advice", "Asesoría"
        VALUATION = "valuation", "Valuación"
        CREDIT = "credit", "Créditos"
        MARKETING = "marketing", "Marketing"

    title = models.CharField("título", max_length=120)
    short_description = models.CharField("descripción breve", max_length=255)
    icon = models.CharField(
        "icono",
        max_length=20,
        choices=IconChoice.choices,
        default=IconChoice.ADVICE,
    )
    sort_order = models.PositiveSmallIntegerField("orden", default=0)
    is_active = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "servicio"
        verbose_name_plural = "servicios"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField("nombre", max_length=120)
    photo = models.ImageField(
        "foto", upload_to="testimonials/", blank=True, null=True
    )
    quote = models.TextField("testimonio")
    rating = models.PositiveSmallIntegerField(
        "calificación",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    sort_order = models.PositiveSmallIntegerField("orden", default=0)
    is_published = models.BooleanField("publicado", default=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "testimonio"
        verbose_name_plural = "testimonios"

    def __str__(self):
        return self.name
