import json
import requests

class E621API(object):
	def __init__(self, user_agent):
		self.url_base = "https://e621.net/"
		self.headers = {"Content-Type": "application/json", "User-Agent": user_agent}

	def get_posts(self, tags:str = "", limit:int = 1):
		tags = tags.replace(" ", "+")
		if limit > 10: limit = 10

		url = f"{self.url_base}posts.json?limit={limit}&tags={tags}+status:active+rating:explicit"

		response = requests.get(url, headers=self.headers)

		if response.status_code == 200:
			return json.loads(response.content.decode("utf-8"))
		else:
			return f"{response.status_code}: {response.reason}"

	