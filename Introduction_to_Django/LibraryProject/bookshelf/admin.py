from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to display
    list_filter = ('author', 'publication_year')            # Filters on the right
    search_fields = ('title', 'author')                     # Search box