import nextcord
from nextcord.ext import commands
import json
import os
from datetime import datetime
import pandas as pd

class Util(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	with open("config/configuration.json", "r") as f: config = json.load(f)
	managers = config["manager"]
	startTime = config["startTime"]

	@commands.command()
	async def ping(self, ctx):
		embed=nextcord.Embed(title=f"Pong! {round(self.bot.latency * 1000)}ms", color=0x00f21c)
		await ctx.send(embed=embed)

	@commands.command()
	async def help(self, ctx):
		await ctx.send("Help commands are hard just ping 0ne lol")

	@commands.command()
	async def reloadCogs(self, ctx):
		if ctx.author.id not in self.managers: return await ctx.send("You do not have access to this command.")

		embed = nextcord.Embed(title="Reloading cogs...", color=0x00f21c)

		for cog in [x[:-3] for x in os.listdir("cogs") if x[-3:] == ".py"]:
			try:
				self.bot.reload_extension(f"cogs.{cog}")
				embed.add_field(name=f"Reloading {cog}.", value="Success!", inline=False)
			except Exception as e:
				embed.add_field(name=f"Reloading {cog}",value=f"Failed: {e}",inline=False)
				embed.color = 0xf20004

		await ctx.send(embed=embed)

	@commands.command()
	async def upTime(self, ctx):
		embed = nextcord.Embed(title="Up Time", color=0x00f21c)

		timeObj = datetime.strptime(self.startTime, "%Y-%m-%d %H:%M:%S.%f")

		embed.add_field(name="Bot Uptime", value=f"{pd.to_timedelta(datetime.now() - timeObj).round('1s')}", inline=False)

		await ctx.send(embed=embed)

def setup(bot:commands.Bot):
	bot.add_cog(Util(bot))