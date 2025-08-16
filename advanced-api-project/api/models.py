from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    # A string representation of the Author model
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE) # ForeignKey to Author model
    publication_year = models.IntegerField()

    # A string representation of the Book model
    def __str__(self):
        return self.title