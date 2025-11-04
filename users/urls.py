from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from .forms import (
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from .views import UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html',authentication_form=CustomAuthenticationForm),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(next_page='login'),
        name='logout'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(template_name='users/password_reset.html',  form_class=CustomPasswordResetForm),
        name='password_reset'
    ),

    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', form_class=CustomSetPasswordForm),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]