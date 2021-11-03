from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

# Create your views here.
from django.urls import reverse, resolve
from press.models import Post, PostStatus, Category, CoolUser
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView

from press.forms import PostForm, CategoryForm
from press.stats_manager import extract_stats_from_single_post, extract_stats_from_posts


# Home page
def index(request):
	url_name = resolve(request.path_info).url_name

	# Checking if coming from login or logout url
	if url_name == 'index-after-login':
		return HttpResponseRedirect('/')
	else:
		return render(request, 'index.html')


# Default, fallback error page
def page_not_found(request, exception):
	return render(request, '404.html', status=404)


# About Page with fetch functionality :)
class About(TemplateView):
	template_name = 'about.html'


def get_html_from_post(post):
	return f'''
    <html>
    <body>
    <h1>The asked post id {post.id}</h1> 
    <ul>
    <li>{post.title}</li>
    <li>{post.body}</li>
    <li>{post.category.label}</li>
    <li>{post.last_update}</li>
    </ul>
    <p>{post.author.user.username}</p>
    </body>
    </html>
    '''


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


class PostList(ListView):
	model = Post
	paginate_by = 2
	context_object_name = 'post_list'
	template_name = 'posts_list.html'

	def get_queryset(self):
		queryset = super(PostList, self).get_queryset()
		category_slug = self.kwargs['category_slug']
		category = get_object_or_404(Category, slug=category_slug)
		return queryset.filter(category=category)


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
			redirect_url = reverse('post-detail', kwargs={'post_id': instance.id})

			return HttpResponseRedirect(redirect_url)
	else:
		form = PostForm(instance=post)

	return render(request, 'posts/posts_update.html', {'form': form})


# Filter posts by search query
class PostFilteredByText(PostList):
	def get_queryset(self):
		queryset = super(PostList, self).get_queryset()
		search_text = self.request.GET.get('q')
		qs1 = Q(title__icontains=search_text)
		qs2 = Q(body__icontains=search_text)
		qs3 = Q(author__user__username__icontains=search_text)
		qs4 = Q(category__label__eq=search_text)
		return queryset.filter(qs1 | qs2 | qs3)

	def get_context_data(self, *args, **kwargs):
		context = super(PostFilteredByText, self).get_context_data(*args, **kwargs)
		context['search_data'] = self.request.GET.get('q')
		return context


def post_filtered_by_text(request):
	search_text = request.GET.get('q')
	qs1 = Q(title__icontains=search_text)
	qs2 = Q(body__icontains=search_text)
	qs3 = Q(author__user__username__icontains=search_text)
	qs4 = Q(category__label__eq=search_text)
	posts_list = Post.objects.filter(qs1 | qs2 | qs3 | qs4)
	stats = extract_stats_from_posts(post_list)
	return render(request, 'posts_list.html', {'post_list': posts_list, 'stats': stats})


# Displaying all categories and how many posts they have
def category_list(request):
	return render(request, 'categories/category_list.html')


# Displaying all posts with a certain category
def category_posts(request, category_slug):
	posts = Post.objects.filter(status=PostStatus.PUBLISHED.value, category=Category.objects.get(slug=category_slug))

	return render(request, 'categories/category_posts.html', {'category': category_slug, 'posts': posts})


def category_update(request, category_id):
	return render(request, 'categories/category_update.html')


# List of all the cool users
class CooluserList(ListView):
	model = CoolUser


# Detail view of a cool user
class CooluserDetail(DetailView):
	model = CoolUser
