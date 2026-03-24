from django.test import Client, TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_returns_200(self):
        client = Client()
        response = client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)
