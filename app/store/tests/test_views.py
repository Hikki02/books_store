import json

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username="test_username")
        self.book1 = Book.objects.create(name='test book', price=10, author_name='author_name 1',
                                         owner=self.user)
        self.book2 = Book.objects.create(name='test book 2', price=20, author_name='author_name 1')
        self.book3 = Book.objects.create(name='test book', price=10, author_name='author_name 1')

        UserBookRelation.objects.create(user=self.user, book=self.book1, like=True, rate=1, )

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')).order_by('id')
        serializers_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializers_data, response.data)
        self.assertEqual(serializers_data[0]['rating'], '1.00')
        self.assertEqual(serializers_data[0]['likes_count'], 1)

    def test_get_search(self):
        url = reverse('book-list')
        books = Book.objects.filter(id__in=[self.book3.id, self.book1.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        response = self.client.get(url, data={'search': 'author_name 1'})
        serializers_data = BookSerializer(books, many=True).data
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializers_data, response.data)

    def test_post(self):
        url = reverse('book-list')

        data = {
            "name": "test name 1",
            "price": 10,
            "author_name": "author 1",
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json', )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            "name": self.book1.name,
            "price": 290,
            "author_name": self.book1.author_name,
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json', )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(290, self.book1.price)

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username="test_username2")
        url = reverse('book-detail', args=(self.book1.id,))
        data = {
            "name": self.book1.name,
            "price": 290,
            "author_name": self.book1.author_name,
        }
        self.client.force_login(self.user2)
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json', )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(10, self.book1.price)


class BooksRelationTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username="test_username")
        self.user2 = User.objects.create(username="test_username2")
        self.book1 = Book.objects.create(name='test book', price=10, author_name='author_name 1',
                                         owner=self.user)
        self.book2 = Book.objects.create(name='test book 2', price=20, author_name='author_name 1')

    def test_like_patch(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book1)
        self.assertTrue(relation.like)

        data = {
            "is_bookmarks": True,
        }
        json_data = json.dumps(data)

        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book1)
        self.assertTrue(relation.is_bookmarks)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book1.id,))
        data = {
            "rate": 4,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book1)
        self.assertEqual(4, relation.rate)
