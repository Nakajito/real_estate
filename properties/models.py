from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Neighborhood(models.Model):
    class IconStyle(models.TextChoices):
        BUILDING = "building", "Edificio"
        MONUMENT = "monument", "Monumento"
        PIN = "pin", "Pin de mapa"

    name = models.CharField("nombre", max_length=120)
    slug = models.SlugField("slug", max_length=140, unique=True)
    icon_style = models.CharField(
        "estilo de icono",
        max_length=20,
        choices=IconStyle.choices,
        default=IconStyle.PIN,
    )
    sort_order = models.PositiveSmallIntegerField("orden", default=0)
    is_active = models.BooleanField("activa", default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "colonia"
        verbose_name_plural = "colonias"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Property(models.Model):
    class ListingType(models.TextChoices):
        BUY = "buy", "Compra"
        RENT = "rent", "Renta"

    class PropertyType(models.TextChoices):
        HOUSE = "house", "Casa"
        APARTMENT = "apartment", "Departamento"
        LAND = "land", "Terreno"
        OFFICE = "office", "Oficina"

    title = models.CharField("título", max_length=200)
    slug = models.SlugField("slug", max_length=220, unique=True)
    description = models.TextField("descripción", blank=True)
    listing_type = models.CharField(
        "tipo de operación",
        max_length=10,
        choices=ListingType.choices,
        default=ListingType.BUY,
    )
    property_type = models.CharField(
        "tipo de propiedad",
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.HOUSE,
    )
    price = models.DecimalField("precio", max_digits=14, decimal_places=2)
    currency = models.CharField("moneda", max_length=3, default="MXN")
    neighborhood = models.ForeignKey(
        Neighborhood,
        on_delete=models.PROTECT,
        related_name="properties",
        verbose_name="colonia",
    )
    borough = models.CharField("alcaldía", max_length=120, blank=True)
    address_line = models.CharField("dirección", max_length=255, blank=True)
    square_meters = models.PositiveIntegerField("m²", null=True, blank=True)
    parking_spots = models.PositiveSmallIntegerField(
        "estacionamientos", default=0
    )
    featured = models.BooleanField("destacada", default=False)
    published = models.BooleanField("publicada", default=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        ordering = ["-featured", "-created_at"]
        verbose_name = "propiedad"
        verbose_name_plural = "propiedades"
        indexes = [
            models.Index(fields=["featured", "listing_type"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("properties:detail", kwargs={"slug": self.slug})

    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "propiedad"
            slug = base
            n = 0
            while (
                Property.objects.filter(slug=slug)
                .exclude(pk=self.pk)
                .exists()
            ):
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="propiedad",
    )
    image = models.ImageField("imagen", upload_to="properties/%Y/%m/")
    is_primary = models.BooleanField("principal", default=False)
    sort_order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "imagen de propiedad"
        verbose_name_plural = "imágenes de propiedades"

    def __str__(self):
        return f"{self.property_id} — {self.image.name}"
