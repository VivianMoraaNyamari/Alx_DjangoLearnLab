from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test user & token
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Create sample book
        self.book = Book.objects.create(title="Sample Book", author="John Doe", published_year=2020)

        # Endpoints
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])

    def test_create_book(self):
        data = {"title": "New Book", "author": "Jane Smith", "published_year": 2021}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_list_books(self):
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book(self):
        data = {"title": "Updated Book", "author": "John Doe", "published_year": 2022}
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_partial_update_book(self):
        data = {"title": "Partially Updated"}
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Partially Updated")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url + "?author=John Doe", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(book["author"] == "John Doe" for book in response.data))

    def test_search_books(self):
        response = self.client.get(self.list_url + "?search=Sample", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Sample" in book["title"] for book in response.data))

    def test_order_books_by_year(self):
        Book.objects.create(title="Older Book", author="Jane Doe", published_year=1999)
        response = self.client.get(self.list_url + "?ordering=published_year", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["published_year"] for book in response.data]
        self.assertEqual(years, sorted(years))

    def test_authentication_required(self):
        self.client.credentials()  # remove auth
        response = self.client.get(self.list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        