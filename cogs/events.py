import nextcord
from nextcord.ext import commands
import json

class Events(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	with open("config/exemptions.json", "r") as f: exemptions = json.load(f)["exemptions"]
	with open("config/exemptions.json", "r") as f: harass = json.load(f)["muttHarass"]

	with open("config/configuration.json", "r") as f: manager = json.load(f)["manager"]

	@commands.command()
	async def addExemption(self, ctx, user:nextcord.User):
		if ctx.author.id not in self.manager: return

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
	async def removeExemption(self, ctx, user:nextcord.User):
		if ctx.author.id not in self.manager: return

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
	async def isExempt(self, ctx, user:nextcord.User = None):
		if ctx.author not in self.manager or not user: user = ctx.author

		with open("config/exemptions.json", "r") as f:
			exemptions = json.load(f)
			if user.id in exemptions["exemptions"]: 
				await ctx.reply(f"{user.name} is exempted.")
			else:
				await ctx.reply(f"{user.name} is not exempted.")

	@commands.command()
	async def bullyMutt(self, ctx):
		if not ctx.author.id in self.manager: return

		with open("config/exemptions.json", "r") as f: config = json.load(f)

		if self.harass:
			config["muttHarass"] = False
			with open("config/exemptions.json", "w") as f:
				json.dump(config, f, indent=4)
			await ctx.send("Mutt harassment is now disabled.")
			self.bot.reload_extension("cogs.events")
		else:
			config["muttHarass"] = True
			with open("config/exemptions.json", "w") as f:
				json.dump(config, f, indent=4)
			await ctx.send("Mutt harassment is now enabled.")
			await ctx.guild.get_member(525896357756796948).send(":)")
			self.bot.reload_extension("cogs.events")

	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.author.id in self.exemptions: return

		msgstring = f" {msg.content.lower()} "
		for item in ['.',',','!','?']:
			msgstring = msgstring.replace(item, "")

		if self.harass and msg.author.id == 525896357756796948: await msg.channel.send("<:CheemWierd:951980915960184842>")
		if " horny " in msgstring: await msg.add_reaction("<:gay:898076464061231125>")
		if " cum " in msgstring: await msg.add_reaction("<:cum:950228416135843901>")
		if " bruh " in msgstring: await msg.add_reaction("<a:catdie:951702853817360394>")
		if " mutt " in msgstring: await msg.add_reaction("<:CheemWierd:951980915960184842>")


def setup(bot:commands.Bot):
	bot.add_cog(Events(bot))