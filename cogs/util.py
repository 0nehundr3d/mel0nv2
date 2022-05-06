import nextcord
from nextcord.ext import commands
import json
import os

class Util(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	with open("config/configuration.json", "r") as f: config = json.load(f)
	managers = config["manager"]

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

	@commands.command()
	async def help(self, ctx):
		await ctx.send("Help commands are hard lol just ping 0ne")

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

def setup(bot:commands.Bot):
	bot.add_cog(Util(bot))