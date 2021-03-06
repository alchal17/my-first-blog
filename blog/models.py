from django.conf import settings
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse


class Test_data(models.Model):
    data_title = models.CharField(max_length=100)

    def __str__(self):
        return self.data_title


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

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name='author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text
