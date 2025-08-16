from rest_framework import serializers
from .models import Author, Book
from datetime import datetime # Import datetime to validate the published year

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    """
    books = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model, including validation for the published year.
    This serializer incudes a nested AuthorSerializer to represent the author of the book.
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    # Validate the published year to ensure it is not in the future
        def validate_published_year(self, value):
            current_year = datetime.now().year
            if value > current_year:
                raise serializers.ValidationError("Published year cannot be in the future.")
            