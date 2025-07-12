# mysite/news/views.py

from django.views.generic import ListView, DetailView # Import Django's generic views
from django.contrib.auth.models import User # Import Django's built-in User model
from .models import Article, Follow # Import our Article and new Follow models
from django.shortcuts import get_object_or_404, redirect # For fetching objects or redirecting
from django.contrib.auth.decorators import login_required # To ensure only logged-in users can follow
from django.utils.decorators import method_decorator # For applying decorators to class-based views
from django.http import JsonResponse # For AJAX responses

class ArticleListView(ListView):
    """
    This view displays a list of all news articles.
    It's perfect for your homepage showing the latest headlines.
    """
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_articles'] = Article.objects.all().order_by('-published_date')[:5]
        return context

class ArticleDetailView(DetailView):
    """
    This view displays the full content of a single news article.
    It's what happens when you click on a headline.
    """
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    # Note: Your Article model doesn't currently have a 'slug' field.
    # If you intend to use slugs for URLs, you'll need to add
    # `slug = models.SlugField(unique=True, max_length=200)`
    # to your Article model in news/models.py and run makemigrations/migrate again.
    # For now, these lines are commented out to avoid errors if slug is not present.
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_articles'] = Article.objects.all().order_by('-published_date')[:5]
        
        # Add author information and follow status to the context
        article_author = self.get_object().author # Get the author of the current article
        context['article_author'] = article_author

        if self.request.user.is_authenticated:
            # Check if the current logged-in user is following this article's author
            is_following = Follow.objects.filter(
                follower=self.request.user,
                following=article_author
            ).exists()
            context['is_following'] = is_following
        else:
            context['is_following'] = False # Not following if not logged in

        # Get the count of followers for the article's author
        follower_count = Follow.objects.filter(following=article_author).count()
        context['follower_count'] = follower_count

        return context

# View to handle following a user
@login_required # Ensures only logged-in users can access this view
def follow_user(request, user_id):
    # Ensure it's a POST request for security
    if request.method == 'POST':
        # Get the user to be followed (the 'following' user)
        user_to_follow = get_object_or_404(User, id=user_id)
        
        # The user who is doing the following (the 'follower')
        follower_user = request.user

        # Prevent a user from following themselves
        if follower_user == user_to_follow:
            return JsonResponse({'status': 'error', 'message': 'Cannot follow yourself.'}, status=400)

        # Create the follow relationship if it doesn't already exist
        follow, created = Follow.objects.get_or_create(
            follower=follower_user,
            following=user_to_follow
        )
        
        if created:
            # If a new follow relationship was created
            follower_count = Follow.objects.filter(following=user_to_follow).count()
            return JsonResponse({'status': 'success', 'action': 'followed', 'follower_count': follower_count})
        else:
            # If the user was already following
            follower_count = Follow.objects.filter(following=user_to_follow).count()
            return JsonResponse({'status': 'info', 'action': 'already_followed', 'follower_count': follower_count})
    
    # If not a POST request, redirect or return an error
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


# View to handle unfollowing a user
@login_required # Ensures only logged-in users can access this view
def unfollow_user(request, user_id):
    # Ensure it's a POST request for security
    if request.method == 'POST':
        # Get the user to be unfollowed (the 'following' user)
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        # The user who is doing the unfollowing (the 'follower')
        follower_user = request.user

        # Delete the follow relationship
        deleted_count, _ = Follow.objects.filter(
            follower=follower_user,
            following=user_to_unfollow
        ).delete()
        
        if deleted_count > 0:
            # If a follow relationship was successfully deleted
            follower_count = Follow.objects.filter(following=user_to_unfollow).count()
            return JsonResponse({'status': 'success', 'action': 'unfollowed', 'follower_count': follower_count})
        else:
            # If no follow relationship was found (user wasn't following)
            follower_count = Follow.objects.filter(following=user_to_unfollow).count()
            return JsonResponse({'status': 'info', 'action': 'not_following', 'follower_count': follower_count})
    
    # If not a POST request, redirect or return an error
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)