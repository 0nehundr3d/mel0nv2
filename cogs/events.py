import nextcord
from nextcord.ext import commands
import json

class Events(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	with open("config/exemptions.json", "r") as f: exemptions = json.load(f)["exemptions"]

	with open("config/configuration.json", "r") as f: manager = json.load(f)["manager"]

	@commands.command()
	async def addExemption(self, ctx, user:nextcord.User):
		if ctx.author.id not in self.manager: return

		with open("config/exemptions.json", "r") as f:
			exemptions = json.load(f)
			if user.id in exemptions["exemptions"]: return await ctx.send(f"{user.name} is already exempted."); return

			exemptions["exemptions"].append(user.id)
		
		try:
			self.bot.reload_extension("cogs.events")
			await ctx.send(f"Added {user.name} to exemptions.")
		except Exception as e:
			await ctx.reply(f"Failed add user to exemptions.\n{e}")

		with open("config/exemptions.json", "w") as f: json.dump(exemptions, f, indent=4)

	@commands.command()
	async def removeExemption(self, ctx, user:nextcord.User):
		if ctx.author.id not in self.manager: return

		with open("config/exemptions.json", "r") as f:
			exemptions = json.load(f)
			if user.id not in exemptions["exemptions"]: return await ctx.send(f"{user.name} is not exempted."); return

			exemptions["exemptions"].remove(user.id)
		
		try:
			self.bot.reload_extension("cogs.events")
			await ctx.send(f"removed {user.name} from exemptions.")
		except Exception as e:
			await ctx.reply(f"Failed remove user from exemptions.\n{e}")

		with open("config/exemptions.json", "w") as f: json.dump(exemptions, f, indent=4)

	@commands.command()
	async def isExempt(self, ctx, user:nextcord.User = None):
		if ctx.author not in self.manager or not user: user = ctx.author

		with open("config/exemptions.json", "r") as f:
			exemptions = json.load(f)
			if user.id in exemptions["exemptions"]: 
				await ctx.reply(f"{user.name} is exempted.")
			else:
				await ctx.reply(f"{user.name} is not exempted.")


	@commands.Cog.listener()
	async def on_message(self, msg):
		if msg.author.id in self.exemptions: return

		if "horny" in msg.content.lower(): await msg.reply("<:gay:898076464061231125>")

def setup(bot:commands.Bot):
	bot.add_cog(Events(bot))