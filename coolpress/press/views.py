from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from press.models import Post, PostStatus
from django.views.generic import TemplateView

from press.forms import PostForm


# Home page
def index(request):
	return render(request, 'index.html')


# Default, fallback error page
def page_not_found(request, exception):
	return render(request, '404.html', status=404)


# About Page with fetch functionality :)
class About(TemplateView):
	template_name = 'about.html'


# Specific post details page
def post_detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'posts_detail.html', {'post': post})


# Displaying all posts
def post_list(request):
	post_list = Post.objects.filter(status=PostStatus.PUBLISHED.value).order_by('-pk')[:20]
	return render(request, 'posts_list.html', {'post_list': post_list})


@login_required
def post_update(request, post_id=None):
	post = None

	if post_id:
		post = get_object_or_404(Post, pk=post_id)

		if request.user != post.author.user:
			return HttpResponseBadRequest('Not Allowed to change others posts')

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user.cooluser
			instance.save()
			redirect_url = reverse('posts-detail', kwargs={'post_id': instance.id})

			return HttpResponseRedirect(redirect_url)
	else:
		form = PostForm(instance=post)

	return render(request, 'posts_update.html', {'form': form})


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
