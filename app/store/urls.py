from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BookViewSet, oauth, UserBookRelationApiView

router = SimpleRouter()

router.register(f'book', BookViewSet)
router.register(f'book-relations', UserBookRelationApiView)

urlpatterns = [
    path('oauth/', oauth),
]

urlpatterns += router.urls
