from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    following = models.ManyToManyField('self', related_name='followers', blank=True, symmetrical=False)

    def __str__(self):
        return self.username