import nextcord
from nextcord.ext import commands
import Wrappers.e621Wrapper as e621


class NSFW(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	e6Client = e621.E621API(user_agent="0ne/COFEFEBOTT")

	@commands.command()
	async def test(self, ctx):
		await ctx.send(self.e6client.get_posts())

def setup(bot:commands.Bot):
	bot.add_cog(NSFW(bot))