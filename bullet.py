import pygame, util, math
class bullet:
	def __init__(self, positionTuple, velocity, angle, scale, isRed):
		self.position = positionTuple
		self.velocity = (velocity * math.cos(angle), velocity * math.sin(angle))
		self.innerRadius = 1 * scale
		self.outerRadius = 3 * scale
		self.isReflected = False
		if isRed:
			self.color = util.red
		else:
			self.color = util.blue
	
	def update(self, surface):
		self.position = (int(self.position[0] + self.velocity[0]), int(self.position[1] + self.velocity[1]))
		pygame.draw.circle(surface, self.color, self.position, self.outerRadius)
		pygame.draw.circle(surface, util.white, self.position, self.innerRadius)
		
		if self.position[0] + self.outerRadius < 0:
			return False
		if self.position[0] - self.outerRadius > surface.get_width():
			return False
		if self.position[1] - self.outerRadius > surface.get_height():
			return False
		return True
	def hasReflected(self):
		return self.isReflected
	def getRect(self):
		return pygame.Rect((self.position[0] - self.outerRadius, self.position[1] - self.outerRadius), (2 * self.outerRadius, 2 * self.outerRadius))
	def reflectCheck(self, reflectRect):
		if not(self.isReflected):
			bulletRect = pygame.Rect((self.position[0] - self.outerRadius, self.position[1] - self.outerRadius), (2 * self.outerRadius, 2 * self.outerRadius))
			reflectBlock = reflectRect.toRect()
			self.isReflected = reflectBlock.colliderect(bulletRect)
			if self.isReflected:
				self.velocity = (self.velocity[0], - self.velocity[1])
	def hits(self, checkableEnemy):
		enemyRect = checkableEnemy.getRect()
		bulletRect = self.getRect()
		return enemyRect.colliderect(bulletRect)
