from django.views.generic import DetailView, ListView

from .filters import PropertyFilter
from .models import Neighborhood, Property


class PropertyListView(ListView):
    model = Property
    template_name = "properties/property_list.html"
    context_object_name = "property_list"
    paginate_by = 9

    def get_queryset(self):
        qs = (
            Property.objects.filter(published=True)
            .select_related("neighborhood")
            .prefetch_related("images")
        )
        self.filterset = PropertyFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter"] = self.filterset
        ctx["neighborhoods"] = Neighborhood.objects.filter(is_active=True).order_by(
            "sort_order", "name"
        )
        q = self.request.GET.copy()
        q.pop("page", None)
        ctx["filter_query"] = q.urlencode()
        return ctx


class PropertyDetailView(DetailView):
    model = Property
    template_name = "properties/property_detail.html"
    context_object_name = "property"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Property.objects.filter(published=True)
            .select_related("neighborhood")
            .prefetch_related("images")
        )
