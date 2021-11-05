from django.core.management import BaseCommand

from press.mediastack_manager import gather_and_create_news


# get_api_news
class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('categories', nargs='+', help='List of categories to get new for')
		parser.add_argument('--countries', nargs='+', help='List of countries to get news for')
		parser.add_argument('--limit', type=int, help='Limit of posts to be added')

	def handle(self, *args, **options):
		limit = options['limit']
		categories = options['categories']
		countries = options['countries']

		single_countries = []
		single_categories = []

		if not countries:
			countries = ['us']
			single_countries = ['us']
		else:
			for cntry in countries:
				if ',' in cntry:
					single_countries.extend(cntry.split(','))
				else:
					single_countries.append(cntry)

		for cat in categories:
			if ',' in cat:
				single_categories.extend(cat.split(','))
			else:
				single_categories.append(cat)

		inserted_posts = gather_and_create_news(single_categories, ['en'], single_countries, limit)

		self.stdout.write(
			f'\n\nInserted {len(inserted_posts)} {"posts" if len(inserted_posts) != 1 else "post"} '
			f'with news about {single_categories} from {len(single_countries)} '
			f'{"countries" if len(single_countries) != 1 else "country"} ({",".join(countries)}) '
			f'with limit {limit} in english!\n'
		)
