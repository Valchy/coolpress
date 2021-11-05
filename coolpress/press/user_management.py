from typing import Optional

from bs4 import BeautifulSoup
from libgravatar import Gravatar
from pip._vendor import requests


def get_gravatar_link(email: str) -> Optional[str]:
	g = Gravatar(email)
	return g.get_image(size=280)


def extract_github_repositories(content) -> Optional[int]:
	soup = BeautifulSoup(content, 'html.parser')
	css_selector = 'a[href$="repositories"] span'
	repositories_info = soup.select_one(css_selector)

	return int(repositories_info.text)


def extract_github_followers(content) -> Optional[int]:
	soup = BeautifulSoup(content, 'html.parser')
	css_selector = 'a[href$="followers"] span'
	followers_info = soup.select_one(css_selector)

	return int(followers_info.text)


def extract_github_following(content) -> Optional[int]:
	soup = BeautifulSoup(content, 'html.parser')
	css_selector = 'a[href$="following"] span'
	following_info = soup.select_one(css_selector)

	return int(following_info.text)


def get_github_data(github_profile):
	url = f'https://github.com/{github_profile}'
	response = requests.get(url)
	gh_repositories = None
	gh_followers = None
	gh_following = None

	if response.status_code == 200:
		gh_repositories = extract_github_repositories(response.content)
		gh_followers = extract_github_followers(response.content)
		gh_following = extract_github_following(response.content)

	return gh_repositories, gh_followers, gh_following
