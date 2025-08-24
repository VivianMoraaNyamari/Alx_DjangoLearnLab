from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from posts import permissions
from .serializers import RegistrationSerializer, CustomUserSerializer
from .models import CustomUser


class RegistrationView(generics.GenericAPIView):
    # Automatically handles user creation
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [] # No permission needed for registration

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Get the created user and create a token for them
        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        
        headers = self.get_success_headers(serializer.data)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)
    
class LoginView(APIView):
    permission_classes = [] # No permission needed for login

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user against the database
        user = authenticate(username=username, password=password)

        if user:
            # Get or create a token and return it if a user is authenticated successfully
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        else:
            # If authentication fails, return an error
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(APIView):
    # This view requires a token for authentication
    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user

        if target_user == current_user:
            return Response(
                {'error': 'You cannot follow yourself.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # We only handle the 'add' action in this view.
        if not current_user.following.filter(id=target_user.id).exists():
            current_user.following.add(target_user)
            return Response(
                {'message': f'You are now following {target_user.username}.'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': f'You are already following {target_user.username}.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class UnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user

        if target_user == current_user:
            return Response(
                {'error': 'You cannot unfollow yourself.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # We only handle the 'remove' action in this view.
        if current_user.following.filter(id=target_user.id).exists():
            current_user.following.remove(target_user)
            return Response(
                {'message': f'You have unfollowed {target_user.username}.'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': f'You are not following {target_user.username}.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        