from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Profile


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        phone_number = form.cleaned_data.get("phone_number")
        Profile.objects.update_or_create(
            user=user, defaults={"phone_number": phone_number}
        )
        login(self.request, user)
        messages.success(self.request, "Registration successful!")
        return response


class UserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)
