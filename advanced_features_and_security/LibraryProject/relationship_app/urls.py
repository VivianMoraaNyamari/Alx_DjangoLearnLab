from django.urls import path
from . import views # Import all views
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books

app_name = 'relationship_app' 

urlpatterns = [
    path('register/', views.register_view, name='register'),
    
    path('books/', views.all_books_list_view, name='books_list'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/registration/logged_out.html'), name='logout'),

    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),

    path('add_book/', views.add_book, name='add_book'),  # Changed from books/add/
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),  # Changed from books/<pk>/edit/
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),

]