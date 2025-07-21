from bookshelf.models import Book

# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Confirm deletion by checking all books
all_books = Book.objects.all()
print(f"All books count: {all_books.count()}")
print(f"Remaining books: {all_books}")
