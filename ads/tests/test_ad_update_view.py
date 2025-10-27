from django.test import TestCase
from django.urls import reverse
from ads.models import Ad, Category
from django.contrib.auth.models import User


class AdUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="pass123")
        self.other_user = User.objects.create_user(
            username="intruder", password="pass123"
        )
        self.ad = Ad.objects.create(
            title="Old Ad", description="desc", price=100, user=self.user
        )
        self.url = reverse("edit_ad", args=[self.ad.pk])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_owner_can_update(self):
        category = Category.objects.create(name="For sale")
        self.client.login(username="owner", password="pass123")

        response = self.client.post(
            self.url,
            {
                "title": "Updated Ad",
                "description": "A cool new ad",
                "category": category.id,
                "location": "Coimbatore",
                "price": 1500,
                "contact_email": "test@gmail.com",
                "contact_phone": "9876543210",
            },
        )

        self.assertRedirects(response, reverse("my_ads"))
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, "Updated Ad")

    def test_other_user_cannot_update(self):
        self.client.login(username="intruder", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        post_response = self.client.post(self.url, {"title": "Malicious Update"})
        self.assertEqual(post_response.status_code, 403)

        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, "Old Ad")
