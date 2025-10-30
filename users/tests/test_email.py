from django.core import mail
from django.test import TestCase
from django.core.mail import send_mail

class SendMailTest(TestCase):
    def test_send_mail_success(self):
        subject = "Test Email from Django"
        message = "This is a test email from Adify."
        from_email = "dhaaneshs712@gmail.com"
        recipient = "dhaanesh@testpress.com"
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recipient],
        )
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, message)
        self.assertEqual(email.from_email, from_email)
        self.assertIn(recipient, email.to)