from django.test import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_serializer_ok(self):
        book1 = Book.objects.create(name='test book 1', price=10, author_name='Author 1')
        book2 = Book.objects.create(name='test book 2', price=20, author_name='Author 2')
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'test book 1',
                'price': '10.00',
                'author_name': 'Author 1',
            },
            {
                'id': book2.id,
                'name': 'test book 2',
                'price': '20.00',
                'author_name': 'Author 2',
            }
        ]
        self.assertEqual(expected_data, data)
