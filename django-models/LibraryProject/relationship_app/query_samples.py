import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

try:
    django.setup()
except RuntimeError:
    # This handles cases where django.setup() might have already been called
    # (e.g., if you run this from a Django management command or shell)
    pass

# Import your models 
from relationship_app.models import Author, Book, Library, Librarian


def query_all_books_by_author(author_name='Stephen King'):
    """Query all books by a specific author"""
    try:
        author = Author.objects.get(name=author_name) 
        books = Book.objects.filter(author=author) 

        print(f"Books by {author.name}:")
        if books: # Check if there are any books
            for book in books:
                print(f"- {book.title}")
        else:
            print(f"No books found for '{author.name}'.")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found in the database.")
    except Exception as e:
        print(f"An unexpected error occurred in query_all_books_by_author: {e}")


def list_all_books_in_library(library_name='City Library'): 
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all() 

        print(f"Books in {library.name}:")
        if books: # Check if there are any books
            for book in books:
                print(f"- {book.title}")
        else:
            print(f"No books found in '{library.name}'.")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found in the database.")
    except Exception as e:
        print(f"An unexpected error occurred in list_all_books_in_library: {e}")


def retrieve_librarian_for_library(library_name='City Library'): # Add library_name as an argument with a default
    """Retrieve librarian for library"""
    try:
        library = Librarian.objects.get(library=library)
        librarian = library.librarian

        print(f"Librarian for {library.name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found in the database.")
    except Librarian.DoesNotExist:
        # This specific exception catches if a Library exists but no Librarian is linked via OneToOne
        print(f"No librarian assigned to the library '{library_name}'.")
    except AttributeError:
        # This might catch if 'library.librarian' somehow doesn't exist (e.g., if there's no related object)
        print(f"Could not retrieve librarian for '{library_name}' (AttributeError).")
    except Exception as e:
        print(f"An unexpected error occurred in retrieve_librarian_for_library: {e}")


if __name__ == "__main__":
    # Create data to test the queries
    print("--- Ensuring Sample Data Exists ---")
    try:
        # Create an Author if one with this name doesn't exist
        author1, created = Author.objects.get_or_create(name='Stephen King')
        if created: print(f"Created Author: {author1.name}")

        author2, created = Author.objects.get_or_create(name='J.K. Rowling')
        if created: print(f"Created Author: {author2.name}")

        # Create a Library
        library1, created = Library.objects.get_or_create(name='City Library')
        if created: print(f"Created Library: {library1.name}")

        library2, created = Library.objects.get_or_create(name='District Branch')
        if created: print(f"Created Library: {library2.name}")

        # Create some Books and link them
        book1, created = Book.objects.get_or_create(title='The Shining', author=author1)
        if created: print(f"Created Book: {book1.title}")

        book2, created = Book.objects.get_or_create(title='It', author=author1)
        if created: print(f"Created Book: {book2.title}")

        book3, created = Book.objects.get_or_create(title='Harry Potter and the Sorcerer\'s Stone', author=author2)
        if created: print(f"Created Book: {book3.title}")

        # Add books to libraries (Many-to-Many)
        library1.books.add(book1, book2)
        library1.books.add(book3) 
        library2.books.add(book3) 
        

        # Create Librarians and link them to libraries
        librarian1, created = Librarian.objects.get_or_create(name='Alice Smith', library=library1)
        if created: print(f"Created Librarian: {librarian1.name} for {library1.name}")

        librarian2, created = Librarian.objects.get_or_create(name='Bob Johnson', library=library2)
        if created: print(f"Created Librarian: {librarian2.name} for {library2.name}")

    except Exception as e:
        print(f"Error creating sample data: {e}")

    print('----------------------------------')

    print("--- Running Queries ---")
    
    query_all_books_by_author('Stephen King')
    print('-------------------------')
    query_all_books_by_author('J.K. Rowling') 
    print('-------------------------')
    query_all_books_by_author('Non Existent Author')
    print('-------------------------')

    list_all_books_in_library('City Library')
    print('-------------------------')
    list_all_books_in_library('District Branch')
    print('-------------------------')
    list_all_books_in_library('Non Existent Library') 
    print('-------------------------')

    retrieve_librarian_for_library('City Library')
    print('-------------------------')
    retrieve_librarian_for_library('District Branch')
    print('-------------------------')
    retrieve_librarian_for_library('Non Existent Library')
    print('-------------------------')