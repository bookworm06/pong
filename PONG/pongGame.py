import pygame
import sys
import random

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1

	#Player score
	if ball.left <= 0:
		pygame.mixer.Sound.play(score_sound)
		player_score += 1
		score_time = pygame.time.get_ticks()

	#Opponent score
	if ball.right >= screen_width:
		pygame.mixer.Sound.play(score_sound)
		opponent_score += 1
		score_time = pygame.time.get_ticks()

	if ball.colliderect(player) and ball_speed_x > 0:
		pygame.mixer.Sound.play(pong_sound)
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1


	if ball.colliderect(opponent) and ball_speed_x < 0:
		pygame.mixer.Sound.play(pong_sound)
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

def player_animation():
	player.y += player_speed
	# if player.top < ball.y:
	# 	player.y += player_speed
	# if player.top > ball.y:
	# 	player.y -= player_speed
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

def opponent_ai():
	# opponent.y += opponent_speed
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.top > ball.y:
		opponent.y -= opponent_speed
	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height

#Restarting the ball
def ball_restart():
	global ball_speed_x, ball_speed_y, score_time

	current_time = pygame.time.get_ticks()
	ball.center = (screen_width/2, screen_height/2)

	if current_time - score_time < 700:
		number_three = game_font.render("3", False, light_grey)
		screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))

	if 700 < current_time - score_time < 1400:
		number_two = game_font.render("2", False, light_grey)
		screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))

	if 1400 < current_time - score_time < 2100:
		number_one = game_font.render("1", False, light_grey)
		screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_x, ball_speed_y = 0, 0
	else:
		ball_speed_y = 7 * random.choice((1, -1))
		ball_speed_x = 7 *random.choice((1, -1))
		score_time = None

#General Setup
pygame.mixer.pre_init(44100, -16, 2, 52)
pygame.init()
clock = pygame.time.Clock()

#The Main Window
screen_height = 800
screen_width = 1480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PONG")

#Shapes
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

#Colors
bg_color = pygame.Color('grey3')
light_grey = (2, 220, 200)

#Speeds
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

#Text
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

#Sound
pong_sound = pygame.mixer.Sound("hit.wav")
score_sound = pygame.mixer.Sound("point.wav")

#Score Timer
score_time = True

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				player_speed += 7
			if event.key == pygame.K_UP:
				player_speed -= 7

			if event.key == pygame.K_s:
				opponent_speed += 7
			if event.key == pygame.K_w:
				opponent_speed -= 7

			if event.key == pygame.K_BACKSPACE:
				sys.exit()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				player_speed -= 7
			if event.key == pygame.K_UP:
				player_speed += 7

			if event.key == pygame.K_s:
				opponent_speed -= 7
			if event.key == pygame.K_w:
				opponent_speed += 7

	if player_score >= 15:
		sys.exit()

	if opponent_score >= 15:
		sys.exit()

	#Game Logic
	ball_animation()
	player_animation()
	opponent_ai()

	#Visuals
	screen.fill(bg_color)
	pygame.draw.rect(screen, light_grey, player)
	pygame.draw.rect(screen, light_grey, opponent)
	pygame.draw.ellipse(screen, light_grey, ball)
	pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

	if score_time:
		ball_restart()

	player_text = game_font.render(f"{player_score}", False, light_grey)
	screen.blit(player_text, (760, 400))

	opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
	screen.blit(opponent_text, (700, 400))

	pygame.display.flip()
	clock.tick(60)