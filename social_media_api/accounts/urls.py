from django.urls import path
from .views import FollowView, RegistrationView, LoginView, ProfileView, UnfollowView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowView.as_view(), name='unfollow_user'),

]
