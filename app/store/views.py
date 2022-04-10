from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name', 'price', 'author_name', ]
    ordering_fields = ['price', 'name', ]


def oauth(request):
    return render(request, 'oauth.html')
