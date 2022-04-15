from rest_framework import serializers as s

from .models import Book, UserBookRelation


class BookSerializer(s.ModelSerializer):
    likes_count = s.SerializerMethodField()
    annotated_likes = s.IntegerField(read_only=True)
    rating = s.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name',
                  'likes_count', 'annotated_likes', 'rating',)

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializers(s.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = '__all__'
