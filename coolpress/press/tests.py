from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from press.models import CoolUser, Category


class PostModelTest(TestCase):
	def test_sample_post(self):
		u = User.objects.create(first_name='juantigo')
		cu = CoolUser.objects.create(user=u)
		self.assertEqual(cu.id, 1)

	def test_reaching_unknown_post(self):
		response = self.client.get(reverse('post-detail', kwargs={'post_id': 9999999}))
		self.assertEqual(response.status_code, 404)

	def test_categories_count_same_as_context(self):
		categories = Category.objects.all()
		response = self.client.get(reverse('category-list'))
		context_categories = response.context['categories']
		self.assertCountEqual(categories, context_categories)
