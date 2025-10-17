from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        phone_number = form.cleaned_data.get("phone_number")
        if phone_number:
            user.profile.phone_number = phone_number
            user.profile.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful!")
        return response
