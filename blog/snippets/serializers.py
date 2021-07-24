from rest_framework import serializers
from blog.models import Comment


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ['comment_text', 'published_date', 'author', 'post']
