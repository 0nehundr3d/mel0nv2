from contextlib import redirect_stdout
import io
import textwrap
import traceback
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
		token = data["token"]
		prefix = data["prefix"]
		manager = data["manager"]
		status = data["status"]
		game = data["game"]
		gameType = data["gameType"]

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

	@bot.command(hidden=True, aliases=["e"])
	async def eval(ctx, rawStr:str, *, body: str):
			raw = False
			if rawStr == "true":
				raw = True
			#Evaluates a code

			env = {
					"bot": bot,
					"ctx": ctx,
					"channel": ctx.message.channel,
					"author": ctx.message.author,
					"guild": ctx.message.guild,
					"message": ctx.message,
				}
			if ctx.message.author.id in manager:
				env.update(globals())

				stdout = io.StringIO()

				to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"

				try:
						exec(to_compile, env)
				except Exception as e:
						return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

				func = env["func"]
				try:
					with redirect_stdout(stdout):
							ret = await func()
				except Exception as e:
						value = stdout.getvalue()
						await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
				else:
						value = stdout.getvalue()
						try:
								await ctx.message.add_reaction("\u2705")
						except:
								pass

						if ret is None:
								if value:
										if raw:
											await ctx.send(f"{value}")
										else:
											await ctx.send(f"```py\n{value}\n```")
						else:
								pass

	bot.run(token)

if __name__ == "__main__":
	main()