from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad
from django.contrib.messages import get_messages

class MarkSoldAdViewTests(TestCase):
    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')

        # Create an active ad
        self.ad = Ad.objects.create(
            title="Test Ad",
            description="Test description",
            price=100,
            location="Test City",
            user=self.owner
        )

        self.client = Client()

    def test_owner_can_mark_sold(self):
        self.client.login(username='owner', password='pass')
        url = reverse('mark_sold_ad', args=[self.ad.pk])

        response = self.client.post(url, follow=True)
        self.ad.refresh_from_db()
        self.assertFalse(self.ad.is_active)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Ad marked as sold" in m.message for m in messages))

    def test_owner_can_reopen(self):
        self.ad.is_active = False
        self.ad.save()

        self.client.login(username='owner', password='pass')
        url = reverse('mark_sold_ad', args=[self.ad.pk])
        response = self.client.post(url, follow=True)
        self.ad.refresh_from_db()
        self.assertTrue(self.ad.is_active)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Ad marked as active" in m.message for m in messages))

    def test_non_owner_cannot_toggle(self):
        self.client.login(username='other', password='pass')
        url = reverse('mark_sold_ad', args=[self.ad.pk])

        response = self.client.post(url, follow=True)
        self.ad.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertTrue(self.ad.is_active)
