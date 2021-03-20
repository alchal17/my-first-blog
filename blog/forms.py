from django import forms
from .models import Post, Category
from django.utils import timezone


class PostForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.filter())

    class Meta:
        model = Post
        fields = ('title', 'text', 'category',)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_title',)
