from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from press.models import Post, PostStatus, Category, CoolUser
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
	return render(request, 'posts/posts_detail.html', {'post': post})


# Posts filtered by specific author
class PostsByAuthor(TemplateView):
	template_name = 'posts/posts_author.html'

	def get_context_data(self):
		context = super(PostsByAuthor, self).get_context_data()
		user_id = self.kwargs['author_id']

		user_name = CoolUser.objects.get(user_id=user_id)
		context['user_name'] = user_name

		posts = Post.objects.filter(author_id=user_id)
		context['post_list'] = posts

		return context


# Displaying all posts
def post_list(request):
	post_list = Post.objects.filter(status=PostStatus.PUBLISHED.value).order_by('-pk')[:20]
	return render(request, 'posts/posts_list.html', {'post_list': post_list})


# class PostList(ListView):
#     model = Post
#     paginate_by = 2
#     context_object_name = 'post_list'
#     template_name = 'posts_list.html'
#
#     def get_queryset(self):
#         queryset = super(PostList, self).get_queryset()
#         category_slug = self.kwargs['category_slug']
#         category = get_object_or_404(Category, slug=category_slug)
#         return  queryset.filter(category=category)


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

	return render(request, 'posts/posts_update.html', {'form': form})


# Displaying all categories and how many posts they have
def category_list(request):
	return render(request, 'categories/category_list.html')


# Displaying all posts with a certain category
def category_posts(request, category_slug):
	posts = Post.objects.filter(status=PostStatus.PUBLISHED.value, category=Category.objects.get(slug=category_slug))

	return render(request, 'categories/category_posts.html', {'category': category_slug, 'posts': posts})


def category_update(request, category_id):
	return render(request, 'categories/category_update.html')