from django.urls import path, include
from api.views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('books/', BookList.as_view(), name="book_list_view"),
    path('', include(router.urls)),
    
]
