from django.shortcuts import render, get_object_or_404

# Create your views here.
from press.models import Post, PostStatus, Category


# Home page
def index(request):
	return render(request, 'index.html')


# Default, fallback error page
def page_not_found(request, exception):
	return render(request, '404.html', status=404)


# Specific post details page
def post_detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'posts_detail.html', {'post': post})


# Displaying all posts
def post_list(request):
	post_list = Post.objects.filter(status=PostStatus.PUBLISHED.value).order_by('-pk')[:20]
	return render(request, 'posts_list.html', {'post_list': post_list})


# Displaying all categories and how many posts they have
def category_list(request):
	categories = []

	for category in Category.objects.all():
		categories.append({
			'slug': category.slug,
			'label': category.label,
			'available_posts': str(Post.objects.filter(category=category.id).count())
		})

	return render(request, 'category_list.html', {'categories': categories})


# Displaying all posts with a certain category
def category_posts(request, category_slug):
	posts = Post.objects.filter(status=PostStatus.PUBLISHED.value, category=Category.objects.get(slug=category_slug))

	return render(request, 'category_posts.html', {'category': category_slug, 'posts': posts})