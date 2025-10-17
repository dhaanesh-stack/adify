from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, Category, CategoryType

class HomePageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username="testuser", password="password123")

        # Create categories
        cls.categories = []
        for cat in ['job', 'gig', 'rental', 'sale', 'service', 'event']:
            category, _ = Category.objects.get_or_create(name=cat)
            cls.categories.append(category)

        # Create 10 test ads
        for i in range(10):
            Ad.objects.create(
                user=cls.user,
                title=f"Test Ad {i+1}",
                description=f"This is a description for ad {i+1}.",
                category=cls.categories[i % len(cls.categories)],
                price=1000 + i*100,
                location="Test City",
                contact_email="test@example.com",
                contact_phone="9999999999",
                show_contact=True
            )

    def test_homepage_status_code(self):
        """Homepage returns 200 OK."""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_template_used(self):
        """Homepage uses the correct template."""
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, "home.html")

    def test_homepage_lists_ads(self):
        """All ads are present in the context."""
        url = reverse('home')
        response = self.client.get(url)
        self.assertIn('ads', response.context)
        self.assertEqual(len(response.context['ads']), 6)  # paginate_by=6

    def test_pagination_is_six(self):
        """Pagination displays 6 ads per page."""
        url = reverse('home')
        response = self.client.get(url)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['ads']), 6)

    def test_second_page_contains_remaining_ads(self):
        """Second page contains the remaining ads."""
        url = reverse('home') + '?page=2'
        response = self.client.get(url)
        self.assertEqual(len(response.context['ads']), 4)  # 10 total ads, 6 on first page

    def test_ads_without_images_show_default(self):
        """Ads with no image can still render the template."""
        # This ad has no image
        Ad.objects.create(
            user=self.user,
            title="No Image Ad",
            description="No image description",
            category=self.categories[0],
            price=500,
            location="City",
            contact_email="noimage@example.com",
            contact_phone="8888888888",
            show_contact=True
        )
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, "No Image Ad")
