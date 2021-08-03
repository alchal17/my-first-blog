from django.utils import timezone
from .models import Post, Category, Tag, Comment
from django.shortcuts import get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm, CommentForm
from django.views.generic import CreateView, FormView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core import serializers
from django.http import JsonResponse
import locale
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from blog.snippets.serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


class PostFormView(FormView):
    model = Post
    template_name = 'blog/post_list.html'
    form_class = FilterForm
    success_url = reverse_lazy('post_list')

    def get(self, request, *args, **kwargs):
        self.request = request
        return super(PostFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        context['posts'] = Post.objects.all()
        if self.request.GET.get("tags"):
            context['posts'] = Post.objects.filter(tag=self.request.GET.get("tags"))
        return context

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


# class PostDetailCreateView(CreateView):
#     form_class = CommentForm
#     model = Comment
#     template_name = 'blog/post_detail.html'
#     pk_url_kwarg = 'pk'
#
#     def get(self, request, pk):
#         self.pk = pk
#         self.request = request
#         return super(PostDetailCreateView, self).get(request, pk)
#
#     def get_success_url(self):
#         return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})
#
#     def get_context_data(self, **kwargs):
#         post = Post.objects.get(pk=self.kwargs['pk'])
#         context = super(PostDetailCreateView, self).get_context_data(**kwargs)
#         context['comments'] = Comment.objects.filter(post=post).order_by('-published_date')
#         context['title'] = f'Detail of {post.title} post'
#         context['form'] = CommentForm
#         context['post'] = post
#         return context
#
#     # def post(self, request, *args, **kwargs):
#     #     post = get_object_or_404(Post, pk=self.kwargs['pk'])
#     #     if request.is_ajax:
#     #         form = CommentForm(request.POST)
#     #         if form.is_valid():
#     #             locale.setlocale(locale.LC_ALL, "ru")
#     #             new_comment = form.save(commit=False)
#     #             new_comment.post = post
#     #             new_comment.author = self.request.user
#     #             new_comment.published_date = timezone.now()
#     #             instance = form.save()
#     #             today = datetime.today().strftime("%d %B %Y г. %H:%M")
#     #             user = self.request.user.username
#     #             json_comment = serializers.serialize('json', [new_comment, ])
#     #             ser_instance = serializers.serialize('json', [instance, ])
#     #             return JsonResponse({"instance": ser_instance, 'new_c': json_comment, 'today': today, 'user': user},
#     #                                 status=200)
#     #         else:
#     #             return JsonResponse({'error': form.errors}, status=400)
#     #     return JsonResponse({"error": ""}, status=400)
#
#     def post(self, request, *args, **kwargs):
#         post = get_object_or_404(Post, pk=self.kwargs['pk'])
#         if request.is_ajax:
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 new_comment = form.save(commit=False)
#                 new_comment.post = post
#                 new_comment.author = self.request.user
#                 new_comment.published_date = timezone.now()
#                 instance = form.save()
#                 # serializer = CommentSerializer(new_comment, instance, many=True)
#                 # serializer = CommentSerializer(new_comment, many=True)
#                 serializer = CommentSerializer(new_comment, many=True)
#                 if serializer.is_valid():
#                     json = JSONRenderer.render(serializer.data)
#                     print(json)
#                     return JsonResponse(json, status=status.HTTP_200_OK)
#                 else:
#                     return JsonResponse({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
#         return JsonResponse({"error": ""}, status=status.HTTP_400_BAD_REQUEST)

class PostDetailCreateView(APIView):
    form_class = CommentForm
    model = Comment
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = 'pk'

    def get(self, request, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        queryset = Comment.objects.filter(post=post).order_by('-published_date')
        serializer = CommentSerializer(queryset, many=True)
        return JsonResponse(JSONRenderer().render(serializer.data), safe=False)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        context = super(PostDetailCreateView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=post).order_by('-published_date')
        context['title'] = f'Detail of {post.title} post'
        context['form'] = CommentForm
        context['post'] = post
        return context

    # def post(self, request, *args, **kwargs):
    #     post = get_object_or_404(Post, pk=self.kwargs['pk'])
    #     if request.is_ajax:
    #         form = CommentForm(request.POST)
    #         if form.is_valid():
    #             locale.setlocale(locale.LC_ALL, "ru")
    #             new_comment = form.save(commit=False)
    #             new_comment.post = post
    #             new_comment.author = self.request.user
    #             new_comment.published_date = timezone.now()
    #             instance = form.save()
    #             today = datetime.today().strftime("%d %B %Y г. %H:%M")
    #             user = self.request.user.username
    #             json_comment = serializers.serialize('json', [new_comment, ])
    #             ser_instance = serializers.serialize('json', [instance, ])
    #             return JsonResponse({"instance": ser_instance, 'new_c': json_comment, 'today': today, 'user': user},
    #                                 status=200)
    #         else:
    #             return JsonResponse({'error': form.errors}, status=400)
    #     return JsonResponse({"error": ""}, status=400)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if request.is_ajax:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = self.request.user
                new_comment.published_date = timezone.now()
                instance = form.save()
                # serializer = CommentSerializer(new_comment, instance, many=True)
                # serializer = CommentSerializer(new_comment, many=True)
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid():
                    json = JSONRenderer.render(serializer.data)
                    print(json)
                    return JsonResponse(json, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"error": ""}, status=status.HTTP_400_BAD_REQUEST)
