from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from streamlit import status
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from .models import Post, Comment, Like
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics

class PostViewSet(viewsets.ModelViewSet):
    # Defines the set of objects the viewset can operate on
    queryset = Post.objects.all()

    # The serializer to use for converting data
    serializer_class = PostSerializer

    # IsAuthenticatedOrReadOnly: Allows any user to view, but only authenticated users to write.
    # IsOwnerOrReadOnly: Ensures that a user can only edit/delete their own posts.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # The filter backend to use for filtering the queryset
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'content']

    # The method is called when a new object is created
    # Sets the author of the post to the currently authenticated user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    # Defines the set of objects the viewset can operate on
    queryset = Comment.objects.all()

    # The serializer to use for converting data
    serializer_class = CommentSerializer

    # IsAuthenticatedOrReadOnly: Allows any user to view, but only authenticated users to write.
    # IsOwnerOrReadOnly: Ensures that a user can only edit/delete their own comments.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


    # The method is called when a new object is created
    # Sets the author of the comment to the currently authenticated user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can see their feed

    def get_queryset(self):
        # We get the list of users the current user is following.
        following_users = self.request.user.following.all()
        
        # We filter posts to include only those where the author is in the list of followed users.
        # We order them by creation date, from newest to oldest.
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        return queryset
    
class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if the user has already liked the post.
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # If a new like was created, send a notification.
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked',
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post.id
            )
            return Response(
                {'message': 'Post liked successfully.'},
                status=status.HTTP_201_CREATED
            )
        else:
            # If the like already existed, it means the user is unliking the post.
            like.delete()
            return Response(
                {'message': 'Post unliked successfully.'},
                status=status.HTTP_200_OK
            )
        