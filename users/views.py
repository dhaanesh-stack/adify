from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            if phone_number and hasattr(user, 'profile'):
                user.profile.phone_number = phone_number
                user.profile.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')
