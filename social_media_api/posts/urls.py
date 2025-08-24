from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedView, PostViewSet, CommentViewSet, LikeToggleView

# Create a router instance
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# The API URLs are automatically determined by the router
urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', LikeToggleView.as_view(), name='post-like-toggle'),
    path('posts/<int:pk>/unlike/', LikeToggleView.as_view(), name='post-unlike-toggle'),
]
