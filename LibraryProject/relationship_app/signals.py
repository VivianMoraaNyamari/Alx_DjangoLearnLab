from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a UserProfile only if it doesn't exist"""
    if created and not UserProfile.objects.filter(user=instance).exists():
        UserProfile.objects.create(user=instance)