from django.urls import path

from . import views

urlpatterns = [
    # Home and About Page view
    path('', views.index, name='index'),
    path('accounts/profile/', views.index, name='index-after-login'),
    path('about/', views.About.as_view(), name='about-page'),
    path('search', views.search, name='search'),

    # Post views
    path('posts/', views.PostsList.as_view(), name='posts-list'), # All posts
    path('posts/<str:username>/', views.PostsByAuthor.as_view(), name='post-author'), # Posts by author
    path('post/<int:post_id>/', views.post_detail, name='post-detail'), # Specific post by id
    path('post/add/', views.post_update, name='post-add'), # Add a post
    path('post/update/<int:post_id>/', views.post_update, name='post-update'), # Update a post
    path('post-filtered/', views.PostFilteredByText.as_view(), name='post-filtered'), # Posts filtered by search query

    # Category views
    path('categories/', views.category_list, name='category-list'), # All categories
    path('category/<str:category_slug>/', views.category_posts, name='category-posts'), # Specific category
    path('category/add/', views.CategoryAdd.as_view(), name='category-add'), # Add a category
    path('category/update/<int:category_id>/', views.CategoryUpdate.as_view(), name='category-update'), # Update category

    # User views
    path('users/', views.CooluserList.as_view(), name='cooluser-list'), # All users
    path('user/<int:pk>', views.CooluserDetail.as_view(), name='cooluser-detail'), # Specific user
]

# Handling error pages (might cause images file load error in production)
handler404 = 'press.views.page_not_found'