from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('category/new', views.category_new, name='category_new'),
    path('tag/new/', views.tag_new, name='tag_new'),
    path('post/<int:pk>/comment/', views.comment_post, name='comment_post'),
]
