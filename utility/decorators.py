import json
from nextcord.ext import commands

class Decorators:

	def __init__(self):
		with open("config/configuration.json", "r") as f: self.config = json.load(f)

	def reloadJsons(self):
		with open("config/configuration.json", "r") as f: self.config = json.load(f)

	def is_manager(self):
		def preticate(ctx):
			return ctx.author.id in self.config["manager"]
		return commands.check(preticate)