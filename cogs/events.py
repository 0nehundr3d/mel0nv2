import nextcord
from nextcord.ext import commands
import json
import utility.decorators as decorators
import typing

class Events(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	Decorators = decorators.Decorators()

	with open("config/exemptions.json", "r") as f:
		e = json.load(f) 
		exemptions = e["exemptions"]

	with open("config/targets.json", "r") as f:
		targets = json.load(f)
		muttHarass = targets["mutt"]
		neoHarass = targets["neo"]

	@commands.command()
	@Decorators.is_manager()
	async def addExemption(self, ctx, user:nextcord.User):

		with open("config/exemptions.json", "r") as f:
			exemptions = json.load(f)
			if user.id in exemptions["exemptions"]: return await ctx.send(f"{user.name} is already exempted."); return

			exemptions["exemptions"].append(user.id)

		with open("config/exemptions.json", "w") as f: json.dump(exemptions, f, indent=4)

		try:
			self.bot.reload_extension("cogs.events")
			await ctx.send(f"Added {user.name} to exemptions.")
		except Exception as e:
			await ctx.reply(f"Failed add user to exemptions.\n{e}")

	@commands.command()
	@Decorators.is_manager()
	async def removeExemption(self, ctx, user:nextcord.User):

		with open("config/exemptions.json", "r") as f:
			exemptions = json.load(f)
			if user.id not in exemptions["exemptions"]: return await ctx.send(f"{user.name} is not exempted."); return

			exemptions["exemptions"].remove(user.id)

		with open("config/exemptions.json", "w") as f: json.dump(exemptions, f, indent=4)

		try:
			self.bot.reload_extension("cogs.events")
			await ctx.send(f"removed {user.name} from exemptions.")
		except Exception as e:
			await ctx.reply(f"Failed remove user from exemptions.\n{e}")

	@commands.command()
	@Decorators.is_manager()
	async def isExempt(self, ctx, user:nextcord.User = None):

		with open("config/exemptions.json", "r") as f:
			exemptions = json.load(f)
			if user.id in exemptions["exemptions"]: 
				await ctx.reply(f"{user.name} is exempted.")
			else:
				await ctx.reply(f"{user.name} is not exempted.")

	@commands.command()
	@Decorators.is_manager()
	async def bully(self, ctx, user:typing.Literal["mutt", "neo"]):
		if user == "mutt":
			await ctx.send(f"Mutt harassment: {not self.muttHarass}")
			self.targets["mutt"] = not self.muttHarass
			with open("config/targets.json", "w") as f:
				json.dump(self.targets, f, indent=4)
			self.bot.reload_extension("cogs.events")
		elif user == "neo":
			await ctx.send(f"Neo harassment: {not self.neoHarass}")
			self.targets["neo"] = not self.neoHarass
			with open("config/targets.json", "w") as f:
				json.dump(self.targets, f, indent=4)
			self.bot.reload_extension("cogs.events")

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.author == self.bot.user: return

		if self.muttHarass and msg.author.id == 972241312805970061: await msg.channel.send("<:CheemWierd:951980915960184842>")
		if self.neoHarass and msg.author.id == 972241312805970061 and "cope" in msg.content: await msg.channel.send("xope")

		if msg.channel.type == nextcord.ChannelType.private and msg.author != self.bot.get_user(346060682388832266): await self.bot.get_user(346060682388832266).send(f"{msg.author.name}#{msg.author.discriminator}({msg.author.id}): {msg.content}")

		if msg.author.id in self.exemptions: return

		msgstring = f" {msg.content.lower()} "
		for item in ['.',',','!','?']:
			msgstring = msgstring.replace(item, "")

		if " horny " in msgstring: await msg.add_reaction("<:gay:898076464061231125>")
		if " cum " in msgstring: await msg.add_reaction("<:cum:950228416135843901>")
		if " bruh " in msgstring: await msg.add_reaction("<a:catdie:951702853817360394>")
		if " mutt " in msgstring: await msg.add_reaction("<:CheemWierd:951980915960184842>")


def setup(bot:commands.Bot):
	bot.add_cog(Events(bot))