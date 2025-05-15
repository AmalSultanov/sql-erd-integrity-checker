from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from integrity_checker.main.forms import UserRegistrationForm


def homepage(request):
    return render(request, 'index.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            login(request, user)
            return redirect('main:home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('main:home')
