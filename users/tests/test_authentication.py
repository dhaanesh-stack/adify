from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(TestCase):
    """Test cases for user registration, login, and logout."""

    def setUp(self):
        """Create a test user for login/logout tests."""
        self.user_credentials = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        self.user = User.objects.create_user(**self.user_credentials)

    def test_registration_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_can_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'NewPass123',
            'password2': 'NewPass123',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.profile.phone_number, '1234567890')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_can_login(self):
        response = self.client.post(reverse('login'), {
            'username': self.user_credentials['username'],
            'password': self.user_credentials['password']
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_with_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': self.user_credentials['username'],
            'password': 'WrongPass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "Please enter a correct username and password")

    def test_user_can_logout(self):
        self.client.login(
            username=self.user_credentials['username'],
            password=self.user_credentials['password']
        )
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
