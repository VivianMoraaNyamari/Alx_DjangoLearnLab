from rest_framework import generics
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.core.exceptions import PermissionDenied
from django_filters import rest_framework as filters
from rest_framework import filters

class BookListView(generics.ListAPIView):
    """
    View to retrieve all books.
    This view uses the BookSerializer to serialize the book data.
    """

    # This view allows for searching and filtering of books by author name, title, and publication year.
    # It also supports ordering by title, author's name, and publication year.
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter] 
    ordering_fields = ['title', 'author__name', 'publication_year']

    def get_queryset(self):
        """
        Optionally filter the books by author name, title and publication year if provided in the query parameters.
        """
        queryset = super().get_queryset()
        author_name = self.request.query_params.get('author', None)
        title = self.request.query_params.get('title', None)
        publication_year = self.request.query_params.get('publication_year', None)

        if author_name:
            queryset = queryset.filter(author__name__icontains=author_name)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if publication_year:
            queryset = queryset.filter(publication_date__year=publication_year)
        return queryset

class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    """
    View to create a new model instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return super().perform_create(serializer)(self, serializer)
    
    # Only authenticated users can create a book
        if not self.request.user.has_perm('api.add_book'):
            raise PermissionDenied("You do not have permission to create a book.")

        serializer.save(author=self.request.user)  

class BookUpdateView(generics.UpdateAPIView):
    """
    View to update an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Example: Only allow users with a specific permission
        if not self.request.user.has_perm('api.change_book'):
            raise PermissionDenied("You do not have permission to update this book.")
        serializer.save()

    def get_queryset(self):
        # Example: Only allow users to update books they created
        return Book.objects.filter(created_by=self.request.user)

class BookDeleteView(generics.DestroyAPIView):
    """
    View to remove a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can delete a book