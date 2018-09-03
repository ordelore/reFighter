import pygame, os
class player:
	def __init__(self, positionTuple, scale):
		self.positionX = positionTuple[0]
		self.positionY = positionTuple[1]
		self.lives = 3
		self.isRed = True
		self.redSprite = pygame.image.load(os.path.join("sprites", "fighterRed.png"))
		self.blueSprite = pygame.image.load(os.path.join("sprites", "fighterBlue.png"))
		#resize sprite to fit the scale
		#assumption: red&blue ships are the same size
		newSize = tuple([scale*x for x in self.redSprite.get_size()])
		self.redSprite = pygame.transform.scale(self.redSprite, newSize)
		self.blueSprite = pygame.transform.scale(self.blueSprite, newSize)
		self.sprite = self.redSprite
		
		self.positionX = positionTuple[0] - self.sprite.get_width() / 2
		self.positionY = positionTuple[1] - self.sprite.get_height()
	def getColor(self):
		return self.isRed
	def getPosition(self):
		return (self.positionX, self.positionY)
	def getSize(self):
		return self.sprite.get_size()
	def changeColor(self):
		self.isRed = not(self.isRed)
		if self.isRed:
			self.sprite = self.redSprite
		else:
			self.sprite = self.blueSprite
	def getHeight(self):
		return self.sprite.get_height()
	def move(self, howMuch, surface):
		if self.positionX + howMuch < surface.get_width() - self.sprite.get_width() and self.positionX + howMuch > 0:
			self.positionX += howMuch
	def update(self, surface):
		surface.blit(self.sprite, (self.positionX, self.positionY))
	def getRect(self):
		return pygame.Rect((self.positionX, self.positionY), self.sprite.get_size())
