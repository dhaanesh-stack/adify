from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Extends the default Django User model with additional optional information.
    Single Responsibility: only stores extra user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
