# mysite/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')), # Include URLs from the 'news' app
    path('accounts/', include('accounts.urls')), # Include URLs from the 'accounts' app
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)