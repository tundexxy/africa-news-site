# mysite/users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views # Import Django's built-in auth views
from . import views # Import views from the current app (for 'register' view)

urlpatterns = [
    # Path for the custom registration page (using your users.views.register function)
    path('register/', views.register, name='register'),

    # Paths for Django's built-in login/logout views
    # LoginView uses a specific template to render the login form.
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # LogoutView logs out the user and then redirects to the specified page (homepage in this case).
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]