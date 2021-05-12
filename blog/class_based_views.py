from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category, Tag, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm, CommentForm
from django.views.generic import ListView, CreateView


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'

    def apply_form(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['posts'] = self.Post.objects.all()
        return context


class TagCreateView(CreateView):
    model = Tag
    fields = ['tag_title']
    template_name = 'blog/tag_new.html'
