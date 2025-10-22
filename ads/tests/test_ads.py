from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, Category

User = get_user_model()

class AdsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpass")
        self.category = Category.objects.create(name="sale")
        self.ad = Ad.objects.create(
            user=self.user,
            title="Test Ad",
            description="Test description",
            category=self.category,
            price=100.00,
            contact_phone="1234567890",
            contact_email="test@example.com",
            show_contact=True,
            location="Test Location"
        )

    def test_post_ad_login_required(self):
        url = reverse("post_ad")
        response = self.client.get(url)
        self.assertRedirects(response, f"/users/login/?next={url}")

    def test_post_ad_creation_success(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("post_ad")
        data = {
            "title": "New Ad",
            "description": "New description",
            "category": str(self.category.id),
            "price": "200.00",
            "contact_phone": "9876543210",
            "contact_email": "new@example.com",
            "show_contact": "on",
            "location": "New Location"
        }
        response = self.client.post(url, data)
        new_ad = Ad.objects.filter(title="New Ad").first()
        self.assertIsNotNone(new_ad)
        self.assertEqual(new_ad.user, self.user)
        self.assertRedirects(response, reverse("my_ads"))

    def test_my_ads_shows_only_user_ads(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("my_ads")
        response = self.client.get(url)
        self.assertContains(response, "Test Ad")
        Ad.objects.create(
            user=self.other_user,
            title="Other Ad",
            description="Other description",
            category=self.category,
            price=50.00,
            contact_phone="1112223333",
            contact_email="other@example.com",
            show_contact=True,
            location="Other Location"
        )
        response = self.client.get(url)
        self.assertNotContains(response, "Other Ad")

    def test_edit_ad_permission_for_other_user(self):
        self.client.login(username="otheruser", password="otherpass")
        url = reverse("edit_ad", args=[self.ad.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_edit_ad_success(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("edit_ad", args=[self.ad.pk])
        data = {
            "title": "Updated Ad",
            "description": self.ad.description,
            "category": str(self.category.id),
            "price": str(self.ad.price),
            "contact_phone": self.ad.contact_phone,
            "contact_email": self.ad.contact_email,
            "show_contact": "on",
            "location": self.ad.location
        }
        response = self.client.post(url, data)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, "Updated Ad")
        self.assertRedirects(response, reverse("my_ads"))

    def test_delete_ad_permission_for_other_user(self):
        self.client.login(username="otheruser", password="otherpass")
        url = reverse("delete_ad", args=[self.ad.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_delete_ad_success(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("delete_ad", args=[self.ad.pk])
        response = self.client.post(url)
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())
        self.assertRedirects(response, reverse("my_ads"))
