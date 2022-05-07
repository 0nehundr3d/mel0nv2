from nextcord.ext import commands
from utility import decorators


class Meta(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	Decorators = decorators.Decorators()

	@decorators.is_manager()
	@commands.command()
	async def showFile(self, ctx, file:str):
		pass

def setup(bot:commands.Bot):
	bot.add_cog(Meta(bot))