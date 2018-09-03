#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2018 Lorenzo <Lorenzo@LORENZO-HP>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import pygame, sys, util, bullet, math, player, reflect, enemy, random
import pygame.font
import os
def main(args):
	pygame.init()
	pygame.font.init()
	
	#scale changes the scale of everything
	scale = 2
	
	#320x240 resolution CAN BE CHANGED
	size = (scale * 320,scale * 240)
	isMainMenu = True
	needToDrawMainMenu = True
	previousFrameTime = 0
	timeBetweenFrames = 16
	gameNameFont = pygame.font.Font(os.path.join("fonts", "pcsenior.ttf"), 10 * scale)
	gameInfoFont = pygame.font.Font(os.path.join("fonts", "pcsenior.ttf"), 5 * scale)
	hasChangedColor = False
	dangerDisplayed = False
	dangerMessageTickLength = 500
	dangerMessageTickSoFar = 0
	score = 0
	timeBetweenEnemySpawn = 300
	timeSinceEnemySpawn = timeBetweenEnemySpawn / 2
	
	reflectTickTime = 20
	relfectTimeOnScreen = 0
	reflectPresent = False
	
	gameScreen = pygame.display.set_mode(size)
	gameScreen.fill(util.black)
	pygame.display.update()
	
	warningMessage = gameNameFont.render("CAUTION!!", True, util.white)
	
	mainCharacter = player.player((int(size[0] / 2), size[1]), scale)
	reflectBlock = reflect.reflect(scale)
	enemyList = []
	lives = 3
	gameOver = False
	while not(gameOver):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		currentTime = pygame.time.get_ticks()
		if currentTime - previousFrameTime > timeBetweenFrames:
			previousFrameTime = currentTime
			timeSinceEnemySpawn += 1
			gameScreen.fill(util.black)
			
			#lives counter
			for dot in range(lives):
				pygame.draw.circle(gameScreen, util.green, (5 * scale + 11 * scale * dot, 5 * scale), 5 * scale)
				
			if timeBetweenEnemySpawn <= timeSinceEnemySpawn:
				#add a new wave of enemies
				timeSinceEnemySpawn = 0
				enemiesToSpawn = random.randint(4, 8)
				spawnRange = size[0] / enemiesToSpawn
				for count in range(enemiesToSpawn - 1):
					#(0 == count % 2) generates red on even ships
					enemyList.append(enemy.enemy((5 + count * spawnRange, 5), (0 == count % 2), count % 3, 10 * random.randint(3, 6), random.randint(2, 5), random.uniform(5 * math.pi / 4, 7 * math.pi / 5), gameScreen.get_size(), scale))
			
			
			#update player character
			keys = pygame.key.get_pressed()
			
			#move ship
			if keys[pygame.K_LEFT]:
				mainCharacter.move(scale * -2, gameScreen)
			if keys[pygame.K_RIGHT]:
				mainCharacter.move(scale * 2, gameScreen)
			
			#changing the color of the ship and making sure it doesn't change too quickly
			if keys[pygame.K_z] and not(hasChangedColor):
				mainCharacter.changeColor()
				hasChangedColor = True
			if not(keys[pygame.K_z]):
				hasChangedColor = False
				
			#reflect mechanic
			if keys[pygame.K_SPACE] and not(reflectPresent):
				reflectPresent = True
				reflectTimeOnScreen = reflectTickTime
				reflectBlock.newReflect(mainCharacter)
				reflectBlock.show()
			if not(keys[pygame.K_SPACE]) and reflectPresent:
				#keep the reflect on the screen for a certain amount fo time after space is pressed
				reflectTimeOnScreen -= 1
				if reflectTimeOnScreen == 0:
					reflectPresent = False
					reflectBlock.hide()
			if reflectPresent:
				reflectBlock.updateReflect(gameScreen)
			if dangerDisplayed:
				gameScreen.blit(warningMessage, (gameScreen.get_width() / 2 - warningMessage.get_width() / 2, 2 * scale))
				dangerMessageTickSoFar += 1
				if dangerMessageTickSoFar > timeBetweenEnemySpawn / 2:
					dangerMessageTickSoFar = 0
					dangerDisplayed = False
			for enemyShip in enemyList:
				score = enemyShip.update(gameScreen, reflectBlock, enemyList, score)
				if enemyShip.checkCollision(mainCharacter):
					lives -= 1
					enemyList = []
					dangerDisplayed = True
					if lives == 0:
						gameOver = True
			scoreText = gameInfoFont.render(str(score), False, util.white)
			gameScreen.blit(scoreText, (gameScreen.get_width() - scoreText.get_width(), gameScreen.get_height() - mainCharacter.getHeight() - scoreText.get_height()))
			mainCharacter.update(gameScreen)
			pygame.display.update()
			
	gameScreen.fill(util.black)
	gameOverText = gameNameFont.render("GAME OVER!", True, util.white)
	gameOver2Text = gameInfoFont.render("To play again, quit this screen and reload", False, util.white)
	scoreText = gameInfoFont.render("Score: " + str(score), False, util.white)
	gameScreen.blit(gameOverText, (gameScreen.get_width() / 2 - gameOverText.get_width() / 2, 3 * scale))
	gameScreen.blit(gameOver2Text, (gameScreen.get_width() / 2 - gameOver2Text.get_width() / 2, gameOverText.get_height() + scale))
	gameScreen.blit(scoreText, (gameScreen.get_width() / 2 - scoreText.get_width() / 2, gameOverText.get_height() + 2 * scale + gameOver2Text.get_height()))
	pygame.display.update()
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
