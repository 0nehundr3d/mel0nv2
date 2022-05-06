import nextcord
from nextcord.ext import commands


class Util(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

	@commands.command()
	async def help(self, ctx):
		await ctx.send("Help commands are hard lol just ping 0ne")

def setup(bot:commands.Bot):
	bot.add_cog(Util(bot))