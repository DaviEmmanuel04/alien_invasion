import pygame
from pygame.sprite import Group


from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
	# Inicializa o jogo e cria um objeto para tela
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	
	# Cria uma instância para armazenar dados estatísticos do jogo
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	# Cria o botão play
	play_button = Button(ai_settings, screen, "Play")
	
	
	# Cria uma nave
	ship = Ship(ai_settings, screen)	
	
	
	# Cria um grupo no qual serão armazenados os projéteis
	bullets = Group()
	
	
	# Cria um grupo para os aliens
	aliens = Group()
	
	
	# Cria uma frota de aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	
	# Carrega a e inicia a musica de fundo
	pygame.mixer.music.load("sound/bg_music.mp3")
	pygame.mixer.music.play(-1)
	
	
	# Sons do jogo
	laser = pygame.mixer.Sound("sound/laser.wav")
	explosion = pygame.mixer.Sound("sound/explosion.wav")
	
	
	# Inicializa o laço principal do jogo
	while True:
		
		
		# Observa eventos de teclado e mouse
		gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, laser)
		
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosion)
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
		
		
		gf.update_sreen(ai_settings, screen, stats, sb, ship, aliens, bullets,
			play_button)		
				
				
run_game()				
