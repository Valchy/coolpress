from django.urls import path

from . import views

urlpatterns = [ # Question: why exactly do we specify a name attribute?
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post_detail, name='posts-detail'),
    path('posts/', views.post_list, name='posts-list'),
    path('categories', views.category_list, name='category-list'),
    path('category/<str:category_slug>', views.category_posts, name='category-posts'),
]

# Handling error pages
handler404 = 'press.views.page_not_found'