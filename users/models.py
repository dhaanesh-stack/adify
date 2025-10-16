from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """Extends the default Django User model with additional optional information."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
