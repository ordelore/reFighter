import pygame, math, random, bullet, player
from numpy import linspace
class enemy:
	def __init__(self, positionTuple, isRed, firingPattern, frequency, velocity, angle, screenDimensions, scale):
		self.position = positionTuple
		self.isRed = isRed
		self.firingPattern = firingPattern
		self.frequency = frequency * 2
		self.velocity = (velocity * math.cos(angle), velocity * math.sin(angle))
		self.timeSinceFire = 0
		self.firedWeapons = []
		self.scale = scale
		#1 = straight ahead
		#2 = arc of a set angel w/ certain # of bullets
		#3 = oscillating arc
		
		if firingPattern == 1:
			self.firingAngle = math.pi / 2
			self.angleChanges = False
			self.angleSpread = 0
			self.fireAtOnce = 1
		elif firingPattern == 2:
			self.angleSpread = random.choice((30, 45, 60, 90))
			self.angleChanges = False
			self.firingAngle = math.pi / 2
			if self.angleSpread == 30:
				self.fireAtOnce = 5
			elif self.angleSpread == 45:
				self.fireAtOnce = 9
			elif self.angleSpread == 60:
				self.fireAtOnce = 6
			else:
				self.fireAtOnce = 10
		else:
			self.firingAngle = math.pi / 2
			self.angleChanges = True
			self.angleSpread = random.choice((30, 45, 60, 90))
			self.fireAtOnce = 1
		self.angleSpread = math.radians(self.angleSpread)
		#color sprite
		if isRed:
			self.sprite = pygame.image.load("sprites\\enemyRed.png")
		else:
			self.sprite = pygame.image.load("sprites\\enemyBlue.png")
		#resize sprite to fit the scale
		newSize = tuple([scale*x for x in self.sprite.get_size()])
		self.sprite = pygame.transform.scale(self.sprite, newSize)
		
		self.maxX = screenDimensions[0] - self.sprite.get_width()
		self.minX = 0
		self.maxY = screenDimensions[1] / 2 - self.sprite.get_height()
		self.minY = 0
	def checkCollision(self, player):
		for fired in self.firedWeapons:
			if not(fired.hasReflected()):
				if fired.getRect().colliderect(player.getRect()):
					return True
	def fireWeapon(self):
		startingPosition = (self.position[0] + self.sprite.get_width() / 2, self.position[1] + self.sprite.get_height())
		startingVelocity = 3
		if self.fireAtOnce == 1:
			self.firedWeapons.append(bullet.bullet(startingPosition, startingVelocity, self.firingAngle, self.scale, self.isRed))
		elif self.firingPattern == 2:
			step = 2 * self.angleSpread / self.fireAtOnce
			for outAngle in linspace(self.firingAngle-self.angleSpread, self.firingAngle + self.angleSpread , self.fireAtOnce):
				self.firedWeapons.append(bullet.bullet(startingPosition, startingVelocity, outAngle, self.scale, self.isRed))
	def getRect(self):
		size = self.sprite.get_size()
		return pygame.Rect(self.position, size)
	def update(self, surface, reflectScreen, enemyList, score):
		if self.frequency == self.timeSinceFire:
			self.timeSinceFire = 0
			self.fireWeapon()
		for fired in self.firedWeapons:
			#returns false if off screen
			if not(fired.update(surface)):
				self.firedWeapons.remove(fired)
			if reflectScreen.canSee():
				fired.reflectCheck(reflectScreen)
			#if a bullet is redlected, check to see if it hits an enemy ship
			if fired.hasReflected():
				for checkEnemy in enemyList:
					if fired.hits(checkEnemy):
						score += 150
						enemyList.remove(checkEnemy)
		self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
		
		#bound checking
		newX = self.position[0]
		newY = self.position[1]
		newVX = self.velocity[0]
		newVY = self.velocity[1]
		if self.position[0] <= self.minX:
			newX = self.minX + 1
			newVX = self.velocity[0] * -1
		if self.position[0] >= self.maxX:
			newX = self.maxX - 1
			newVX = self.velocity[0] * -1
		if self.position[1] <= self.minY:
			newY = self.minY + 1
			newVY = self.velocity[1] * -1
		if self.position[1] >= self.maxY:
			newY = self.maxY - 1
			newVY = self.velocity[1] * -1
		self.position = (int(newX), int(newY))
		self.velocity = (newVX, newVY)
		surface.blit(self.sprite, self.position)
		self.timeSinceFire += 1
		return score
