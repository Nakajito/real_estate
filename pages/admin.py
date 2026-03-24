from django.contrib import admin

from .models import Service, Testimonial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "sort_order", "is_active")
    list_filter = ("is_active", "icon")
    search_fields = ("title", "short_description")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "sort_order", "is_published")
    list_filter = ("is_published", "rating")
    search_fields = ("name", "quote")
