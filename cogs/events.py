import nextcord
from nextcord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	with open("config/exemptions.txt", "r") as f:
		exemptions = f.read().splitlines()

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.author.id in self.exemptions: return

		if "horny" in msg.content.lower(): await msg.reply("<:gay:898076464061231125>")

def setup(bot:commands.Bot):
	bot.add_cog(Events(bot))