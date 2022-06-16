import pygame, sys, random 

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_floating_hearts():
	random_floating_hearts_pos = random.choice(floating_hearts_height)
	bottom_floating_hearts = floating_hearts_surface.get_rect(midtop = (700,random_floating_hearts_pos))
	top_floating_hearts = floating_hearts_surface.get_rect(midbottom = (700,random_floating_hearts_pos - 300))
	return bottom_floating_hearts,top_floating_hearts

def move_floating_heartss(floating_heartss):
	for floating_hearts in floating_heartss:
		floating_hearts.centerx -= 5
	return floating_heartss

def draw_floating_heartss(floating_heartss):
	for floating_hearts in floating_heartss:
		if floating_hearts.bottom >= 1024:
			screen.blit(floating_hearts_surface,floating_hearts)
		else:
			flip_floating_hearts = pygame.transform.flip(floating_hearts_surface,False,True)
			screen.blit(flip_floating_hearts,floating_hearts)
def remove_floating_heartss(floating_heartss):
	for floating_hearts in floating_heartss:
		if floating_hearts.centerx == -600:
			floating_heartss.remove(floating_hearts)
	return floating_heartss
def check_collision(floating_heartss):
	for floating_hearts in floating_heartss:
		if cat_rect.colliderect(floating_hearts):
			#death_sound.play()
			return False

	if cat_rect.top <= -100 or cat_rect.bottom >= 900:
		return False

	return True

def rotate_cat(cat):
	new_cat = pygame.transform.rotozoom(cat,-cat_movement * 3,1)
	return new_cat

def cat_animation():
	new_cat = cat_frames[cat_index]
	new_cat_rect = new_cat.get_rect(center = (100,cat_rect.centery))
	return new_cat,new_cat_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,70))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576,900))
clock = pygame.time.Clock()
game_font = pygame.font.Font('HeartyGeelynEditsMarker-le2d.ttf',60)


# Game Variables
gravity = 0.25
cat_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('hearts2.png').convert() 
bg_surface = pygame.transform.scale2x(bg_surface)


width = 500
height = 40

floor_surface = pygame.image.load('base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

cat_downflap = pygame.transform.scale2x(pygame.image.load('cat4.png').convert_alpha())
cat_frames = [cat_downflap, cat_downflap, cat_downflap]
cat_index = 0 
cat_surface = cat_frames[cat_index]
cat_rect = cat_surface.get_rect(center = (100,512))

catFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(catFLAP,200)

floating_hearts_surface = pygame.image.load('float2.png') #change no.1: the cat can go above or below the obstables 
floating_hearts_surface = pygame.transform.scale2x(floating_hearts_surface)
floating_hearts_list = []
SPAWNfloating_hearts = pygame.USEREVENT
pygame.time.set_timer(SPAWNfloating_hearts,1200)
floating_hearts_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))
'''
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
'''
score_sound_countdown = 100

while True:
	for event in pygame.event.get():


		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
        
			if event.key == pygame.K_SPACE and game_active:
				cat_movement = 0
				cat_movement -= 6
				#flap_sound.play()

            #if event.key == pygame.K_0 and game_active:
                #cat_movement = 0
				#cat_movement -= 8

			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				floating_hearts_list.clear()
				cat_rect.center = (100,512)
				cat_movement = 0
				score = 0
            

		if event.type == SPAWNfloating_hearts:
			floating_hearts_list.extend(create_floating_hearts())

		if event.type == catFLAP:
			if cat_index < 2:
				cat_index += 1
			else:
				cat_index = 0

			cat_surface,cat_rect = cat_animation()
        

	screen.blit(bg_surface,(0,0))

	if game_active:
		# cat
		cat_movement += gravity
		rotated_cat = rotate_cat(cat_surface)
		cat_rect.centery += cat_movement
		screen.blit(rotated_cat,cat_rect)
		game_active = check_collision(floating_hearts_list)

		# floating_hearts
		floating_hearts_list = move_floating_heartss(floating_hearts_list)
		floating_hearts_list = remove_floating_heartss(floating_hearts_list)
		draw_floating_heartss(floating_hearts_list)
		
		score += 0.01
		score_display('main_game')
		score_sound_countdown -= 1
		if score_sound_countdown <= 0:
			#score_sound.play()
			score_sound_countdown = 100
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')

	#floor moving
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0
	
    
	pygame.display.update()
	clock.tick(60)