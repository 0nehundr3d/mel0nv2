import nextcord
from nextcord.ext import commands
import json
from utility import converters
import os
from datetime import datetime

def main():

	# Get configuration.json
	with open("config/configuration.json", "r") as config:
		data = json.load(config)
		prefix = data["prefix"]
		manager = data["manager"]
		status = data["status"]
		game = data["game"]
		gameType = data["gameType"]
	
	with open("config/token.txt", "r") as t:
		token = t.read()

	data["startTime"] = f"{datetime.now()}"

	with open("config/configuration.json", "w") as config:
		json.dump(data, config, indent=4)

	bot = commands.Bot(prefix, intents = nextcord.Intents.all())
	bot.remove_command("help")

	# Load cogs
	for cog in [x[:-3] for x in os.listdir("cogs") if x[-3:] == ".py"]:
		try:
			bot.load_extension(f"cogs.{cog}")
			print(f"Loaded {cog}")
		except Exception as e:
			print(f"Failed to load extension {cog}: {e}")

	@bot.event
	async def on_ready():
		print(f"We have logged in as {bot.user}")
		await bot.change_presence(activity=nextcord.Activity(type=converters.Convertor.convertGameType(gameType), name = game), status=converters.Convertor.convertStatus(status))
		print(nextcord.__version__)

	def check_manager():
			def predicate(ctx):
				return ctx.author.id in manager
			return commands.check(predicate)

	@check_manager()
	@bot.command(hidden=True)
	async def load(ctx, *, module):
			try:
				bot.load_extension(f"cogs.{module}")
			except commands.ExtensionError as e:
				await ctx.send(f"{e.__class__.__name__}: {e}")
			else:
				embed=nextcord.Embed(title=f"Loaded {str(module).capitalize()}", description=f"Successfully loaded cogs.{str(module).lower()}!", color=0x2cf818)
				await ctx.send(embed=embed)

	@check_manager()
	@bot.command(hidden=True)
	async def unload(ctx, *, module):
			try:
				bot.unload_extension(f"cogs.{module}")
			except commands.ExtensionError as e:
				await ctx.send(f"{e.__class__.__name__}: {e}")
			else:
				embed=nextcord.Embed(title=f"Unloaded {str(module).capitalize()}", description=f"Successfully unloaded cogs.{str(module).lower()}!", color=0xeb1b2c)
				await ctx.send(embed=embed)

	@check_manager()
	@bot.command(name="reload", hidden=True)
	async def _reload(ctx, *, module):
			try:
				bot.reload_extension(f"cogs.{module}")
			except commands.ExtensionError as e:
				await ctx.send(f"{e.__class__.__name__}: {e}")
			else:
				embed=nextcord.Embed(title=f"Reloaded {str(module).capitalize()}", description=f"Successfully reloaded cogs.{str(module).lower()}!", color=0x00d4ff)
				await ctx.send(embed=embed)

	bot.run(token)

if __name__ == "__main__":
	main()