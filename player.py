import pygame, os
class player:
	def __init__(self, positionTuple, scale):
		self.positionX = positionTuple[0]
		self.positionY = positionTuple[1]
		self.lives = 3
		self.isRed = True
		self.redSprite = self.loadAndResize("fighterRed.png", scale)
		self.blueSprite = self.loadAndResize("fighterBlue.png", scale)
		self.redRightSprite = self.loadAndResize("fighterRedRight.png", scale)
		self.redLeftSprite = self.loadAndResize("fighterRedLeft.png", scale)
		self.blueLeftSprite = self.loadAndResize("fighterBlueLeft.png", scale)
		self.blueRightSprite = self.loadAndResize("fighterBlueRight.png", scale)
		self.sprite = self.redSprite
		self.positionX = positionTuple[0] - self.sprite.get_width() / 2
		self.positionY = positionTuple[1] - self.sprite.get_height()
	def loadAndResize(self, spriteName, scale):
		currentSprite = pygame.image.load(os.path.join("sprites", spriteName))
		#resize sprite to fit the scale
		#assumption: red&blue ships are the same size
		newSize = tuple([scale*x for x in currentSprite.get_size()])
		return pygame.transform.scale(currentSprite, newSize)
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
	def forward(self):
		if self.isRed:
			self.sprite = self.redSprite
		else:
			self.sprite = self.blueSprite
	def move(self, howMuch, surface):
		if self.positionX + howMuch < surface.get_width() - self.sprite.get_width() and self.positionX + howMuch > 0:
			self.positionX += howMuch
		if howMuch > 0:
			if self.isRed:
				self.sprite = self.redRightSprite
			else:
				self.sprite = self.blueRightSprite
		else:
			if self.isRed:
				self.sprite = self.redLeftSprite
			else:
				self.sprite = self.blueLeftSprite
	def update(self, surface):
		surface.blit(self.sprite, (self.positionX, self.positionY))
	def getRect(self):
		return pygame.Rect((self.positionX, self.positionY), self.sprite.get_size())
