from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BookViewSet, oauth

router = SimpleRouter()

router.register(f'book', BookViewSet)

urlpatterns = [
    path('oauth/', oauth),
]

urlpatterns += router.urls
