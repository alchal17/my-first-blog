from rest_framework import serializers
from blog.models import Comment, Tag
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class CommentSerializer(serializers.ModelSerializer):
    published_date = serializers.DateTimeField(format="%d %B, %I:%M %p, %Y")
    author = AuthorSerializer(many=False)

    class Meta:
        model = Comment
        fields = ['comment_text', 'published_date', 'author']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_title', ]
