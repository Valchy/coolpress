from django.core.management import BaseCommand

from press.mediastack_manager import gather_and_create_news


class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('categories', nargs='+', help='What news categories to pull information from')
		parser.add_argument('--limit', type=int, help='Limit of posts to be added')

	def handle(self, *args, **options):
		limit = options['limit']
		categories = options['categories']
		single_categories = []

		for cat in categories:
			if ',' in cat:
				single_categories.extend(cat.split(','))
			else:
				single_categories.append(cat)

		inserted_posts = gather_and_create_news(categories, ['en'], limit)

		self.stdout.write(f'Inserted {len(inserted_posts)} posts of news about {single_categories} with limit {limit}')