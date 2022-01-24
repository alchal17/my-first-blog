from django.utils import timezone
from .models import Post, Category, Tag, Comment, Rating
from django.shortcuts import get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm, CommentForm
from django.views.generic import CreateView, FormView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from rest_framework.response import Response
from blog.snippets.serializers import CommentSerializer, TagSerializer
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import generics
from django.shortcuts import render
from django.db.models import Avg, Func


class Round(Func):
    function = 'ROUND'


class PostFormView(FormView):
    model = Post
    template_name = 'blog/post_list.html'
    form_class = FilterForm
    success_url = reverse_lazy('post_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.annotate(avg_rating=Round(Avg('rating__value'), 2)).order_by('published_date')
        context['posts'] = posts
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
        context['title'] = f'Edit {Post.objects.get(pk=self.pk).title} post'
        return context

    def get(self, request, *args, **kwargs):
        self.pk = self.kwargs['pk']
        return super(PostUpdateView, self).get(request, *args, **kwargs)


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    renderer_classes = [TemplateHTMLRenderer]
    model = Tag
    queryset = Tag.objects.all()

    def post(self, request, *args, **kwargs):
        form = TagForm(request.POST)
        if request.is_ajax:
            if form.is_valid():
                new_tag = form.save(commit=False)
                form.save()
                serializer = TagSerializer(new_tag)
                json_tag = JSONRenderer().render(serializer.data).decode('utf8')
                return JsonResponse({'new_tag': json_tag}, status=200, safe=False)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)

    def list(self, request, *args, **kwargs):
        response = super(TagList, self).list(request, *args, **kwargs)
        response.tags = Tag.objects.all()
        response.form = TagForm
        response.title = 'Create a new tag'
        return Response({'tags': response.tags, 'form': response.form, 'title': response.title},
                        template_name='blog/tag_new.html')


class Comment_Rating_List(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comments = Comment.objects.filter(post=post).order_by('-published_date')
        return comments

    def list(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post_ratings = Rating.objects.filter(post=post)
        if not Rating.objects.filter(author=self.request.user, post=post).exists():
            if not Rating.objects.filter(post=post).exists():
                rating_dict = {'rating': 0}
            else:
                average_rating = round(post_ratings.aggregate(Avg('value'))['value__avg'], 2)
                rating_dict = {'rating': average_rating}
        else:
            rating = Rating.objects.get(author=self.request.user, post=post).value
            rating_dict = {'rating': rating}
        ser_comments = CommentSerializer(self.get_queryset(), many=True)
        new_ser_comments_rating = ser_comments.data
        new_ser_comments_rating.append(rating_dict)
        return Response(new_ser_comments_rating)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        number = request.POST.get('number', None)
        if number:
            rating, created = Rating.objects.update_or_create(author=self.request.user, post=post,
                                                              defaults={'value': number})
            rating.save()
        if request.is_ajax:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = self.request.user
                new_comment.published_date = timezone.now()
                form.save()
                serializer = CommentSerializer(new_comment)
                json_comment = JSONRenderer().render(serializer.data).decode('utf8')
                return JsonResponse({'new_comment': json_comment}, status=200, safe=False)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        return JsonResponse({"error": ""}, status=400)


def homepage(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    title = f'Detail of {post.title} post'
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'title': title})
