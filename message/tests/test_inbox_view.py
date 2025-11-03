from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, Category
from message.models import Message

User = get_user_model()


class InboxViewTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username="seller", password="pass123")
        self.buyer = User.objects.create_user(username="buyer", password="pass123")
        self.other_user = User.objects.create_user(username="other", password="pass123")

        self.category = Category.objects.create(name="sale")

        self.ad = Ad.objects.create(
            user=self.seller,
            title="Test Ad",
            description="Some description",
            category=self.category,
            price=100
        )

        Message.objects.create(sender=self.buyer, receiver=self.seller, ad=self.ad, content="Hi Seller!")
        Message.objects.create(sender=self.buyer, receiver=self.seller, ad=self.ad, content="Are you there?", is_read=True)

        Message.objects.create(sender=self.other_user, receiver=self.seller, ad=self.ad, content="Hello!")

        self.url = reverse("inbox")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{reverse("login")}?next={self.url}')

    def test_inbox_view_as_seller(self):
        self.client.login(username="seller", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "message/inbox.html")

        conversations = response.context["conversations"]
        self.assertEqual(len(conversations), 2)

        unread_total = sum(conv["unread_count"] for conv in conversations)
        self.assertEqual(unread_total, 2)

    def test_inbox_view_as_buyer(self):
        self.client.login(username="buyer", password="pass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        conversations = response.context["conversations"]
        self.assertEqual(len(conversations), 1)
        unread_total = sum(conv["unread_count"] for conv in conversations)
        self.assertEqual(unread_total, 0)
