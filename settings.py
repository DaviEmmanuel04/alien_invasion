class Settings():
	"""Uma classe para armazenar todas as configurações da invasão alienigena."""
	
	
	def __init__(self):
		# Configurações da tela
		self.screen_width = 1280
		self.screen_height = 640
		self.bg_color = (230, 230, 230)
		
		
		# Configurações da nave
		self.ship_limit = 3
		
		
		# Configurações dos projéteis
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3
		
		
		# Configurações dos alienígenas
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		
		
		# Pontuação
		self.aliens_points = 50
		
		
		# Taxa de aumento de velocidade
		self.speedup_scale = 1.1
		# A taxa com que os pontos aumentam
		self.score_scale = 1.5
		
		
		self.initialize_dynamic_settings()
		
			
	def initialize_dynamic_settings(self):
		"""Inicializa as configurações que mudam no decorrer do jogo"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 2
		self.alien_speed_factor = 1	
		
		
		self.fleet_direction = 1
		
		
	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale 
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale 	
		
		
		self.aliens_points = int(self.aliens_points * self.score_scale)
		
