from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=125)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=125)

    def __str__(self):
        return f'ID:{self.id} {self.name}'
