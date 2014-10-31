from __future__ import print_function

import argparse

# Just so it will work with py2 or py3
try:
	from StringIO import StringIO
except:
	from io import BytesIO as StringIO

try:
	import pycurl
	from bs4 import BeautifulSoup
except ImportError:
	print('You need to have the packages pycurl and BeautifulSoup installed')

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
		' (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'

def get(url):
	# holds response
	output_stream = StringIO()

	c = pycurl.Curl()
	c.setopt(c.USERAGENT, USER_AGENT)
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, output_stream.write)
	c.setopt(c.FOLLOWLOCATION, True)
	try:
		c.perform()
		if c.getinfo(c.HTTP_CODE) >= 299:
			raise IOError('Response code not in 2xx range')
	except Exception:
		raise IOError('Something went wrong when requesting resource.')
	finally:
		c.close()

	return list_posts(output_stream.getvalue())


def list_posts(content):
	soup = BeautifulSoup(content)

	posts = []
	for element in soup.find_all('td', attrs={'class':'title'})[:-1]:
		if element.a:
			posts.append((element.a.string, element.a.attrs['href']))
	return posts


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--get', choices=['news', 'ask', 'newest'], default='news')
	args = parser.parse_args()

	url = 'https://news.ycombinator.com/{0}'.format(
		args.get
	)

	for elements in get(url):
		print(elements)
