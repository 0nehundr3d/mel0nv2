import nextcord
from nextcord.ext import commands


class CogName(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

def setup(bot:commands.Bot):
	bot.add_cog(CogName(bot))