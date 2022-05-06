import nextcord
from nextcord.ext import commands


class Debug(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot


def setup(bot:commands.Bot):
	bot.add_cog(Debug(bot))