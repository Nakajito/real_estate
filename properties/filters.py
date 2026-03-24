import django_filters
from django.db.models import Q

from .models import Neighborhood, Property


class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label="Precio mínimo",
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label="Precio máximo",
    )
    neighborhood = django_filters.ModelChoiceFilter(
        queryset=Neighborhood.objects.filter(is_active=True).order_by("sort_order", "name"),
        label="Colonia",
        empty_label="Todas las colonias",
    )
    q = django_filters.CharFilter(
        method="filter_q",
        label="Buscar",
    )

    class Meta:
        model = Property
        fields = ["listing_type", "property_type", "neighborhood"]

    def filter_q(self, queryset, name, value):
        if not value or not value.strip():
            return queryset
        term = value.strip()
        return queryset.filter(
            Q(title__icontains=term) | Q(description__icontains=term)
        )
