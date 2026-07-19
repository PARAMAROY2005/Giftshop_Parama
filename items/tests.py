from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Gift


class AuthAccessTests(TestCase):
    def setUp(self):
        self.gift = Gift.objects.create(name="Mug", price=100, details="Test gift")
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="securepass123",
        )

    def test_guest_cannot_add_to_wishlist(self):
        response = self.client.get(reverse("add_to_wishlist", args=[self.gift.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_guest_home_shows_profile_link_to_login(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, reverse("login"))

    def test_logged_in_user_sees_profile_link(self):
        self.client.login(username="tester", password="securepass123")
        response = self.client.get(reverse("home"))

        self.assertContains(response, reverse("profile"))

    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_checkout_page_renders(self):
        from items.models import Cart
        Cart.objects.create(gift=self.gift, quantity=1)
        self.client.login(username="tester", password="securepass123")
        response = self.client.get(reverse("checkout"))

        self.assertEqual(response.status_code, 200)

    def test_my_orders_page_renders_for_authenticated_user(self):
        self.client.login(username="tester", password="securepass123")
        response = self.client.get(reverse("my_orders"))

        self.assertEqual(response.status_code, 200)
