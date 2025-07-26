from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden
from .models import Book, Library, UserProfile
from .forms import BookForm  
from django.contrib import messages
from django.http import HttpResponse

# Role check functions
def check_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def check_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def check_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin View
@login_required
@user_passes_test(check_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian View
@login_required
@user_passes_test(check_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member View
@login_required
@user_passes_test(check_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# --- Function-based View: List All Books ---
def all_books_list_view(request):
    """
    A function-based view to display a comprehensive list of all books
    available in the library system, along with their authors.
    """
    all_books = Book.objects.all().select_related('author').order_by('title')

    context = {
        'books': all_books,
        'page_title': 'Our Complete Book Collection',
        'intro_message': 'Explore every title we have at a glance.'
    }

    return render(request, 'relationship_app/list_books.html', context)

def list_books(request):
    books = Book.objects.select_related('author').all().order_by('title')
    output = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    return HttpResponse(output, content_type="text/plain")

# --- Class-based View: Library Details ---
class LibraryDetailView(DetailView):
    """
    Displays details of a specific library including all books it contains.
    Accessed via primary key (pk).
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = 2025  # Example of adding extra context
        return context


# --- User Registration View ---
def register_view(request):
    """
    Handles new user registration using Django's built-in UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the new user
            return redirect('home')  # Change 'home' to the name of your home route
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})

# Add Book View
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books_list')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})

# Edit Book View
@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})

# Delete Book View
@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('books_list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

# List book view
@login_required
@permission_required('relationship_app.canaddbook', raise_exception=True)
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'list_books.html', {'books': books})