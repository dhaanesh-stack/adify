from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, Category
from message.models import Message

User = get_user_model()

class AdChatViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")
        self.category = Category.objects.create(name="sale")
        self.ad_user1 = Ad.objects.create(
            user=self.user1,
            title="Ad from user1",
            description="Description",
            category=self.category,
            price=100,
            location="City",
            contact_email="user1@example.com"
        )
        self.ad_user2 = Ad.objects.create(
            user=self.user2,
            title="Ad from user2",
            description="Description",
            category=self.category,
            price=200,
            location="Town",
            contact_email="user2@example.com"
        )

    def test_login_required(self):
        url = reverse("chat_ad", kwargs={"pk": self.ad_user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_chat_own_ad(self):
        self.client.login(username="user1", password="pass123")
        url = reverse("chat_ad", kwargs={"pk": self.ad_user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_user_can_chat_on_others_ad(self):
        self.client.login(username="user1", password="pass123")
        url = reverse("chat_ad", kwargs={"pk": self.ad_user2.id})
        response = self.client.post(url, {"content": "Hi there"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(content="Hi there").exists())
