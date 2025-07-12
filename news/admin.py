# news/admin.py

from django.contrib import admin
from .models import Article, Follow # Import your Article and new Follow models

# Register your models here.
# This line assumes you have an Article model.
# If you don't, you can comment it out or remove it for now.
admin.site.register(Article)

# Register the Follow model to make it accessible in the Django admin interface.
admin.site.register(Follow)