from rest_framework import serializers
from blog.models import Comment
from django.contrib.auth.models import User, Group

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_text', 'published_date', 'author']
