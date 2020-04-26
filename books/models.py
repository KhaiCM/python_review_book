from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class BookBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BookBase):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Book(BookBase):
    name = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=100)
    number_of_pages = models.IntegerField(default=0)
    image = models.FileField(upload_to='static/book/images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Review(BookBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.TextField()


class Comment(BookBase):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')


class Mark(BookBase):
    STATUS_CHOICES = (
        (0, 'Unread'),
        (1, 'Reading'),
        (2, 'Read'),
    )
    STATUS_FAVORITE = (
        (0, 'Normal'),
        (1, 'Favorite')
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_reading = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    favorite = models.IntegerField(choices=STATUS_FAVORITE, default=0)

    def __str(self):
        return self.page_reading
