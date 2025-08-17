from django.contrib import admin
from .models import Post, Comment

# Ensures that posts and comments can be managed through the admin interface
admin.site.register(Post)
admin.site.register(Comment)
