from nextcord.ext import commands
import nextcord
import typing
from utility import decorators

class Pain(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
		self.last = None

	Decorators = decorators.Decorators()

	@commands.command()
	async def say(self, ctx,channel: typing.Optional[nextcord.TextChannel], *, message:str):
		if channel is None:
			channel = ctx.channel
		await channel.send(message)

	@Decorators.is_manager()
	@commands.command()
	async def message(self, ctx, user: typing.Optional[nextcord.User], *, message:str):
		if user:
			self.last = user
		elif not user and self.last:
			user = self.last
		else:
			return await ctx.send("No user specified.")
		await user.send(message)
		await ctx.send(f"Message sent to {user}.")

	@Decorators.is_manager()
	@commands.command()
	async def showLast(self, ctx):
		if self.last:
			await ctx.author.send(f"{self.last.name}#{self.last.discriminator}({self.last.id})")
		else:
			await ctx.send("No last user found.")

def setup(bot:commands.Bot):
	bot.add_cog(Pain(bot))