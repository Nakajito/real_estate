from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from properties.models import Neighborhood, Property


class PropertyViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.neighborhood = Neighborhood.objects.create(
            name="Condesa",
            slug="condesa-test",
            sort_order=1,
        )
        cls.prop_buy = Property.objects.create(
            title="Casa en venta",
            slug="casa-venta-test",
            listing_type=Property.ListingType.BUY,
            property_type=Property.PropertyType.HOUSE,
            price=Decimal("5000000"),
            neighborhood=cls.neighborhood,
            published=True,
        )
        cls.prop_rent = Property.objects.create(
            title="Depto en renta",
            slug="depto-renta-test",
            listing_type=Property.ListingType.RENT,
            property_type=Property.PropertyType.APARTMENT,
            price=Decimal("35000"),
            neighborhood=cls.neighborhood,
            published=True,
        )
        cls.prop_high = Property.objects.create(
            title="Casa cara",
            slug="casa-cara-test",
            listing_type=Property.ListingType.BUY,
            property_type=Property.PropertyType.HOUSE,
            price=Decimal("15000000"),
            neighborhood=cls.neighborhood,
            published=True,
        )

    def setUp(self):
        self.client = Client()

    def test_list_filters_by_listing_type_rent(self):
        url = reverse("properties:list")
        response = self.client.get(url, {"listing_type": "rent"})
        self.assertEqual(response.status_code, 200)
        ids = {p.pk for p in response.context["property_list"]}
        self.assertIn(self.prop_rent.pk, ids)
        self.assertNotIn(self.prop_buy.pk, ids)

    def test_list_filters_price_range(self):
        url = reverse("properties:list")
        response = self.client.get(
            url,
            {"min_price": "4000000", "max_price": "6000000"},
        )
        self.assertEqual(response.status_code, 200)
        ids = {p.pk for p in response.context["property_list"]}
        self.assertIn(self.prop_buy.pk, ids)
        self.assertNotIn(self.prop_high.pk, ids)
        self.assertNotIn(self.prop_rent.pk, ids)

    def test_detail_ok(self):
        url = reverse("properties:detail", kwargs={"slug": self.prop_buy.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["property"], self.prop_buy)

    def test_detail_404_unknown_slug(self):
        url = reverse("properties:detail", kwargs={"slug": "no-existe"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unpublished_not_in_list(self):
        Property.objects.filter(pk=self.prop_buy.pk).update(published=False)
        url = reverse("properties:list")
        response = self.client.get(url)
        ids = {p.pk for p in response.context["property_list"]}
        self.assertNotIn(self.prop_buy.pk, ids)
