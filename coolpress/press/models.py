from datetime import timedelta, datetime
from enum import Enum

import pytz
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from press.user_management import get_gravatar_link, get_github_data


class CoolUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	github_profile = models.CharField(max_length=150, null=True, blank=True)
	gh_repositories = models.IntegerField(null=True, blank=True)
	gh_followers = models.IntegerField(null=True, blank=True)
	gh_following = models.IntegerField(null=True, blank=True)
	last_followers_check = models.DateTimeField(null=True, blank=True)
	gravatar_link = models.CharField(max_length=400, null=True, blank=True)

	def __str__(self):
		user = self.user
		return f'{user.first_name} {user.last_name} ({user.username})'

	def save(self, *args, **kwargs):
		super(CoolUser, self).save(*args, **kwargs)

		date_for_check = datetime.utcnow()
		date_for_check = date_for_check.replace(tzinfo=pytz.utc)
		min_date_for_check = self.last_followers_check

		if min_date_for_check:
			min_date_for_check += timedelta(days=1)

		gh_repositories = None
		gh_followers = None
		gh_following = None

		if self.user.email:
			email = self.user.email
			gravatar_link = get_gravatar_link(email)

			# Getting gravatar link based on user email
			if gravatar_link != self.gravatar_link:
				self.gravatar_link = gravatar_link
				self.save()

		# Getting github profile data
		if self.github_profile and (not self.last_followers_check or date_for_check > min_date_for_check):
			gh_repositories, gh_followers, gh_following = get_github_data(self.github_profile)
			self.last_followers_check = datetime.utcnow()
			self.save()

		# Checking if there is difference in the data and if so resaving it
		if gh_repositories and gh_repositories != self.gh_repositories:
			self.gh_repositories = gh_repositories
			self.save()

		if gh_followers and gh_followers != self.gh_followers:
			self.gh_followers = gh_followers
			self.save()

		if gh_following and gh_following != self.gh_following:
			self.gh_following = gh_following
			self.save()


class Category(models.Model):
	class Meta:
		verbose_name_plural = "categories"

	label = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)

	def get_absolute_url(self):
		return reverse('category-detail', kwargs={'pk': self.pk})

	def __str__(self):
		return f'{self.slug}'


class PostStatus(Enum):
	DRAFT = 'DRAFT'
	PUBLISHED = 'PUBLISHED'


POST_LABELED_STATUS = [
	(PostStatus.DRAFT.value, 'Draft'),
	(PostStatus.PUBLISHED.value, 'Published post'),
]


class Post(models.Model):
	title = models.CharField(max_length=400)
	body = models.TextField()
	image_link = models.CharField(max_length=400, null=True, blank=True)

	word_cloud_link = models.CharField(max_length=400, null=True, blank=True)

	source_link = models.CharField(max_length=400, null=True, blank=True)
	source_label = models.CharField(max_length=400, null=True, blank=True)

	status = models.CharField(
		max_length=32,
		choices=POST_LABELED_STATUS,
		default=PostStatus.DRAFT,
	)

	author = models.ForeignKey(CoolUser, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	creation_date = models.DateTimeField(auto_now_add=True)
	last_update = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.title} - by {self.author.user.username}'
