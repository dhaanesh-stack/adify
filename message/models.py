from django.db import models
from django.conf import settings
from ads.models import Ad

class Message(models.Model):
    """Represents a message sent from a buyer to a seller for a specific ad."""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='received_messages')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Message from {self.sender.username} regarding "{self.ad.title}"'
