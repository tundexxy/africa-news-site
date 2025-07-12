# news/models.py

from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User model

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Assuming 'author' links to Django's User model
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    published_date = models.DateTimeField(auto_now_add=True)
    
    # NEW FIELD ADDED HERE:
    # This field will store the URL of the article's main image.
    # blank=True means it's optional, null=True means it can be NULL in the database.
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Follow(models.Model):
    """
    Represents a follow relationship between two users.
    'follower' is the user who is following another user.
    'following' is the user who is being followed.
    """
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"