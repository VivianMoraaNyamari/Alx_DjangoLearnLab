from bookshelf.models import Book

# Retrieve the book we just created
book = Book.objects.get(title="1984")

print(f"Retrieved book: {book}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
print(f"ID: {book.id}")
