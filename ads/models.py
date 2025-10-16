from django.db import models
from django.contrib.auth.models import User

# Predefined categories
CATEGORY_CHOICES = [
    ('job', 'Job'),
    ('gig', 'Gig'),
    ('rental', 'Rental'),
    ('sale', 'For Sale'),
    ('service', 'Service'),
    ('event', 'Event'),
]

class Category(models.Model):
    """Represents a predefined ad category."""
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.get_name_display() if hasattr(self, 'get_name_display') else self.name


class Ad(models.Model):
    """Represents a single classified ad posted by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='ads')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ad_images/', null=True, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    show_contact = models.BooleanField(default=True)
    event_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
