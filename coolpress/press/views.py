from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from press.models import Post


def index(request):
    return HttpResponse('Hello there :)')

def post_detail(request, post_id):
    post_object = Post.objects.get(pk=post_id)
    return HttpResponse(post_object)