from nextcord.ext import commands
import nextcord
import typing
import utility.decorators as decorators

class Pain(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
		self.target = None

	Decorators = decorators.Decorators()

	@commands.command()
	async def say(self, ctx,channel: typing.Optional[nextcord.TextChannel], *, message:str):
		if channel is None:
			channel = ctx.channel
		await channel.send(message)

	@commands.command()
	@Decorators.is_manager()
	async def send(self, ctx, user:typing.Optional[nextcord.User], *, message:str):
		if user == None:
			if self.target == None:
				self.target = self.bot.get_guild(347915804819324930).get_member(346060682388832266)
			user = self.target
		await user.send(message)
		await ctx.send(f"Message Sent to {user.name}#{user.discriminator}!")

	@commands.command()
	@Decorators.is_manager()
	async def setTarget(self, ctx, user:nextcord.User):
		self.target = user
		await ctx.send(f"Target set to:{user.name}#{user.discriminator}")

	@commands.command()
	@Decorators.is_manager()
	async def getTarget(self, ctx):
		await ctx.send(f"Target is:{self.target.name}#{self.target.discriminator}")

def setup(bot:commands.Bot):
	bot.add_cog(Pain(bot))