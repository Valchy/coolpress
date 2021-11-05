from typing import Optional

from bs4 import BeautifulSoup
from libgravatar import Gravatar
from pip._vendor import requests


def get_gravatar_link(email: str) -> Optional[str]:
	g = Gravatar(email)
	return g.get_image(size=280)


def extract_github_repositories(soup) -> Optional[int]:
	css_selector = 'a[href$="repositories"] span'
	repositories_info = soup.select_one(css_selector)

	return int(repositories_info.text)


def extract_github_followers(soup) -> Optional[int]:
	css_selector = 'a[href$="followers"] span'
	followers_info = soup.select_one(css_selector)

	return int(followers_info.text)


def extract_github_following(soup) -> Optional[int]:
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
		soup = BeautifulSoup(response.content, 'html.parser')

		gh_repositories = extract_github_repositories(soup)
		gh_followers = extract_github_followers(soup)
		gh_following = extract_github_following(soup)

	return gh_repositories, gh_followers, gh_following
