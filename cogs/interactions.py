import nextcord
from nextcord.ext import commands
from Wrappers.e621Wrapper import E621API
import json

class Interactions(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
		self.e6Client = E621API(user_agent="C0FEFEBOTT (by 0ne)")

	with open("config/configuration.json", "r") as f:
		manager = json.load(f)["manager"]

	@nextcord.slash_command(guild_ids=[851600669961224222], description="access NSFW commands")
	async def nsfw(self, interaction: nextcord.Interaction):
		pass
		
	
	@nsfw.subcommand(description="pull posts from e621.net")
	async def yiff(self, interaction: nextcord.Interaction, 
		tags: str = nextcord.SlashOption(description="tags to search for", default=""),
		limit: int = nextcord.SlashOption(description="number of posts to return", default=1)):
		if not interaction.channel.nsfw and interaction.author.id not in self.manager: return await interaction.send("This command can only be used in NSFW channels.")

		await interaction.send("Sending...")

		posts = self.e6Client.get_posts(tags, limit)
		for post in posts["posts"]:
			postUrl= post["file"]["url"]

			embed = nextcord.Embed(title="Source",url=post["sources"][0]).set_image(url=postUrl)
			await interaction.channel.send(embed=embed)


def setup(bot:commands.Bot):
	bot.add_cog(Interactions(bot))