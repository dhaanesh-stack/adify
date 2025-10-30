from django.test import TestCase
from django.urls import reverse
from ads.models import Ad
from django.contrib.auth.models import User

class AdDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="deleter", password="pass123")
        self.other_user = User.objects.create_user(username="hacker", password="pass123")
        self.ad = Ad.objects.create(title="Delete Me", description="desc", price=500, user=self.user)
        self.url = reverse('delete_ad', args=[self.ad.pk])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, '/accounts/login/?next=' + self.url)

    def test_owner_can_delete(self):
        self.client.login(username="deleter", password="pass123")
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('my_ads'))
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username="hacker", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
