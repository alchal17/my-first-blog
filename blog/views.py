from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

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

# def category_new2(request, pk):
#     if request.method == "POST":
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.save()
#             return redirect(f'post/{pk}/edit')
#     else:
#         form = CategoryForm()
#     return render(request, 'blog/category_new.html', {'form': form})
