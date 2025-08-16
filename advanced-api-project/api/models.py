from django.db import models

class Author(models.Model):
    """
    Author model:
    Stores basic information about book authors.
    Each Author can have multiple related Book entries (One-to-Many).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model:
    Represents a book with its title, publication year, and a link to its author.
    The 'author' field creates a ForeignKey relationship to Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name="books",   # allows Author.books to access all books
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    