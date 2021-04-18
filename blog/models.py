from django.conf import settings
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text


class Category(models.Model):
    category_title = models.CharField(max_length=100)

    def __str__(self):
        return self.category_title


class Tag(models.Model):
    tag_title = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_title

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag)
    comment = models.ManyToManyField(Comment)

    def __str__(self):
        return self.title
