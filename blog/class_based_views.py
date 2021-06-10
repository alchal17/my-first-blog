from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category, Tag, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm, CommentForm
from django.views.generic import ListView, CreateView, FormView, UpdateView
from django.views import View
from django.urls import reverse_lazy, reverse


class PostFormView(FormView):
    model = Post
    template_name = 'blog/post_list.html'
    form_class = FilterForm
    success_url = reverse_lazy('post_list')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        context['posts'] = Post.objects.all()
        if request.GET.get("t"):
            context['posts'] = Post.objects.all().filter(tag=request.GET.get("t"))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        filtered_category_posts = Post.objects.all()
        if form.cleaned_data.get("category"):
            filtered_category_posts = filtered_category_posts.filter(
                category=form.cleaned_data.get("category")).order_by('published_date').distinct()
        if form.cleaned_data.get("tag"):
            filtered_category_posts = filtered_category_posts.filter(tag__in=form.cleaned_data.get("tag")).order_by(
                'published_date').distinct()
        context['posts'] = filtered_category_posts
        return self.render_to_response(context)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class TagCreateView(CreateView):
    model = Tag
    template_name = 'blog/tag_new.html'
    success_url = reverse_lazy('post_list')
    fields = ['tag_title']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TagForm
        context['title'] = 'Create a new tag'
        return context


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'blog/category_new.html'
    fields = ['category_title']
    success_url = reverse_lazy('post_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryForm
        context['title'] = 'Create a new category'
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form, *args, **kwargs):
        post = form.save(commit=False)
        post.author = self.request.user
        post.published_date = timezone.now()
        post.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create a new post'
        return context


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['title'] = f'Edit the post'
        return context


class PostDetailFormView(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = 'pk'

    def get(self, request, pk):
        self.post = Post.objects.get(pk=pk)
        self.pk = pk
        self.request = request
        return super(PostDetailFormView, self).get(request, pk)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.author = self.request.user
        new_comment.published_date = timezone.now()
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostDetailFormView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().filter(post=self.post)
        context['title'] = f'Detail of {self.post.title} post'
        context['form'] = CommentForm
        context['post'] = self.post
        return context
