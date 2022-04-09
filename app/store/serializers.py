from rest_framework import serializers as s

from .models import Book


class BookSerializer(s.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
