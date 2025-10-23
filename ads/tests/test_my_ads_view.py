from django.test import TestCase
from django.urls import reverse
from ads.models import Ad
from django.contrib.auth.models import User

class MyAdsViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")
        Ad.objects.create(title="Ad by user1", description="desc", price=100, user=self.user1)
        Ad.objects.create(title="Ad by user2", description="desc", price=200, user=self.user2)
        self.url = reverse('my_ads')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/users/login/?next=' + self.url)

    def test_logged_in_user_only_sees_own_ads(self):
        self.client.login(username="user1", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ad by user1")
        self.assertNotContains(response, "Ad by user2")
