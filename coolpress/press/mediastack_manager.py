import os
import requests

from typing import List

from press.models import Post, User, CoolUser, Category, PostStatus


def insert_post_from_mediastack(single_post):
	author = single_post['author']
	category = single_post['category']
	email = single_post['source']
	title = single_post['title']
	body = single_post['description']
	image_link = single_post['image']
	source_link = single_post['source']

	# Source link check
	if not source_link:
		source_link = 'MediaStack News'
		email = 'mediastakcnews.com'

	# Author and username handling
	if not author:
		author = 'anonymous'
		username = 'anonymous@coolpress.com'
	else:
		if 'staff' in author.lower():
			username = f'staff@{email.lower()}'
		else:
			author_names = author.lower().split(' ')

			if len(author_names) == 1:
				new_author_name = author_names[0]
			else:
				new_author_name = author_names[0][0] + author_names[-1]

			username = f'{new_author_name}@coolpress.com'

	# New category if post category does not exist
	try:
		post_category = Category.objects.get(slug=category)
	except Category.DoesNotExist:
		new_category = Category.objects.create(label=f'{category} News', slug=category)
		post_category = new_category

	# New user if post author does not exist
	try:
		user = User.objects.get(email=email)
		post_author = CoolUser.objects.get(user_id=user.id)
	except User.DoesNotExist:
		try:
			# Fix username collision bug
			user = User.objects.get(username=username)
			post_author = CoolUser.objects.get(user_id=user.id)
		except User.DoesNotExist:
			u = User.objects.create(email=email, username=username, first_name=author, last_name=author)
			cu = CoolUser.objects.create(user=u)
			post_author = cu

	# Check if exact same post with body and title exists
	try:
		Post.objects.get(title=title, body=body, image_link=image_link, source_link=source_link, category_id=post_category.id, author_id=post_author.id)
		return None
	except Post.DoesNotExist:
		return Post.objects.create(title=title, body=body, image_link=image_link, source_link=source_link, category_id=post_category.id, author_id=post_author.id, status=PostStatus.PUBLISHED.value)


def gather_and_create_news(categories, languages, countries, limit) -> List[Post]:
	response_array = []
	mediastack_api = os.environ['MEDIASTACK_API']
	url_categories = ','.join(categories)
	url_languages = ','.join(languages)
	url_countries = ','.join(countries)

	url = f'http://api.mediastack.com/v1/news?access_key={mediastack_api}&categories={url_categories}&languages={url_languages}&countries={url_countries}&limit={limit}'
	response = requests.get(url)
	data = response.json()

	for d in data['data']:
		post = insert_post_from_mediastack(d)

		if post:
			response_array.append(post)

	return response_array
