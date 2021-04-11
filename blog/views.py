from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category, Tag
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm


def post_list(request):
    form1 = FilterForm(request.POST)
    if request.method == "POST" and form1.is_valid():
        filtered_category_posts = Post.objects.all()
        if form1.cleaned_data.get("category"):
            filtered_category_posts = filtered_category_posts.filter(category=form1.cleaned_data.get("category"))
        if form1.cleaned_data.get("tag"):
            filtered_category_posts = filtered_category_posts.filter(tag__in=form1.cleaned_data.get("tag"))
    else:
        filtered_category_posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html', {'form1': form1, 'posts': filtered_category_posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

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
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form1 = PostForm(request.POST, instance=post)
        if form1.is_valid():
            post1 = form1.save(commit=False)
            post1.author = request.user
            post1.published_date = timezone.now()
            post1.save()
            form1.save_m2m()
            return redirect('post_list')
    else:
        form1 = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form1})

def category_new(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('post_list')
    else:
        form = CategoryForm()
    return render(request, 'blog/category_new.html', {'form': form})

def tag_new(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return redirect('post_list')
    else:
        form = TagForm()
    return render(request, 'blog/tag_new.html', {'form': form})

def sa1(request):
    return render(request, 'blog/search.html', {})
