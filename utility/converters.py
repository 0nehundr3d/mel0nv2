import nextcord

class Convertor():
	@staticmethod
	def convertGameType(num:int):
		if num == 0:
			return nextcord.ActivityType.playing
		elif num == 1:
			return nextcord.ActivityType.watching
		elif num == 2:
			return nextcord.ActivityType.listening
		elif num == 3:
			return nextcord.ActivityType.competing

	@staticmethod
	def convertStatus(num:int):
		if num == 0:
			return nextcord.Status.online
		elif num == 1:
			return nextcord.Status.idle
		elif num == 2:
			return nextcord.Status.dnd
		elif num == 3:
			return nextcord.Status.invisible

	@staticmethod
	def unConvertStatus(gameType:str):
		if gameType == "online":
			return 0
		elif gameType == "idle":
			return 1
		elif gameType == "dnd":
			return 2
		elif gameType == "invisible":
			return 3
		else:
			return False

	@staticmethod
	def unConvertGameType(gameType:str):
		if gameType == "playing":
			return 0
		elif gameType == "watching":
			return 1
		elif gameType == "listening":
			return 2
		elif gameType == "competing":
			return 3
		else:
			return False
		
