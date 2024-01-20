    
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})

@login_required(login_url='account:login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('main:home')

@login_required(login_url='account:login')
def dashboard(request):
    user = request.user
    return render(request, 'account/dashboard.html', {'user': user})