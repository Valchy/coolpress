from django.urls import path
from django.http import JsonResponse


def hello_api(request):
	return JsonResponse({'success': True, 'msg': 'Hello to my API', 'also_try': 'api/author'})


def send_author(request):
	return JsonResponse({'author': 'Valeri Sabev'})


urlpatterns = [
	path('', hello_api, name='default_api'),
	path('author', send_author, name='send_author')
]
