from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model
from posts.serializers import PostSerializer # Import PostSerializer to embed post data

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class NotificationSerializer(serializers.ModelSerializer):
    # Serializer fields for the GenericForeignKey
    actor = UserSerializer(read_only=True)
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'timestamp', 'read', 'target']
        read_only_fields = ['recipient', 'actor', 'verb', 'timestamp', 'target']

    # This method dynamically serializes the target object based on its type.
    def get_target(self, obj):
        if obj.target:
            if isinstance(obj.target, obj.target.__class__): # check if its a Post
                return PostSerializer(obj.target, context=self.context).data
        return None
    