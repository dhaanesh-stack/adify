from django.core import mail
from django.test import TestCase
from django.core.mail import send_mail

class SendMailTest(TestCase):
    def test_send_mail_success(self):
        send_mail(
            subject="Test Email from Django",
            message="This is a test email from Adify.",
            from_email="dhaaneshs712@gmail.com",
            recipient_list=["dhaanesh@testpress.com"],
        )
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Test Email from Django")
        self.assertEqual(email.body, "This is a test email from Adify.")
        self.assertEqual(email.from_email, "dhaaneshs712@gmail.com")
        self.assertIn("dhaanesh@testpress.com", email.to)
