import os
import requests
import json

from typing import List

from press.models import Post


def insert_post_from_mediastack(single_post):
	return Post()


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