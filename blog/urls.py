from django.urls import path
from . import class_based_views

urlpatterns = [
    path('', class_based_views.PostFormView.as_view(), name='post_list'),
    path('post/<int:pk>/detail', class_based_views.homepage, name='detail_of_post'),
    path('post/<int:pk>/', class_based_views.CommentList.as_view(), name='post_detail'),
    path('post/new/', class_based_views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', class_based_views.PostUpdateView.as_view(), name='post_edit'),
    path('category/new', class_based_views.CategoryCreateView.as_view(), name='category_new'),
    path('tag/new/', class_based_views.TagList.as_view(), name='tag_new'),
]
