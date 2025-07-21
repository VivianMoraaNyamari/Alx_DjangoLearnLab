from bookshelf.models import Book

# Retrieve and update the book's title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated book: {book}")
print(f"New title: {book.title}")