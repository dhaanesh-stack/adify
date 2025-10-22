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
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
