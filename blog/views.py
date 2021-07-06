import random

from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category, Tag, Comment, Test_data
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm, CommentForm, TestForm
from django.http import Http404, JsonResponse
from django.core import serializers


def post_list(request):
    form = FilterForm(request.POST)
    if request.method == "POST" and form.is_valid():
        filtered_category_posts = Post.objects.all()
        if form.cleaned_data.get("category"):
            filtered_category_posts = filtered_category_posts.filter(
                category=form.cleaned_data.get("category")).order_by('published_date').distinct()
        if form.cleaned_data.get("tag"):
            filtered_category_posts = filtered_category_posts.filter(tag__in=form.cleaned_data.get("tag")).order_by(
                'published_date').distinct()
        return render(request, 'blog/post_list.html',
                      {'form': form, 'posts': filtered_category_posts, 'title': 'Main page'})
    if request.GET.get("t"):
        filtered_category_posts = Post.objects.all().filter(tag=request.GET.get("t"))
    else:
        filtered_category_posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html',
                  {'form': form, 'posts': filtered_category_posts, 'title': 'Main page'})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    title = f'Detail of {post.title} post'
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment.objects.create(comment_text=form.cleaned_data.get('comment'), author=request.user,
                                                 published_date=timezone.now())
            new_comment.save()
            post.comment.add(new_comment)
            post.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'title': title})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'title': 'Creating a new post'})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    title = f'Edit post "{post.title}"'
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'title': title})


def category_new(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = CategoryForm()
    return render(request, 'blog/category_new.html', {'form': form, 'title': 'Create a new category'})


def tag_new(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = TagForm()
    return render(request, 'blog/tag_new.html', {'form': form, 'title': 'Create a new tag'})


# def tag_new(request):

def add_ajax(request):
    if request.is_ajax():
        response = {'first-text': 'Lorem Ipsum is simply dummy text',
                    'second-text': 'to make a type specimen book. It has '}
        return JsonResponse(response)
    else:
        raise Http404


# def test(request):
#     text =
# return render(request, 'blog/test.html')
def test(request):
    all_data = Test_data.objects.all()
    # if request.is_ajax():
    #     response = {'first-text': str(random.randint(1, 10)) + " ", 'second-text': str(random.randint(11, 20)) + " "}
    #     return JsonResponse(response)
    # else:
    #     return render(request, 'blog/test.html')
    # if request.method == "POST":
    #     form = TestForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('post_list')
    if request.method == 'GET':
        form = TestForm()
        return render(request, 'blog/test.html', {'form': form, 'all_data': all_data})
    if request.is_ajax and request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)
