import nextcord
from nextcord.ext import commands
import json
import os
from datetime import datetime
import pandas as pd
import utility.decorators as decorators
import typing
from contextlib import redirect_stdout
import io
import textwrap
import traceback

class Util(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	Decorators = decorators.Decorators()

	with open("config/configuration.json", "r") as f: config = json.load(f)
	startTime = config["startTime"]

	@commands.command()
	async def ping(self, ctx):
		embed=nextcord.Embed(title=f"Pong! {round(self.bot.latency * 1000)}ms", color=0x00f21c)
		await ctx.send(embed=embed)

	@commands.command()
	async def help(self, ctx):
		await ctx.send("Help commands are hard just ping 0ne lol")

	@commands.command()
	@Decorators.is_manager()
	async def reloadCogs(self, ctx):

		embed = nextcord.Embed(title="Reloading cogs...", color=0x00f21c)

		for cog in [x[:-3] for x in os.listdir("cogs") if x[-3:] == ".py"]:
			try:
				self.bot.reload_extension(f"cogs.{cog}")
				embed.add_field(name=f"Reloading {cog}.", value="Success!", inline=False)
			except commands.ExtensionNotLoaded:
				try:
					self.bot.load_extension(f"cogs.{cog}")
					embed.add_field(name=f"Loading {cog}.", value="Success!", inline=False)
				except Exception as e:
					embed.add_field(name=f"Loading {cog}",value=f"Failed: {e}",inline=False)
					embed.color = 0xf20004
			except Exception as e:
				embed.add_field(name=f"Reloading {cog}",value=f"Failed: {e}",inline=False)
				embed.color = 0xf20004

		await ctx.send(embed=embed)

	@commands.command(aliases=["uptime"])
	async def upTime(self, ctx):
		embed = nextcord.Embed(title="Up Time", color=0x00f21c)

		timeObj = datetime.strptime(self.startTime, "%Y-%m-%d %H:%M:%S.%f")

		embed.add_field(name="Bot Uptime", value=f"{pd.to_timedelta(datetime.now() - timeObj).round('1s')}", inline=False)

		await ctx.send(embed=embed)

	@commands.command(hidden=True, aliases=["e"])
	@Decorators.is_manager()
	async def eval(self, ctx, raw:typing.Optional[bool] = False, *, body: str):
		#Evaluates a code

		env = {
				"bot": self.bot,
				"ctx": ctx,
				"channel": ctx.message.channel,
				"author": ctx.message.author,
				"guild": ctx.message.guild,
				"message": ctx.message,
			}
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

def setup(bot:commands.Bot):
	bot.add_cog(Util(bot))