import pygame, util
class reflect:
	def __init__(self, scale):
		self.reflectWidth = 20 * scale
		self.reflectHeight = 5 * scale
		self.verticalOffset = 6 * scale
		self.positionTuple = (0,0)
		self.sizeTuple = (self.reflectWidth, self.reflectHeight)
		self.isVisible = False
	def newReflect(self, player):
		playPosition = player.getPosition()
		playSize = player.getSize()
		playPosition = (playPosition[0] + playSize[0] / 2 - self.reflectWidth / 2, playPosition[1] - self.verticalOffset)
		self.positionTuple = playPosition
	def updateReflect(self, surface):
		pygame.draw.rect(surface, util.white, pygame.Rect(self.positionTuple, self.sizeTuple))
	def returnRect(self):
		return (self.positionTuple, self.sizeTuple)
	def show(self):
		self.isVisible = True
	def hide(self):
		self.isVisible = False
	def canSee(self):
		return self.isVisible
	def toRect(self):
		return pygame.Rect(self.positionTuple, self.sizeTuple)
