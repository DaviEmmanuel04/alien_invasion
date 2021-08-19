import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	"""Uma classe que representa um único alienígena da frota."""
	
	
	def __init__(self, ai_settings, screen):
		"""Cria e define a posição do alien."""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		
		# Carrega a imagem do alien e define o rect
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		
		# Armazena a posição exata do alien
		self.x = float(self.rect.x)
	
	
	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True		
		
	def update(self):
		"""Move a frota para a direita"""
		self.x += (self.ai_settings.alien_speed_factor *
					self.ai_settings.fleet_direction)
		self.rect.x = self.x	
		
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)	

