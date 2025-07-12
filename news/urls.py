# mysite/news/urls.py

from django.urls import path
# Import all necessary views: ArticleListView, ArticleDetailView, and our new follow/unfollow views
from .views import ArticleListView, ArticleDetailView, follow_user, unfollow_user

urlpatterns = [
    # Path for the list of all articles (your homepage)
    path('', ArticleListView.as_view(), name='article_list'),
    
    # Path for a single article detail page.
    # IMPORTANT: We are now using '<int:pk>/' (primary key) to identify the article.
    # Your Article model currently doesn't have a 'slug' field.
    # If you later add a 'slug' field to your Article model in news/models.py
    # (and run makemigrations/migrate again), you can change this line back to:
    # path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),

    # New URLs for follow/unfollow functionality
    # These paths are designed to be hit by JavaScript (AJAX) requests
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
]