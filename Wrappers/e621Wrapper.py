import json
import requests

class E621API:
	def __init__(self, user_agent):
		url_base = "https://e621.net/"
		headers = {"Content-Type": "application/json", "User-Agent": user_agent}

		self.url_base = url_base
		self.headers = headers

	def get_posts(self):
		url = f"{self.url_base}post.json"

		response = requests.get(url, headers=self.headers)

		if response.status_code == 200:
			return json.loads(response.content.decode("utf-8"))
		else:
			return response.status_code

	