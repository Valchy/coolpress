from django.shortcuts import get_object_or_404
from django.urls import path
from django.http import JsonResponse

from . import views
from press.models import Category


def hello_api(request):
	return JsonResponse({'success': True, 'msg': 'Hello to my API', 'also_try': 'api/author', 'and_try': 'api/category-json/<str:slug>'})


def send_author(request):
	return JsonResponse({'author': 'Valeri Sabev'})


def category_api(request, slug):
	cat = get_object_or_404(Category, slug=slug)
	return JsonResponse(
		dict(slug=cat.slug, label=cat.label)
	)


urlpatterns = [
	path('', hello_api, name='default_api'),
	path('author', send_author, name='send_author'),
	path('category-json/<str:slug>', category_api, name='category-json')
]
