import random
from nextcord.ext import commands
import random
import re

from regex import P

class CogName(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	@commands.command()
	async def roll(self, ctx, dice:str):
		die = {
			"ammount" : 0,
			"sides" : 0,
			"mod" : 0,
			"reroll" : []
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

		rolls = []

		if set(range(1, die["sides"]+1, 1)).issubset(set(die["reroll"])):
			return await ctx.send("can not reroll all dice states")

		for i in range(die["ammount"]):
			roll = random.randint(1,die["sides"])
			while roll in die["reroll"]:
				roll = random.randint(1,die["sides"])
			rolls.append(roll)

		await ctx.send(f"{rolls} total: {sum(rolls) + die['mod']}")


def setup(bot:commands.Bot):
	bot.add_cog(CogName(bot))