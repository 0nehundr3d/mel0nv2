import json
from nextcord.ext import commands

def is_manager():
	def preticate(ctx):
		with open("config/configuration.json", "r") as f: config = json.load(f)
		return ctx.author.id in config["manager"]
	return commands.check(preticate)