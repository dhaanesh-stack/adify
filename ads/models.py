from django.db import models
from django.conf import settings

# Predefined categories
class CategoryType(models.TextChoices):
    JOB = 'job', 'Job'
    GIG = 'gig', 'Gig'
    RENTAL = 'rental', 'Rental'
    SALE = 'sale', 'For Sale'
    SERVICE = 'service', 'Service'
    EVENT = 'event', 'Event'

class Category(models.Model):
    """Represents a predefined ad category."""
    name = models.CharField(max_length=50, choices=CategoryType.choices, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.get_name_display()


class Ad(models.Model):
    """Represents a single classified ad posted by a user."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='ads')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ad_images/%Y/%m/%d/', null=True, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    show_contact = models.BooleanField(default=True)
    event_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
