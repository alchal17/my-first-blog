from django.urls import path
from . import views
from . import class_based_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # path('', class_based_views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', class_based_views.PostDetailFormView.as_view(), name='post_detail'),
    # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # path('post/new/', views.post_new, name='post_new'),
    path('post/new/', class_based_views.PostCreateView.as_view(), name='post_new'),
    # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/edit/', class_based_views.PostUpdateView.as_view(), name='post_edit'),
    # path('category/new', views.category_new, name='category_new'),
    path('category/new', class_based_views.CategoryCreateView.as_view(), name='category_new'),
    # path('tag/new/', views.tag_new, name='tag_new'),
    path('tag/new/', class_based_views.TagCreateView.as_view(), name='tag_new'),
]
