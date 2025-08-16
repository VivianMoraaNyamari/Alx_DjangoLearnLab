from django.test import APITestCase
from huggingface_hub import User
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Book

class BookListViewTestCase(APITestCase):
    def setUp(self):
        """
        This logs in the user before making requests.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')  # This logs in the user
        # Set up any necessary data for the tests

        self.book = Book.objects.create(
            title='Test Book',
            author=self.user,
            publication_year=2023
        )

    def test_get_queryset_with_author_filter(self):
        # Test filtering by author name
        response = self.client.get('/api/books/', {'author': 'Some Author'})
        self.assertEqual(response.status_code, 200)
        # Add assertions to check if the response contains the expected books
        self.assertTrue(isinstance(response.data, list))

    def test_get_queryset_with_title_filter(self):
        # Test filtering by title
        response = self.client.get('/api/books/', {'title': 'Some Title'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))

        # Add assertions to check if the response contains the expected books

    def test_get_queryset_with_publication_year_filter(self):
        # Test filtering by publication year
        response = self.client.get('/api/books/', {'publication_year': '2023'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))
        # Add assertions to check if the response contains the expected books