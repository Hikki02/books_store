from rest_framework import serializers as s

from .models import Book, UserBookRelation


class BookSerializer(s.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class UserBookRelationSerializers(s.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = '__all__'
