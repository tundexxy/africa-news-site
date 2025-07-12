# mysite/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Django's built-in form for user registration
from django.contrib import messages # For displaying success/error messages

def register(request):
    """
    Handles user registration.
    If the request is POST, it tries to create a new user.
    If the request is GET, it displays an empty registration form.
    """
    if request.method == 'POST':
        # If form is submitted, bind data from the request to the form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # If form data is valid, save the new user to the database
            form.save()
            username = form.cleaned_data.get('username')
            # Display a success message to the user
            messages.success(request, f'Account created for {username}! You can now log in.')
            # Redirect to the login page (NOW THIS URL EXISTS!) after successful registration
            return redirect('login')
        else:
            # If form is not valid, display an error message
            messages.error(request, 'Error creating your account. Please correct the errors below.')
    else:
        # If it's a GET request, create an empty form to display
        form = UserCreationForm()
    
    # Render the registration template, passing the form to it
    return render(request, 'users/register.html', {'form': form})