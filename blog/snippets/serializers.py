from rest_framework import serializers
from blog.models import Comment
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class CommentSerializer(serializers.ModelSerializer):
    published_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z")
    author = AuthorSerializer(many=False)

    class Meta:
        model = Comment
        fields = ['comment_text', 'published_date', 'author']
