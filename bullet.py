import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
	"""Uma classe que administra projéteis disparados pela nave"""
	
	
	def __init__(self, ai_settings, screen, ship):
		"""Cria um projétilna posição atual da nave"""
		super(Bullet, self).__init__()
		self.screen = screen
		
		
		# Cria um rect para o projétil
		self.rect = pygame.Rect(0 ,0, ai_settings.bullet_width,
			ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		
		# Armazena a posição do projétil
		self.y = float(self.rect.y)
		
		
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
	
	
	def update(self):
		"""Move o projétil para cima"""
		# Atualiza a poseção do projétil
		self.y -= self.speed_factor
		# Atualiza a posição de rect
		self.rect.y = self.y
		
		
	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)			
