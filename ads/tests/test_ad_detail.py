from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Ad, Category


class AdDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.category = Category.objects.create(name="For Sale")
        self.ad = Ad.objects.create(
            user=self.user,
            title="Test Ad",
            description="This is a test ad description.",
            category=self.category,
            price=1000,
            location="Test City",
            contact_email="test@example.com",
            contact_phone="1234567890",
            show_contact=True,
        )
        self.url = reverse("ad_detail", kwargs={"pk": self.ad.pk})

    def test_ad_detail_view_redirects_for_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_ad_detail_view_status_code_for_authenticated_user(self):
        self.client.login(username="tester", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_ad_detail_view_template(self):
        self.client.login(username="tester", password="pass123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "ads/ad_detail.html")

    def test_ad_detail_view_context(self):
        self.client.login(username="tester", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.context["ad"], self.ad)

    def test_ad_detail_view_content(self):
        self.client.login(username="tester", password="pass123")
        response = self.client.get(self.url)
        self.assertContains(response, self.ad.title)
        self.assertContains(response, self.ad.description)
        self.assertContains(response, self.ad.price)
        self.assertContains(response, self.ad.location)
        self.assertContains(response, self.ad.category.name)
        self.assertContains(response, self.ad.contact_email)
        self.assertContains(response, self.ad.contact_phone)

    def test_ad_detail_view_nonexistent_ad(self):
        self.client.login(username="tester", password="pass123")
        url = reverse("ad_detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
