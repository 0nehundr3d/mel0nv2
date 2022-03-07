import nextcord
from nextcord.ext import commands
from Wrappers.e621Wrapper import E621API
import json

class NSFW(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot	
		self.e6Client = E621API(user_agent="C0FEFEBOTT (by 0ne)")

	with open("config/configuration.json", "r") as f:
		manager = json.load(f)["manager"]

	@commands.command()
	async def yiff(self, ctx, tags:str = "", limit:int = 1):
		if not ctx.channel.nsfw and ctx.author.id not in self.manager: return await ctx.send("This command can only be used in NSFW channels.")
		
		posts = self.e6Client.get_posts(tags, limit)
		for post in posts["posts"]:
			postUrl= post["file"]["url"]
			artist = ""
			for i in post["tags"]["artist"]:
				if i != post["tags"]["artist"][-1]:
					artist += f"{i},"
				else:
					artist += i

			embed = nextcord.Embed(title="Source",url=post["sources"][0])
			embed.set_image(url=postUrl)
			embed.set_author(name=f"artist(s): {artist}")

			await ctx.send(embed=embed)

def setup(bot:commands.Bot):
	bot.add_cog(NSFW(bot))