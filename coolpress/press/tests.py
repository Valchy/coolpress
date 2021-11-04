import json
import os

from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from press.mediastack_manager import insert_post_from_mediastack, gather_and_create_news
from press.models import Category, CoolUser, Post
from press.stats_manager import StatsDict, extract_stats_from_single_post, extract_stats_from_posts
from press.user_management import get_gravatar_link, extract_github_repositories

from press.__test_data__.sample_posts_data import TITLES, BODIES


class CategoryModelTest(TestCase):
	def test_categories_count_same_as_context(self):
		categories = Category.objects.all()
		response = self.client.get(reverse('category-list'))
		context_categories = response.context['categories']
		self.assertCountEqual(categories, context_categories)


class PostModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.u = User.objects.create(first_name='juanito')
		cls.cu = CoolUser.objects.create(user=cls.u)
		cls.cat = Category.objects.create(slug='random', label='Some random news')
		cls.p = Post.objects.create(category=cls.cat, author=cls.cu)

	def test_reaching_unknown_post(self):
		response = self.client.get(reverse('post-detail', kwargs={'post_id': 9999999}))
		self.assertEqual(response.status_code, 404)

	def test_user_create(self):
		u = User.objects.create(first_name='juantigo')
		cu = CoolUser.objects.create(user=u)
		self.assertEqual(cu.id, 1)

	def test_sample_post(self):
		self.assertEqual(self.cu.pk, 1)

		cnt_of_post = Post.objects.count()
		self.assertEqual(cnt_of_post, 1)

	def test_post_detail(self):
		client = Client()
		url = reverse('post-detail', kwargs={'post_id': self.p.pk})
		response = client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['post_obj'], self.p)
		url = '/post/pepe'
		response = client.get(url)
		self.assertEqual(response.status_code, 404)
		url = reverse('post-detail', kwargs={'post_id': 10})
		response = client.get(url)
		self.assertEqual(response.status_code, 404)


class CreatePostUsingForm(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.juan = User.objects.create(first_name='juanito', is_active=True, username='juanito')
		cls.cu = CoolUser.objects.create(user=cls.juan)
		cls.cat = Category.objects.create(slug='random', label='Some random news')
		cls.juan_post = Post.objects.create(category=cls.cat, author=cls.cu)

		cls.juan_pass = 'Holamundo'
		cls.juan.set_password('Holamundo')
		cls.juan.save()

		cls.maria = User.objects.create(first_name='maria', is_active=True, username='maria')
		cls.cu = CoolUser.objects.create(user=cls.maria)

		cls.maria_pass = 'HolamundoMaria'
		cls.maria.set_password(cls.maria_pass)
		cls.maria.save()

	def setUp(self):
		self.client = Client()

	def test_check_others_updating_permissions(self):
		update_juans_post = reverse('post-update', kwargs=dict(post_id=self.juan_post.id))
		is_logged_in = self.client.login(username=self.juan.username, password=self.juan_pass)
		self.assertTrue(is_logged_in)

		response = self.client.get(update_juans_post)
		self.assertEqual(response.status_code, 200)

		is_logged_in = self.client.login(username=self.maria.username, password=self.maria_pass)
		self.assertTrue(is_logged_in)
		response = self.client.get(update_juans_post)
		self.assertEqual(response.status_code, 400)


class UserManagementTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.proper_email = 'valchygaming@gmail.com'
		cls.wrong_email = 'valchyAlotofRandomThings@gmailRandomGoogleWhyNot.com'
		cls.default_gravatar = 'https://www.gravatar.com/avatar/2988933bbe1b0a831e6a0564560ea099'

	def test_positive_creation_of(self):
		random_user = User.objects.create(username='randomUser', email=self.proper_email)
		user = CoolUser.objects.create(user=random_user)
		self.assertIsNotNone(user.gravatar_link)

	def test_negative_creation_of_gravatar_links(self):
		random_user = User.objects.create(username='randomUser', email=self.wrong_email)
		user = CoolUser.objects.create(user=random_user)
		self.assertEqual(user.gravatar_link, self.default_gravatar)

	def test_update_email(self):
		random_user = User.objects.create(username='randomUser', email=self.wrong_email)
		cool_user = CoolUser.objects.create(user=random_user)
		self.assertEqual(cool_user.gravatar_link, self.default_gravatar)

		cool_user.user.email = self.proper_email
		cool_user.save()
		self.assertIsNotNone(cool_user.gravatar_link)

	def test_get_gravatar_positive(self):
		gravatar_link = get_gravatar_link(self.proper_email)
		self.assertIsNotNone(gravatar_link)
		self.assertTrue(gravatar_link, 'https://www.gravatar.com/avatar/139f76ac09f8b9d3a2392b45b7ad5f4c')

	def test_get_gravatar_negative(self):
		gravatar_link = get_gravatar_link(self.wrong_email)
		self.assertEqual(gravatar_link, self.default_gravatar)


# class GravatarTest(TestCase):
# 	user_email = 'valchygaming@gmail.com'
# 	fake_email = 'ThisEmailShouldNeverWork@SomeTotallyRandomDomain.com'
#
# 	def test_user_gravatar_positive(self):
# 		# user = User.objects.create(email=self.user_email)
# 		gravatar_image = get_gravatar_link(self.user_email)
# 		self.assertIsNotNone(gravatar_image)
#
# 	def test_user_gravatar_negative(self):
# 		# user = User.objects.create(email=self.user_email)
# 		gravatar_image = get_gravatar_link(self.fake_email)
# 		self.assertIsNone(gravatar_image)


class GithubManager(TestCase):
	@classmethod
	def setUpTestData(cls):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		sample_path = '__test_data__/sample_github_profile.html'
		full_path = os.path.join(dir_path, sample_path)

		with open(full_path, 'r') as fr:
			cls.sample_content = fr.read().encode()

		cls.proper_email = 'valchygaming@gmail.com'

	def test_unit_extract_repositories_from_sample(self):
		repositories_cnt = extract_github_repositories(self.sample_content)
		self.assertEqual(repositories_cnt, 34)

	def test_get_github_repositories(self):
		random_user = User.objects.create(username='randomUser', email=self.proper_email)
		cool_user = CoolUser.objects.create(user=random_user, github_profile='valchy')
		self.assertGreaterEqual(cool_user.gh_repositories, 1)

	def test_get_github_repositories_of_random_account(self):
		random_user = User.objects.create(username='randomUser', email=self.proper_email)
		cool_user = CoolUser.objects.create(user=random_user, github_profile='valchy_some_random_username')
		self.assertEqual(cool_user.gh_repositories, None)

	def test_github_repositories_updating(self):
		random_user = User.objects.create(username='randomUser', email=self.proper_email)
		cool_user = CoolUser.objects.create(user=random_user, github_profile='valchy_some_random_username')
		self.assertEqual(cool_user.gh_repositories, None)

		cool_user.github_profile = 'valchy'
		cool_user.save()

		self.assertGreaterEqual(cool_user.gh_repositories, 34)

		cool_user.github_profile = 'valchy_some_random_username'
		cool_user.save()
		self.assertEqual(cool_user.gh_repositories, None)


class StatsManager(TestCase):
	@classmethod
	def setUpTestData(cls):
		category = Category.objects.create(slug='random', label='Random News')
		cls.category = category
		cls.juan = User.objects.create(first_name='juanito', is_active=True, username='juanito')
		author = CoolUser.objects.create(user=cls.juan)
		cls.author = author
		for title, body in zip(TITLES, BODIES):
			_ = Post.objects.create(author=author, category=category, title=title, body=body)

	def test_stats_sample(self):
		msg = 'science ' * 3 + 'art ' * 7 + 'cats ' * 7 + 'of ' * 10 + 'a ' * 10
		sd = StatsDict.from_msg(msg)
		self.assertEqual(sd.top(1), {'a': 10})
		self.assertEqual(sd.top(2), {'a': 10, 'of': 10})
		self.assertEqual(sd.top(10), {'a': 10, 'of': 10, 'art': 7, 'cats': 7, 'science': 3, '': 1})
		from_sd = sd.top(5)
		self.assertEqual(from_sd.top(2), {'a': 10, 'of': 10})

	def test_single_post(self):
		title = 'Applied Python Module because python is awesome, yes it is' * 100
		body = 'This is a description of the module just for fun and to sew how it looks ' \
			   'like like like like or subscribe'
		sample_post = Post.objects.create(title=title, body=body, author=self.author, category=self.category)
		stats = extract_stats_from_single_post(sample_post)

		# self.assertEqual(stats.titles.top(2), {'is': 2, 'python': 2})
		# self.assertEqual(stats.bodies.top(1), {'like': 4})
		# self.assertEqual(stats.all.top(1), {'like': 4})

		# Testing the generation of wordcloud images
		dir_path = os.path.dirname(os.path.realpath(__file__))
		filename = '__test_data__/single_post.jpg'
		file_path = os.path.join(dir_path, filename)
		generated_file = stats.titles.to_file(file_path)
		file_size = os.path.getsize(generated_file)
		self.assertGreater(file_size, 0)

		# Testing the generation of the svg
		svg_generated = stats.titles.to_svg()
		self.assertIsNotNone(svg_generated)

	def test_multi_posts(self):
		posts = Post.objects.filter(category=self.category)
		stats = extract_stats_from_posts(posts)

		self.assertEqual(stats.titles.top(2), {'of': 2, 'python': 2})
		self.assertEqual(stats.bodies.top(5), {'to': 23, 'and': 16, 'the': 16, 'a': 13, '': 10})
		self.assertEqual(stats.all.top(7), {'to': 23, 'and': 16, 'the': 16, 'a': 13, '': 10, 'of': 10, 'is': 9})


class SearchBoxManager(TestCase):
	@classmethod
	def setUpTestData(cls):
		category = Category.objects.create(slug='random', label='Random News')
		cls.category = category
		cls.juan = User.objects.create(first_name='juanito', is_active=True, username='juanito')
		author = CoolUser.objects.create(user=cls.juan)
		cls.author = author

		for title, body in zip(TITLES, BODIES):
			_ = Post.objects.create(author=author, category=category, title=title, body=body)

	def setUp(self):
		self.client = Client()

	def test_search_box(self):
		search_text = 'python'
		url = reverse('post-filtered')
		response = self.client.get(url, data=dict(q=search_text))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['post_list']), 2)

		self.assertEqual(Post.objects.count(), 3)

		search_text = 'valchy'
		response = self.client.get(url, data=dict(q=search_text))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['post_list']), 3)
		self.assertEqual(Post.objects.count(), 3)


class MediaStackManager(TestCase):
	@classmethod
	def setUpTestData(cls):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		sample_path = '__test_data__/news_sample.json'
		full_path = os.path.join(dir_path, sample_path)
		with open(full_path, 'r') as fr:
			cls.ms_json = json.load(fr)

	def test_insert_staff_post(self):
		content = {"author": "CBS Sports Staff",
				   "title": "2021 Fantasy football draft prep: Tips, rankings, advice, rookies, strategy, top 150 by dialed-in experts",
				   "description": "SportsLine's 2021 Fantasy football draft bible can give you a huge edge in your league",
				   "url": "https://www.cbssports.com/fantasy/football/news/2021-fantasy-football-draft-prep-tips-rankings-advice-rookies-strategy-top-150-by-dialed-in-experts/",
				   "source": "CBSSports.com",
				   "image": None,
				   "category": "sports",
				   "language": "en",
				   "country": "us",
				   "published_at": "2021-08-03T15:26:41+00:00"
				   }
		post = insert_post_from_mediastack(content)
		expected_username = 'staff@cbssports.com'
		self.assertGreater(post.id, 0)
		self.assertEqual(post.author.user.username, expected_username)
		self.assertEqual(post.image_link, None)

	def test_insert_no_author(self):
		content = {
			"author": None,
			"title": "Colts lose OG Nelson to same injury as Wentz",
			"description": "Colts All-Pro guard Quenton Nelson will miss the next five to 12 weeks after suffering the same foot injury as quarterback Carson Wentz.",
			"url": "https://www.espn.com/nfl/story/_/id/31950239/indianapolis-colts-ol-quenton-nelson-5-12-weeks-foot-injury",
			"source": "ESPN",
			"image": "https://a.espncdn.com/photo/2019/0315/r514924_600x600_1-1.jpg",
			"category": "sports",
			"language": "en",
			"country": "us",
			"published_at": "2021-08-03T16:35:14+00:00"
		}
		post = insert_post_from_mediastack(content)
		expected_username = 'anonymous@coolpress.com'
		self.assertGreater(post.id, 0)
		self.assertEqual(post.author.user.username, expected_username)
		self.assertEqual(post.image_link, "https://a.espncdn.com/photo/2019/0315/r514924_600x600_1-1.jpg")

	def test_insert_no_source_link_no_image_link(self):
		content = {
			"author": None,
			"title": "Colts lose OG Nelson to same injury as Wentz",
			"description": "Colts All-Pro guard Quenton Nelson will miss the next five to 12 weeks after suffering the same foot injury as quarterback Carson Wentz.",
			"url": "https://www.espn.com/nfl/story/_/id/31950239/indianapolis-colts-ol-quenton-nelson-5-12-weeks-foot-injury",
			"source": None,
			"image": None,
			"category": "sports",
			"language": "en",
			"country": "us",
			"published_at": "2021-08-03T16:35:14+00:00"
		}
		post = insert_post_from_mediastack(content)
		expected_username = 'anonymous@coolpress.com'
		self.assertGreater(post.id, 0)
		self.assertEqual(post.author.user.username, expected_username)
		self.assertEqual(post.image_link, None)
		self.assertEqual(post.source_link, 'MediaStack News')

	def test_insert_named_author_post(self):
		content = {
			"author": "Divya Chaturvedi",
			"title": "Biles Says She Is Proud To Bring The Topic of Mental Health This Olympics",
			"description": "Simone Arianne Biles is an American artistic gymnast. Having a combined total of 32 Olympic and World Championship medals, Biles has tied with Larisa Latynina as the most decorated gymnast of all time. Biles made her long-awaited return to the Olympic Games on Tuesday, taking bronze in the beam final won by Chinese teenager Guan&#8230;The post Biles Says She Is Proud To Bring The Topic of Mental Health This Olympics appeared first on EssentiallySports.",
			"url": "https://www.essentiallysports.com/tokyo-olympics-gymnastics-news-2020-biles-says-she-is-proud-to-bring-the-topic-of-mental-health-this-olympics/",
			"source": "Essentially Sports",
			"image": "https://image-cdn.essentiallysports.com/wp-content/uploads/2021-07-28T044235Z_1862452368_SP1EH7R0VYFUZ_RTRMADP_3_OLYMPICS-2020-GAR-W-TEAM-FNL-411x315.jpg",
			"category": "sports",
			"language": "en",
			"country": "us",
			"published_at": "2021-08-03T17:03:36+00:00"
		}
		post = insert_post_from_mediastack(content)
		expected_username = 'dchaturvedi@coolpress.com'
		self.assertGreater(post.id, 0)
		self.assertEqual(post.author.user.username, expected_username)
		self.assertEqual(post.image_link, "https://image-cdn.essentiallysports.com/wp-content/uploads/2021-07-28T044235Z_1862452368_SP1EH7R0VYFUZ_RTRMADP_3_OLYMPICS-2020-GAR-W-TEAM-FNL-411x315.jpg")

	def test_insert_named_with_3_author_post(self):
		content = {
			"author": "Divya Chaturvedi SecondLast",
			"title": "Biles Says She Is Proud To Bring The Topic of Mental Health This Olympics",
			"description": "Simone Arianne Biles is an American artistic gymnast. Having a combined total of 32 Olympic and World Championship medals, Biles has tied with Larisa Latynina as the most decorated gymnast of all time. Biles made her long-awaited return to the Olympic Games on Tuesday, taking bronze in the beam final won by Chinese teenager Guan&#8230;The post Biles Says She Is Proud To Bring The Topic of Mental Health This Olympics appeared first on EssentiallySports.",
			"url": "https://www.essentiallysports.com/tokyo-olympics-gymnastics-news-2020-biles-says-she-is-proud-to-bring-the-topic-of-mental-health-this-olympics/",
			"source": "Essentially Sports",
			"image": "https://image-cdn.essentiallysports.com/wp-content/uploads/2021-07-28T044235Z_1862452368_SP1EH7R0VYFUZ_RTRMADP_3_OLYMPICS-2020-GAR-W-TEAM-FNL-411x315.jpg",
			"category": "sports",
			"language": "en",
			"country": "us",
			"published_at": "2021-08-03T17:03:36+00:00"
		}
		post = insert_post_from_mediastack(content)
		expected_username = 'dsecondlast@coolpress.com'
		self.assertGreater(post.id, 0)
		self.assertEqual(post.author.user.username, expected_username)
		self.assertEqual(post.image_link, "https://image-cdn.essentiallysports.com/wp-content/uploads/2021-07-28T044235Z_1862452368_SP1EH7R0VYFUZ_RTRMADP_3_OLYMPICS-2020-GAR-W-TEAM-FNL-411x315.jpg")

	def test_get_mediastack_sport_posts(self):
		categories = ['sports', 'health']
		languages = ['en']
		limit = 10
		posts_created = gather_and_create_news(categories, languages, limit)
		self.assertEqual(len(posts_created), 10)

		posts_created_twice = gather_and_create_news(categories, languages, limit)
		self.assertLess(len(posts_created_twice), len(posts_created))
