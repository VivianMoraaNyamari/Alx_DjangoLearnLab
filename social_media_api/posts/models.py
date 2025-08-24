from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(CustomUser, related_name='posts', on_delete=models.CASCADE)  
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta: # Orders from newest to oldest
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] 

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    

class Like(models.Model):
    # Foreign Key to the Post model, indicating which post was liked.
    # If the post is deleted, its likes are deleted.
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    
    # Foreign Key to the User model, indicating who liked the post.
    # If the user is deleted, their likes are deleted.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    
    # Timestamp for when the like was created.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures that a user can only like a specific post once.
        unique_together = ('post', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'