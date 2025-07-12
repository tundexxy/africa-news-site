# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages # Import messages for feedback

def register(request):
    """
    Handles user registration. Displays a registration form and creates a new user.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately after registration
            messages.success(request, f"Account created for {user.username}! You are now logged in.")
            return redirect('article_list') # Redirect to the home page or dashboard
        else:
            # Add form errors to messages for display
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    """
    Handles user login. Displays a login form and authenticates the user.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}! You are now logged in.")
                return redirect('article_list') # Redirect to home page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    """
    Handles user logout. Logs the user out and redirects to the home page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('article_list') # Redirect to home page