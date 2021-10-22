from press.models import Category


def cooluser_processor(request):
	cooluser = None

	if hasattr(request.user, 'cooluser'):
		cooluser = request.user.cooluser

	return {'cooluser': cooluser}


def categories_processor(request):
	categories = Category.objects.all()
	return {'categories': categories}
