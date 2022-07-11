from multiprocessing.sharedctypes import Value
import random
from nextcord.ext import commands
import random
import re

class CogName(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	@commands.command()
	async def roll(self, ctx, dice:str):
		nums = re.split("d|\+", dice)
		try:
			pNums = [int(num) for num in nums]
		except ValueError:
			await ctx.send("Please make sure you are using the correct dice format")
			print(nums)
			return
		results = [random.randint(1,pNums[1]) for i in range(pNums[0])]

		mod = 0
		if len(pNums) == 3:
			mod = pNums[2]

		await ctx.send(f"{results} total:{sum(results) + mod}")


def setup(bot:commands.Bot):
	bot.add_cog(CogName(bot))