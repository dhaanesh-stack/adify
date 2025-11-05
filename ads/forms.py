from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = [
            'title', 'description', 'category', 'price',
            'location', 'image', 'contact_email',
            'contact_phone', 'show_contact', 'event_date'
        ]