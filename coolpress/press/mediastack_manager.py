import os
import requests

from typing import List

from press.models import Post, User, CoolUser, Category


def insert_post_from_mediastack(single_post):
	author = single_post['author']
	category = single_post['category']
	email = single_post['source']
	title = single_post['title']
	body = single_post['description']
	image_link = single_post['image']
	source_link = single_post['source']

	# Author and username handling
	if not author:
		author = 'anonymous'
		username = 'anonymous@coolpress.com'
	else:
		if 'staff' in author.lower(): username = f'staff@{email.lower()}'
		else:
			author_names = author.lower().split(' ')

			if len(author_names) == 1:
				new_author_name = author_names[0]
			else:
				new_author_name = author_names[0][0] + author_names[-1:][0]

			username = f'{new_author_name}@coolpress.com'

	# New category if post category does not exist
	try:
		post_category = Category.objects.get(slug=category)
	except Category.DoesNotExist:
		new_category = Category.objects.create(label=category, slug=category)
		post_category = new_category

	# New user if post author does not exist
	try:
		user = User.objects.get(email=email)
		post_author = CoolUser.objects.get(user_id=user.id)
	except User.DoesNotExist:
		u = User.objects.create(email=email, username=username, first_name=author, last_name=author)
		cu = CoolUser.objects.create(user=u)
		post_author = cu

	# Making and saving post in db
	return Post.objects.create(title=title, body=body, image_link=image_link, source_link=source_link, category_id=post_category.id, author_id=post_author.id)


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
