from .models import Category
from press.gravatar import get_gravatar


def categories_processor(request):
	categories = Category.objects.all()
	return {'categories': categories}


def cooluser_processor(request):
	cooluser = None

	if hasattr(request.user, 'cooluser'):
		cooluser = request.user.cooluser

	return {'cooluser': cooluser}


def navbar_processor(request):
	gravatar_image = ''
	email = None

	if hasattr(request.user, 'cooluser'):
		email = request.user.email
		gravatar_image = get_gravatar(email)

	return {'gravatar_image': gravatar_image}