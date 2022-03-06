import nextcord
from nextcord.ext import commands
from Wrappers.e621Wrapper import E621API

class NSFW(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot	
		self.e6Client = E621API(user_agent="C0FEFEBOTT (by 0ne)")

	@commands.command()
	async def yiff(self, ctx, tags:str = "", limit:int = 1):
		if not ctx.channel.nsfw: return await ctx.send("This command can only be used in NSFW channels.")
		
		posts = self.e6Client.get_posts(tags, limit)
		for post in posts["posts"]:
			await ctx.send(post["file"]["url"])

def setup(bot:commands.Bot):
	bot.add_cog(NSFW(bot))