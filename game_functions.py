import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets,laser):
	if event.key == pygame.K_RIGHT:
		# Move a espaçonave para a direita
		ship.moving_right = True
	elif event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_LEFT:
		# Move a nave para a esquerda
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
		laser.play()
	elif event.key == pygame.K_g:
		ai_settings.bullet_width = 300	
				
def fire_bullet(ai_settings, screen, ship, bullets):
	# Cria um novo projétil e o adiciona ao grupo
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)				
			
			
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, explosion):
	bullets.update()
		
	
	# Livra-se dos projáteis
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)			
	
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosion)
	
	
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, explosion):	
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:	
		explosion.play()
		for aliens in collisions.values():
			stats.score += ai_settings.aliens_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
			
	
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)		
		
def check_keyup_events(event, ship):
	if	event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False		


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, laser):
	"""Responde a eventos de precionamento de teclas e de mouse."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)	
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets, laser)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)	
			
			
def check_play_button(ai_settings, screen, stats, play_button, ship, 
		aliens, bullets, mouse_x, mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)		
	if button_clicked and not stats.game_active:
		# Reinicia as configurações do jogo
		ai_settings.initialize_dynamic_settings()
		
		
		# Oculta o cursor do mouse
		pygame.mouse.set_visible(False)
		
		
		# Reinicia as estatísticas do jogo
		stats.game_active = True						
		stats.reset_stats()
		
		
		# Esvazia as listas
		aliens.empty()
		bullets.empty
		
		
		# Cria uma nova frota e centraliza a nave
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		

def update_sreen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	"""Atualiza as imagens na tela e alterna para nova tela."""
	# Redesenha a tela a cada passagem pelo laço
	screen.fill(ai_settings.bg_color)
	
	
	for bullet in bullets.sprites():
		bullet.draw_bullet()	
	
		
	ship.blitme()
	aliens.draw(screen)
	
	
	# Desenha a pontuação
	sb.show_score()
	
	
	# Desenha o botão play
	if not stats.game_active:
		play_button.draw_button()
				
				
	# Deixa a tela mais recente visivel
	pygame.display.flip()


def get_number_aliens_x(ai_settings, alien_width):
	avaliable_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(avaliable_space_x/(2 * alien_width))
	return number_aliens_x
	
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determina o número de linhas de aliens que cabem na tela"""
	avaliable_space_y = (ai_settings.screen_height - 
							(3 * alien_height) - ship_height)
	number_rows = int(avaliable_space_y / (2 * alien_height))
	return number_rows
								

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width		
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
	
def create_fleet(ai_settings, screen, ship, aliens):
	"""Cria uma frota de alienigenas"""
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
	alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
			row_number)
			
			
def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
			
def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1	
	
	
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	if stats.ships_left > 0:
		# Decrementa um nave
		stats.ships_left -= 1
	
	
		# Limpa a tela
		aliens.empty()
		bullets.empty()
	
	
		# Cria uma nova frota e reposiciona a nave no centro da tela
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		# Faz uma pausa
		sleep(0.5)
	
	
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	"""Verifica se algum alienigenas alcançou a parte inferior da tela"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break									


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
	
	
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
	
	
def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()	
