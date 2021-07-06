from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone, dateformat
from .models import Post, Category, Tag, Comment, Test_data
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm, CommentForm, TestForm
from django.views.generic import ListView, CreateView, FormView, UpdateView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.core import serializers
from django.http import Http404, JsonResponse
import locale
from datetime import datetime


class PostFormView(FormView):
    model = Post
    template_name = 'blog/post_list.html'
    form_class = FilterForm
    success_url = reverse_lazy('post_list')

    def get(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        # context['form'] = form
        # context['posts'] = Post.objects.all()
        # if request.GET.get("tags"):
        #     context['posts'] = Post.objects.all().filter(tag=request.GET.get("tags"))
        # return self.render_to_response(context)
        self.request = request
        return super(PostFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        context['posts'] = Post.objects.all()
        if self.request.GET.get("tags"):
            context['posts'] = Post.objects.all().filter(tag=self.request.GET.get("tags"))
        return context

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form, **kwargs)

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


class PostDetailCreateView(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = 'pk'

    def get(self, request, pk):
        # self.post = Post.objects.get(pk=self.kwargs['pk'])
        self.pk = pk
        self.request = request
        return super(PostDetailCreateView, self).get(request, pk)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})

    # def form_valid(self, form, *args, **kwargs):
    #     post = get_object_or_404(Post, pk=self.kwargs['pk'])
    #     new_comment = form.save(commit=False)
    #     new_comment.post = post
    #     new_comment.author = self.request.user
    #     new_comment.published_date = timezone.now()
    #     form.save()
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        context = super(PostDetailCreateView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().filter(post=post)
        context['title'] = f'Detail of {post.title} post'
        context['form'] = CommentForm
        context['post'] = post
        return context

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if request.is_ajax:
            form = CommentForm(request.POST)
            if form.is_valid():
                # time_of_c = timezone.now()
                locale.setlocale(locale.LC_ALL, "ru")
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = self.request.user
                new_comment.published_date = timezone.now()
                instance = form.save()
                today = datetime.today().strftime("%d %B %Y г. %H:%M")
                user = self.request.user.username
                # new_comment.published_date = datetime.today().strftime("%d %B %Y г. %H:%M")
                # print('new_comment.published_date = ', dateformat.format(timezone.now(), 'Y-m-d H:i:s'))
                json_comment = serializers.serialize('json', [new_comment, ])
                ser_instance = serializers.serialize('json', [instance, ])
                # json_time_of_c = serializers.serialize('json', [time_of_c, ])
                return JsonResponse({"instance": ser_instance, 'new_c': json_comment, 'today': today, 'user': user}, status=200)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

# class Test_class(View):
#     form_class = TestForm
#     template_name = 'blog/test.html'
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         all_data = Test_data.objects.all()
#         return render(request, self.template_name, {"form": form, "all_data": all_data})
#
#     def post(self, request, *args, **kwargs):
#         all_data = Test_data.objects.all()
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#         else:
#             return render(request, self.template_name, {"form": form, "all_data": all_data})
