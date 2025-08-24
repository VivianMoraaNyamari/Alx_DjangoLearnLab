from rest_framework import serializers
from .models import Like, Post, Comment
from django.contrib.auth import get_user_model


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = 'id', 'username', 'email'


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  # Displays author's information instead of just the ID

    class Meta:
        model = Post
        fields = 'author', 'title', 'content', 'created_at', 'updated_at'
        read_only_fields = ('author', 'created_at', 'updated_at')
        

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = 'id', 'post', 'author', 'content', 'created_at', 'updated_at'
        read_only_fields = ('author', 'created_at', 'updated_at')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']