from django.urls import path

from . import views

urlpatterns = [ # Question: why exactly do we specify a name attribute?
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post_detail, name='posts-detail'),
    path('posts/', views.post_list, name='posts-list')
]

# Handling error pages
handler404 = 'press.views.page_not_found'