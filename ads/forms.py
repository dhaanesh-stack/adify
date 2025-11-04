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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_classes = "w-full border border-gray-300 rounded-md p-2 outline-none focus:outline-indigo-500 focus:ring-2 focus:ring-indigo-500"
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.NumberInput, forms.URLInput, forms.Textarea, forms.Select)):
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{existing_classes} {common_classes}".strip()