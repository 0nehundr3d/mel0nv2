import nextcord
from nextcord.ext import commands


class Util(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

	@commands.command()
	async def help(self, ctx):
		embed = nextcord.Embed(title="Help", description="Help is here.")
		embed.add_field(name="ping", value="Returns the bot's latency.", inline=False)
		embed.add_field(name="help", value="Returns this message.", inline=False)
		embed.add_field(name="addExemption", value="Adds a user to the exemptions list.", inline=False)
		embed.add_field(name="removeExemption", value="Removes a user from the exemptions list.", inline=False)
		embed.add_field(name="isExempt", value="Returns whether a user is exempted.", inline=False)
		await ctx.send(embed=embed)

def setup(bot:commands.Bot):
	bot.add_cog(Util(bot))