from django.contrib.auth.models import User
from rest_framework import serializers as s

from .models import Book, UserBookRelation


class BookReaderSerializers(s.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', )


class BookSerializer(s.ModelSerializer):
    annotated_likes = s.IntegerField(read_only=True)
    rating = s.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = s.CharField(source='owner.username', default='', read_only=True)
    readers = BookReaderSerializers(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name',
                  'annotated_likes', 'rating', 'owner_name','readers', )

    # def get_likes_count(self, instance):
    #     return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializers(s.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = '__all__'
