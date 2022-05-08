from nextcord.ext import commands
import nextcord
import typing

class Pain(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	@commands.command()
	async def say(self, ctx,channel: typing.Optional[nextcord.TextChannel], *, message:str):
		if channel is None:
			channel = ctx.channel
		await channel.send(message)

def setup(bot:commands.Bot):
	bot.add_cog(Pain(bot))