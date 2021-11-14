from django.shortcuts import redirect
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CategoryForm, TagForm, FilterForm, CommentForm


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
