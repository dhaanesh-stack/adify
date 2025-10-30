from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, Category

class HomeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")

        cls.cat_electronics = Category.objects.create(name="Electronics")
        cls.cat_furniture = Category.objects.create(name="Furniture")

        cls.ad1 = Ad.objects.create(
            title="iPhone 15",
            description="Brand new iPhone 15 Pro Max",
            user=cls.user,
            category=cls.cat_electronics,
            price=120000,
            location="Chennai",
        )
        cls.ad2 = Ad.objects.create(
            title="Wooden Table",
            description="Used wooden table in good condition",
            user=cls.user,
            category=cls.cat_furniture,
            price=5000,
            location="Coimbatore",
        )
        cls.ad3 = Ad.objects.create(
            title="Laptop",
            description="Gaming laptop with RTX 4060",
            user=cls.user,
            category=cls.cat_electronics,
            price=80000,
            location="Chennai",
        )

    def setUp(self):
        self.url = reverse("home")  

    def test_home_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/home.html")
        self.assertIn("ads", response.context)
        self.assertIn("categories", response.context)

    def test_search_by_keyword(self):
        response = self.client.get(self.url, {"q": "iPhone"})
        ads = list(response.context["ads"])
        self.assertIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)
        self.assertNotIn(self.ad3, ads)

    def test_filter_by_category(self):
        response = self.client.get(self.url, {"category": self.cat_furniture.id})
        ads = list(response.context["ads"])
        self.assertIn(self.ad2, ads)
        self.assertNotIn(self.ad1, ads)
        self.assertNotIn(self.ad3, ads)

    def test_filter_by_location(self):
        response = self.client.get(self.url, {"location": "Chennai"})
        ads = list(response.context["ads"])
        self.assertIn(self.ad1, ads)
        self.assertIn(self.ad3, ads)
        self.assertNotIn(self.ad2, ads)

    def test_filter_by_price_range(self):
        response = self.client.get(self.url, {"min_price": 6000, "max_price": 90000})
        ads = list(response.context["ads"])
        self.assertIn(self.ad3, ads)
        self.assertNotIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)

    def test_combined_filters(self):
        response = self.client.get(
            self.url,
            {
                "q": "laptop",
                "category": self.cat_electronics.id,
                "min_price": 70000,
                "max_price": 100000,
                "location": "Chennai",
            },
        )
        ads = list(response.context["ads"])
        self.assertIn(self.ad3, ads)
        self.assertNotIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)
