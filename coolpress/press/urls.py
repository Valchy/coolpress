from django.urls import path

from . import views

urlpatterns = [
    # Home and About Page view
    path('', views.index, name='index'),
    path('about/', views.About.as_view(), name='about-page'),

    # Post views
    path('posts/', views.post_list, name='posts-list'), # All posts
    path('posts/<str:post_author>/', views.PostsByAuthor.as_view(), name='post-author'), # Posts by author
    path('post/<int:post_id>/', views.post_detail, name='post-detail'), # Specific post by id
    path('post/add/', views.post_update, name='post-add'), # Add a post
    path('post/update/<int:post_id>/', views.post_update, name='post-update'), # Update a post

    # Category views
    path('categories/', views.category_list, name='category-list'), # All categories
    path('category/<str:category_slug>/', views.category_posts, name='category-posts') # Specific category
]

# Handling error pages (might cause images file load error in production)
handler404 = 'press.views.page_not_found'