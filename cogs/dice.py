import random
from nextcord.ext import commands
import random
import re

class CogName(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	@commands.command()
	async def roll(self, ctx, dice:str):
		die = {
			"ammount" : 0,
			"sides" : 0,
			"mod" : 0,
			"reroll" : [],
			"remove" : 0
		}

		die["ammount"] = int(dice[:dice.index(re.search("d", dice).group())])

		dice = dice.replace(dice[:dice.index(re.search("d", dice).group()) + 1], '', 1)

		try:
			die["sides"] = int(dice[:dice.index(re.search("\D", dice).group())])

			dice = dice.replace(dice[:dice.index(re.search("\D", dice).group())], '', 1)
		except:
			die["sides"] = int(dice)
			dice = ''

		detectStr = "[+-rk]"
			
		while re.search(detectStr, dice):
			v = re.search(detectStr, dice).group()

			if v == "+":
				dice = dice.replace('+', '', 1)
				try:
					die["mod"] += int(dice[:dice.index(re.search("\D", dice).group())])
					dice = dice.replace(dice[:dice.index(re.search("\D", dice).group())], '', 1)
				except:
					die["mod"] += int(dice)
					dice = ''

			elif v == "-":
				dice = dice.replace('-', '', 1)
				try:
					die["mod"] -= int(dice[:dice.index(re.search("\D", dice).group())])
					dice = dice.replace(dice[:dice.index(re.search("\D", dice).group())], '', 1)
				except:
					die["mod"] -= int(dice)
					dice = ''

			elif v == "r":
				dice = dice.replace("r", '', 1)
				try:
					die["reroll"].append(int(dice[:dice.index(re.search("\D", dice).group())]))
					dice = dice.replace(dice[:dice.index(re.search("\D", dice).group())], '', 1)
				except:
					die["reroll"].append(int(dice))
					dice = ''
			
			elif v == "k":
				dice = dice.replace("k", '', 1)
				try:
					die["remove"] = (int(dice[:dice.index(re.search("\D", dice).group())]))
					dice = dice.replace(dice[:dice.index(re.search("\D", dice).group())], '', 1)
				except:
					die["remove"] = (int(dice))
					dice = ''

		rolls = []
		removed = []

		if set(range(1, die["sides"]+1, 1)).issubset(set(die["reroll"])):
			return await ctx.send("Can not reroll all dice states")

		if die["ammount"] <= die["remove"]:
			return await ctx.send("Can not remove all rolls")
		

		for i in range(die["ammount"]):
			roll = random.randint(1,die["sides"])
			while roll in die["reroll"]:
				roll = random.randint(1,die["sides"])
			rolls.append(roll)

		for i in range(die["remove"]):
			removed.append(rolls.pop(rolls.index(min(rolls))))

		toSend = f"{rolls} total: {sum(rolls) + die['mod']}"
		if len(removed) > 0:
			toSend = toSend + f" (removed {removed})"

		await ctx.send(toSend)


def setup(bot:commands.Bot):
	bot.add_cog(CogName(bot))