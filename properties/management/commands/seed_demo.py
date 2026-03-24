from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from pages.models import Service, Testimonial
from properties.models import Neighborhood, Property


class Command(BaseCommand):
    help = "Crea colonias, servicios, testimonios y propiedades de demostración."

    @transaction.atomic
    def handle(self, *args, **options):
        neighborhoods_data = [
            ("Condesa", "condesa", Neighborhood.IconStyle.BUILDING, 1),
            ("Polanco", "polanco", Neighborhood.IconStyle.MONUMENT, 2),
            ("Roma", "roma", Neighborhood.IconStyle.PIN, 3),
            ("Roma Norte", "roma-norte", Neighborhood.IconStyle.PIN, 4),
            ("Coyoacán", "coyoacan", Neighborhood.IconStyle.MONUMENT, 5),
            ("Santa Fe", "santa-fe", Neighborhood.IconStyle.BUILDING, 6),
        ]
        neighborhoods = {}
        for name, slug, icon, order in neighborhoods_data:
            n, created = Neighborhood.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "icon_style": icon,
                    "sort_order": order,
                    "is_active": True,
                },
            )
            neighborhoods[slug] = n
            self.stdout.write(
                f"  Colonia {'creada' if created else 'actualizada'}: {name}"
            )

        services_data = [
            (
                "Asesoría profesional",
                "Acompañamiento en cada paso de tu operación.",
                Service.IconChoice.ADVICE,
                1,
            ),
            (
                "Valuación gratis",
                "Estimación orientativa sin costo.",
                Service.IconChoice.VALUATION,
                2,
            ),
            (
                "Gestión de créditos",
                "Te conectamos con opciones de financiamiento.",
                Service.IconChoice.CREDIT,
                3,
            ),
            (
                "Marketing digital",
                "Visibilidad en portales y redes.",
                Service.IconChoice.MARKETING,
                4,
            ),
        ]
        for title, desc, icon, order in services_data:
            obj, created = Service.objects.update_or_create(
                title=title,
                defaults={
                    "short_description": desc,
                    "icon": icon,
                    "sort_order": order,
                    "is_active": True,
                },
            )
            self.stdout.write(
                f"  Servicio {'creado' if created else 'actualizado'}: {title}"
            )

        testimonials_data = [
            (
                "María González",
                "El equipo fue claro y rápido. Encontramos departamento en Roma sin estrés.",
                5,
                1,
            ),
            (
                "Carlos Ruiz",
                "Buena valuación y seguimiento durante la venta en Polanco.",
                5,
                2,
            ),
            (
                "Ana Martínez",
                "Recomiendo la asesoría para créditos; todo muy transparente.",
                4,
                3,
            ),
        ]
        for name, quote, rating, order in testimonials_data:
            obj, created = Testimonial.objects.update_or_create(
                name=name,
                defaults={
                    "quote": quote,
                    "rating": rating,
                    "sort_order": order,
                    "is_published": True,
                },
            )
            self.stdout.write(
                f"  Testimonio {'creado' if created else 'actualizado'}: {name}"
            )

        props = [
            {
                "title": "Casa moderna en Polanco: 3 rec, 4 baños, jardín",
                "slug": "casa-moderna-polanco",
                "listing_type": Property.ListingType.BUY,
                "property_type": Property.PropertyType.HOUSE,
                "price": Decimal("12500000"),
                "neighborhood": neighborhoods["polanco"],
                "borough": "Miguel Hidalgo",
                "square_meters": 240,
                "parking_spots": 2,
                "featured": True,
                "description": "Residencia con acabados de lujo y jardín privativo.",
            },
            {
                "title": "Departamento luminoso en Condesa",
                "slug": "depto-condesa-luminoso",
                "listing_type": Property.ListingType.RENT,
                "property_type": Property.PropertyType.APARTMENT,
                "price": Decimal("45000"),
                "neighborhood": neighborhoods["condesa"],
                "borough": "Cuauhtémoc",
                "square_meters": 95,
                "parking_spots": 1,
                "featured": True,
                "description": "Dos recámaras, balcón y excelente ubicación.",
            },
            {
                "title": "Penthouse en Santa Fe",
                "slug": "penthouse-santa-fe",
                "listing_type": Property.ListingType.BUY,
                "property_type": Property.PropertyType.APARTMENT,
                "price": Decimal("18500000"),
                "neighborhood": neighborhoods["santa-fe"],
                "borough": "Álvaro Obregón",
                "square_meters": 310,
                "parking_spots": 3,
                "featured": True,
                "description": "Vista panorámica y amenidades de torre.",
            },
            {
                "title": "Casa en Coyoacán",
                "slug": "casa-coyoacan",
                "listing_type": Property.ListingType.BUY,
                "property_type": Property.PropertyType.HOUSE,
                "price": Decimal("8900000"),
                "neighborhood": neighborhoods["coyoacan"],
                "borough": "Coyoacán",
                "square_meters": 180,
                "parking_spots": 2,
                "featured": False,
                "description": "Estilo colonial renovado, patio central.",
            },
            {
                "title": "Terreno en Roma Norte",
                "slug": "terreno-roma-norte",
                "listing_type": Property.ListingType.BUY,
                "property_type": Property.PropertyType.LAND,
                "price": Decimal("22000000"),
                "neighborhood": neighborhoods["roma-norte"],
                "borough": "Cuauhtémoc",
                "square_meters": 200,
                "parking_spots": 0,
                "featured": False,
                "description": "Excelente frente, uso de suelo habitacional.",
            },
            {
                "title": "Oficina ejecutiva en Polanco",
                "slug": "oficina-polanco",
                "listing_type": Property.ListingType.RENT,
                "property_type": Property.PropertyType.OFFICE,
                "price": Decimal("120000"),
                "neighborhood": neighborhoods["polanco"],
                "borough": "Miguel Hidalgo",
                "square_meters": 120,
                "parking_spots": 2,
                "featured": True,
                "description": "Espacio listo para ocupar, sala de juntas.",
            },
        ]
        for data in props:
            slug = data.pop("slug")
            n = data.pop("neighborhood")
            obj, created = Property.objects.update_or_create(
                slug=slug,
                defaults={**data, "neighborhood": n, "published": True},
            )
            self.stdout.write(
                f"  Propiedad {'creada' if created else 'actualizada'}: {obj.title}"
            )

        self.stdout.write(self.style.SUCCESS("Datos de demostración listos."))
