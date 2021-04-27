from django import forms
from .models import Post, Category, Tag, Comment
from django.utils import timezone


class PostForm(forms.ModelForm):

    title = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'size': '35', 'placeholder': 'Write your title here'}), label=False)
    # text = forms.CharField(widget=forms.Textarea(attrs={'size': '230', 'placeholder': 'Write your post here'}), label=False)
    text = forms.CharField(label=False)
    text.widget = forms.Textarea(attrs={'size': '120', 'placeholder': 'Write your post here'})
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'tag',)


class CategoryForm(forms.ModelForm):

    category_title = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'size': '50', 'placeholder': 'Create your category here'}))

    class Meta:
        model = Category
        fields = ('category_title',)


class TagForm(forms.ModelForm):

    tag_title = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'size': '50', 'placeholder': 'Create your tag here'}))

    class Meta:
        model = Tag
        fields = ('tag_title',)


class FilterForm(forms.Form):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Category filter", required=False)
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple,
                                         label="Tag filter", required=False)


class CommentForm(forms.Form):

    # comment = forms.CharField(widget=forms.Textarea, label=False)
     comment = forms.CharField(widget=forms.TextInput(attrs={'size': '100', 'placeholder': ' Write your comment here'}), label=False)
