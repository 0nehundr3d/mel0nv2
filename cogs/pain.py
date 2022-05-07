import nextcord
from nextcord.ext import commands


class Pain(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	

def setup(bot:commands.Bot):
	bot.add_cog(Pain(bot))