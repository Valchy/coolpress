from typing import Optional

from libgravatar import Gravatar


# Retrieve gravatar image from user email
def get_gravatar(email: str) -> Optional[str]:
	g = Gravatar(email)
	return g.get_image(size=200, default='', force_default=False, rating='', filetype_extension=False, use_ssl=True)
