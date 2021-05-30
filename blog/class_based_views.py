from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category, Tag, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm, CommentForm
from django.views.generic import ListView, CreateView, FormView, UpdateView
from django.views import View
from django.urls import reverse_lazy, reverse


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list'

    def get_request(self, request, *args, **kwargs):
        self.request = request
        return super(PostListView, self).get(request, *args, **kwargs)

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        form = FilterForm(self.request.POST)
        if self.request.method == "GET" and form.is_valid():
            filtered_category_posts = Post.objects.all()
            if form.cleaned_data.get("category"):
                filtered_category_posts = filtered_category_posts.filter(
                    category=form.cleaned_data.get("category")).order_by("published_date").distinct()
            if form.cleaned_data.get("tag"):
                filtered_category_posts = filtered_category_posts.filter(tag__in=form.cleaned_data.get("tag")).order_by(
                    "publisher_date").distinct()
            context['form'] = form
            context['posts'] = filtered_category_posts
            context['title'] = 'Main page'
            return context


class TagCreateView(CreateView):
    model = Tag
    template_name = 'blog/tag_new.html'
    fields = ['tag_title']
    success_url = reverse_lazy('post_list')

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


class PostDetailFormView(FormView):
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def get(self, request, pk):
        self.post = Post.objects.get(pk=pk)
        self.pk = pk
        return super(PostDetailFormView, self).get(request, pk)

    def get_success_url(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = 'demo'
        return reverse('post_detail', kwargs={"pk": pk})

    def form_valid(self, form, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        new_comment = Comment.objects.create(comment_text=form.cleaned_data.get('comment'), author=self.request.user,
                                             published_date=timezone.now())
        new_comment.save()
        post.comment.add(new_comment)
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostDetailFormView, self).get_context_data(**kwargs)
        context['title'] = f'Detail of {self.post.title} post'
        context['form'] = CommentForm
        context['post'] = self.post
        return context
