from unittest import TestCase

from django.contrib.auth.models import User

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_serializer_ok(self):
        self.user1 = User.objects.create(username="test_username1")
        self.user2 = User.objects.create(username="test_username2")
        book1 = Book.objects.create(name='test book 1', price=10, author_name='Author 1', owner_id=self.user1.id)
        book2 = Book.objects.create(name='test book 2', price=20, author_name='Author 2', owner_id=self.user2.id)
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'test book 1',
                'price': '10.00',
                'author_name': 'Author 1',
                'owner': self.user1.id
            },
            {
                'id': book2.id,
                'name': 'test book 2',
                'price': '20.00',
                'author_name': 'Author 2',
                'owner': self.user2.id
            }
        ]
        self.assertEqual(expected_data, data)
