from django.shortcuts import render

from .models import Service, Testimonial
from properties.models import Neighborhood, Property


def home(request):
    featured = (
        Property.objects.filter(published=True, featured=True)
        .select_related("neighborhood")
        .prefetch_related("images")[:6]
    )
    neighborhoods = Neighborhood.objects.filter(is_active=True).order_by(
        "sort_order", "name"
    )
    services = Service.objects.filter(is_active=True).order_by("sort_order", "id")
    testimonials = Testimonial.objects.filter(is_published=True).order_by(
        "sort_order", "id"
    )
    return render(
        request,
        "pages/home.html",
        {
            "featured_properties": featured,
            "neighborhoods": neighborhoods,
            "services": services,
            "testimonials": testimonials,
        },
    )
