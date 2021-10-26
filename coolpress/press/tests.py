from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from press.models import CoolUser


class PostModelTest(TestCase):
	def test_sample_post(self):
		u = User.objects.create(first_name='juantigo')
		cu = CoolUser.objects.create(user=u)
		self.assertEqual(cu.id, 1)