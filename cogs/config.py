import json
import nextcord
from utility import converters
import utility.decorators as decorators
from nextcord.ext import commands

class Config(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	Decorators = decorators.Decorators()

	@commands.command()
	@Decorators.is_manager()
	async def setGame(self, ctx, *, game:str):
		with open("config/configuration.json", "r") as f: config = json.load(f)
		config["game"] = game

		with open("config/configuration.json", "w") as f:
			json.dump(config, f, indent=4)

		await self.bot.change_presence(activity=nextcord.Activity(type=converters.Convertor.convertGameType(config["gameType"]), name = game), status=converters.Convertor.convertStatus(config["status"]))
		return await ctx.send(f"Game set to {game}")

	@commands.command()
	@Decorators.is_manager()
	async def setGameType(self, ctx, dtype:str):
		with open("config/configuration.json", "r") as f:
			config = json.load(f)
		
		config["gameType"] = converters.Convertor.unConvertGameType(dtype)
		if not config["gameType"]: return await ctx.send("Invalid game type")

		with open("config/configuration.json", "w") as f:
			json.dump(config, f, indent=4)

		await self.bot.change_presence(activity=nextcord.Activity(type=converters.Convertor.convertGameType(config["gameType"]), name = config["game"]), status=converters.Convertor.convertStatus(config["status"]))
		return await ctx.send(f"Game type set to {dtype}")

	@commands.command()
	@Decorators.is_manager()
	async def setStatus(self, ctx, status:str):
		with open("config/configuration.json", "r") as f:
			config = json.load(f)
		
		config["status"] = converters.Convertor.unConvertStatus(status)
		if not config["status"]: return await ctx.send("Invalid game type")

		with open("config/configuration.json", "w") as f:
			json.dump(config, f, indent=4)

		await self.bot.change_presence(activity=nextcord.Activity(type=converters.Convertor.convertGameType(config["gameType"]), name = config["game"]), status=converters.Convertor.convertStatus(config["status"]))
		return await ctx.send(f"status set to {status}")


def setup(bot:commands.Bot):
	bot.add_cog(Config(bot))