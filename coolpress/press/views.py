from django.shortcuts import render, get_object_or_404

# Create your views here.
from press.models import Post, PostStatus


# Home page
def index(request):
	return render(request, 'index.html')


# Default, fallback error page
def page_not_found(request, exception):
	return render(request, '404.html', status=404)


def post_detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'posts_detail.html', {'post_obj': post})


def post_list(request):
	post_list = Post.objects.filter(status=PostStatus.PUBLISHED.value).order_by('-pk')[:20]
	return render(request, 'posts_list.html', {'post_list': post_list})
