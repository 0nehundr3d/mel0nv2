from nextcord.ext import commands
from utility import decorators
import math

class Meta(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot

	Decorators = decorators.Decorators()

	@Decorators.is_manager()
	@commands.command()
	async def showFile(self, ctx, file:str):
		with open(file, "r") as f:
			s = f.readlines()
			sanitized = [x.replace("```", "` ``") for x in s]
			block = ''.join(sanitized)
			chunksize = 1990
			chunks = math.ceil(len(block) / chunksize)
			if len(block) > chunksize:
				for i in range(chunks - 1):
					toSend = '```py\n'
					while len(toSend) + len(sanitized[0]) < chunksize:
						toSend += sanitized.pop(0)
					toSend += '```'
					
					await ctx.send(toSend)
				await ctx.send('```py\n' + ''.join(sanitized) + '```')
			else:
				await ctx.send(f"```py\n{block}\n```")

	@Decorators.is_manager()
	@commands.command()
	async def showLine(self, ctx, file:str, line:int):
		with open(file, "r") as f:
			await ctx.send("```py\n" + f.readlines()[line - 1].replace("```", "` ``") + "```")

	@Decorators.is_manager()
	@commands.command()
	async def editLine(self, ctx, file:str, line:int, *, newLine:str):
		with open(file, "r") as f:
			lines = f.readlines()
			lines[line - 1] = newLine + '\n'
		with open(file, "w") as f:
			f.writelines(lines)
		await ctx.send(f"Edited line {line} in {file}.")

def setup(bot:commands.Bot):
	bot.add_cog(Meta(bot))