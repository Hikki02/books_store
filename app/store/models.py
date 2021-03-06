from django.contrib.auth.models import User
from django.db import models


RATE_CHOICE = (
    (1, 'ok'),
    (2, 'fine'),
    (3, 'good'),
    (4, 'amazing'),
    (5, 'incredible'),
)


class Book(models.Model):
    name = models.CharField(max_length=125)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=125)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owner_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True, blank=True)

    def __str__(self):
        return f'ID:{self.id} {self.name}'


class UserBookRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    is_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICE, null=True)

    def __str__(self):
        return f'{self.user.username} {self.book.name} RATE:{self.rate}'

    def save(self, *args, **kwargs):
        from store.utils import set_rating
        creating = self.pk
        old_rate = self.rate
        super().save(*args, **kwargs)
        new_rate = self.rate
        if old_rate != new_rate or creating:
            set_rating(self.book)
