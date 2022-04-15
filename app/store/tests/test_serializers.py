from unittest import TestCase

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_serializer_ok(self):
        self.user1 = User.objects.create(username="test_username1")
        self.user2 = User.objects.create(username="test_username2")
        self.user3 = User.objects.create(username='test_username3')

        book1 = Book.objects.create(name='test book 1', price=10, author_name='Author 1')
        book2 = Book.objects.create(name='test book 2', price=20, author_name='Author 2')

        UserBookRelation.objects.create(user=self.user1, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=book1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user3, book=book1, like=True, rate=1)

        UserBookRelation.objects.create(user=self.user1, book=book2, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=book2, like=True, rate=1)
        UserBookRelation.objects.create(user=self.user3, book=book2, like=False)

        books = Book.objects.annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')).order_by('id')

        data = BookSerializer(books, many=True).data

        expected_data = [
            {
                'id': book1.id,
                'name': 'test book 1',
                'price': '10.00',
                'author_name': 'Author 1',
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': '3.67'

            },
            {
                'id': book2.id,
                'name': 'test book 2',
                'price': '20.00',
                'author_name': 'Author 2',
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.00'
            }
        ]
        print(data)
        self.assertEqual(expected_data, data)
