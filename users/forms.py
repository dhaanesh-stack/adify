from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

User = get_user_model()

INPUT_CLS = "w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholder_map = {
            "username": "Username",
            "email": "Email address",
            "phone_number": "Phone number (optional)",
            "password1": "Password",
            "password2": "Confirm password",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": INPUT_CLS,
                "placeholder": placeholder_map.get(name, ""),
                "autocomplete": "new-password" if name in ("password1", "password2") else "on",
            })


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholder_map = {
            "username": "Username or email",
            "password": "Password",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": INPUT_CLS,
                "placeholder": placeholder_map.get(name, ""),
                "autocomplete": "current-password" if name == "password" else "username",
            })


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder_map = {
            "email": "Enter your registered email address",
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": INPUT_CLS,
                "placeholder": placeholder_map.get(name, ""),
            })


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholder_map = {
            "new_password1": "New password",
            "new_password2": "Confirm new password",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": INPUT_CLS,
                "placeholder": placeholder_map.get(name, ""),
                "autocomplete": "new-password",
            })
