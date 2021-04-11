from django import forms
from .models import Post, Category, Tag
from django.utils import timezone


class PostForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all())
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'tag',)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('category_title',)


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('tag_title',)


class FilterForm(forms.Form):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Category filter", required=False)
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple,
                                         label="Tag filter", required=False)
