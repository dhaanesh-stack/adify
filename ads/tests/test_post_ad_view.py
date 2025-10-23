from django.test import TestCase
from django.urls import reverse
from ads.models import Category, Ad
from django.contrib.auth.models import User


class PostAdViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="poster", password="pass123")
        self.url = reverse("post_ad")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, "/users/login/?next=" + self.url)

    def test_logged_in_user_can_post_ad(self):
        category = Category.objects.create(name="For sale")

        self.client.login(username="poster", password="pass123")

        response = self.client.post(
            self.url,
            {
                "title": "New Ad",
                "description": "A cool new ad",
                "category": category.id, 
                "location": "Coimba",
                "price": 1500,
                "contact_email": "test@gmail.com",
                "contact_phone": "9876543210",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='New Ad').exists())