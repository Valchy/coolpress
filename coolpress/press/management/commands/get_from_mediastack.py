from django.core.management import BaseCommand

from press.mediastack_manager import gather_and_create_news


# get_homework aaaahh I mean get_from_mediastack
class Command(BaseCommand):
	def handle(self, *args, **options):
		general_posts = gather_and_create_news(['general'], ['en'], ['us'], 3)
		sports_posts = gather_and_create_news(['sports'], ['en'], ['us'], 5)
		entertainment_posts = gather_and_create_news(['entertainment'], ['en'], ['us'], 2)

		self.stdout.write('\n\nHomework done 😎')
		self.stdout.write('Thank you for this awesome Django course Oskar!')
