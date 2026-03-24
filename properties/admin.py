from django.contrib import admin

from .models import Neighborhood, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon_style", "sort_order", "is_active")
    list_filter = ("is_active", "icon_style")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "listing_type",
        "property_type",
        "price",
        "neighborhood",
        "featured",
        "published",
    )
    list_filter = (
        "listing_type",
        "property_type",
        "featured",
        "published",
        "neighborhood",
    )
    search_fields = ("title", "description", "address_line", "borough")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("neighborhood",)
    inlines = [PropertyImageInline]
