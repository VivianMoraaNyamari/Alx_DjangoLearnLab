from django.db import models
from django.conf import settings # For referencing AUTH_USER_MODEL
from django.contrib.contenttypes.fields import GenericForeignKey # For generic relations
from django.contrib.contenttypes.models import ContentType # For generic relations

class Notification(models.Model):
    # Shows the user who receives the notification.
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    
    # Shows the user who performed the action that triggered the notification.
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='initiated_notifications', on_delete=models.CASCADE)
    
    # Short description of the action (e.g., "liked", "commented on", "followed").
    verb = models.CharField(max_length=255)
    
    # Generic Foreign Key setup:
    # 1. content_type: Stores the type of the target object (e.g., 'Post', 'Comment').
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # 2. object_id: Stores the primary key of the target object.
    object_id = models.PositiveIntegerField()
    # 3. target: The actual object that triggered the notification (e.g., the specific Post or Comment).
    target = GenericForeignKey('content_type', 'object_id')
    
    # Timestamp for when the notification was created.
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Indicates whether the notification has been read by the recipient.
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target} for {self.recipient.username}'