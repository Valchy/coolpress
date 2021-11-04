import os
import requests

from typing import List

from press.models import Post, User, CoolUser, Category


def insert_post_from_mediastack(single_post):
	author = single_post['author']
	email = single_post['source']
	title = single_post['title']
	body = single_post['description']
	image_link = single_post['image']
	source_link = single_post['source']

	post_category = None
	post_author = None

	# New category if post category does not exist
	# try:
	# category = single_post['category']
	# post_category = Category.objects.get(slug='health')
	# except Category.DoesNotExist:
	# 	new_category = Category.objects.create(label=post_category, slug=post_category)
	# 	new_category.save()
	# 	post_category = new_category

	# New user if post author does not exist
	# try:
	# 	user = User.objects.get(email=email)
	# 	post_author = CoolUser.objects.get(user_id=user.id)
	# except CoolUser.DoesNotExist:
	# 	u = User.objects.create(email=email, username=f'staff@{email}', first_name=author[0], last_name=author[1])
	# 	cu = CoolUser.objects.create(user=u)
	# 	u.save()
	# 	cu.save()
	# 	post_author = cu

	# Making and saving post in db
	post = Post.objects.create(title=title, body=body, category_id=2, author_id=1)
	post.save()

	return post


def gather_and_create_news(categories, languages, limit) -> List[Post]:
	response_array = []
	mediastack_api = os.environ['MEDIASTACK_API']
	url_categories = ','.join(categories)
	url_languages = ','.join(languages)

	url = f'http://api.mediastack.com/v1/news?access_key={mediastack_api}&categories={url_categories}&languages={url_languages}&limit={limit}'
	response = requests.get(url)
	data = response.json()

	for d in data['data']:
		post = insert_post_from_mediastack(d)
		if post: response_array.append(post)

	return response_array
