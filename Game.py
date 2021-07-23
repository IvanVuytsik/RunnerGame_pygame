import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = test_font.render(f'Score{current_time}',False,(64,64,64)) #f string conversion
    score_rect = score_surface.get_rect(center=(400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement (obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10
            if obstacle_rect.bottom == 385:  screen.blit(knight, obstacle_rect)
            else: screen.blit(witch, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collision (hero, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if hero.colliderect(obstacle_rect): return False
    return True

def hero_animation():
    global hero, hero_index
    if hero_rect.bottom < 380:
        hero = hero_jump
    else:
        hero_index += 0.1
        if hero_index >= len(hero_walk): hero_index = 0
        hero = hero_walk[int(hero_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Currier Knight")

clock = pygame.time.Clock()
test_font = pygame.font.Font('ARCADECLASSIC.TTF', 40)
game_active = False
start_time = 0
score = 0

ground_surface = pygame.image.load('venv/ground0.png').convert_alpha()
#ground_surface = pygame.transform.scale(ground_surface, (800, 400))
sky_surface = pygame.image.load('venv/sky0.png').convert_alpha()
sky_surface = pygame.transform.scale(sky_surface, (800, 400))

#bg = pygame.image.load('venv/castle.jpg').convert_alpha()
#bg = pygame.transform.scale(bg, (800, 400))
#bg_rect = bg.get_rect(bg,(800,400))
#score_surface = test_font.render('My Game', False, (64,64,64)) #text,anti-aliasing,color
#score_rect = score_surface.get_rect(center=(400, 60))
#------------------------hero----------------------------------
hero_walk1 = pygame.image.load('venv/knight0.png').convert_alpha()
hero_walk1 = pygame.transform.scale(hero_walk1, (150, 150))
hero_walk2 = pygame.image.load('venv/knightwalk2.png').convert_alpha()
hero_walk2 = pygame.transform.scale(hero_walk2, (150, 150))

hero_walk = [hero_walk1,hero_walk2]
hero_index = 0

hero_jump = pygame.image.load('venv/knightwalk2.png').convert_alpha()
hero_jump = pygame.transform.scale(hero_jump, (150, 150))

hero = hero_walk[hero_index]

hero_rect = hero.get_rect(midbottom=(100, 200))
hero_rect.inflate_ip(-75,0)
# hero_rect = pygame.Rect (left,top, width, height)
hero_gravity = 0

#------------------------obstacles----------------------------------
knight_stand = pygame.image.load('venv/knight1_stand.png').convert_alpha()
knight_stand = pygame.transform.scale(knight_stand, (150, 150))
knight_move = pygame.image.load('venv/knight1_move.png').convert_alpha()
knight_move = pygame.transform.scale(knight_move, (150, 150))
knight_animation = [knight_stand, knight_move]
knight_index = 0
knight = knight_animation [knight_index]

###knight = pygame.transform.scale(knight, (150, 150))
###knight_rect = knight.get_rect(midbottom=((650, 350)))
###knight_rect.inflate_ip(-50,-75)
witch_stand = pygame.image.load('venv/witch.png').convert_alpha()
witch_move = pygame.image.load('venv/witch_move.png').convert_alpha()
witch_animation = [witch_stand, witch_move]
witch_index = 0
witch = witch_animation[witch_index]

obstacle_rect_list = []

####knight_surface.set_colorkey((0,0,0))
#------------------intro screen----------------------------------
hero_intro = pygame.image.load('venv/knight_front.png').convert_alpha()
hero_intro_scaled = pygame.transform.scale(hero_intro, (250, 230))
### pygame.transform.scale2x (hero_intro)
### pygame.transform.rotozoom (hero_intro,0,2) /angle, scalling
hero_intro_rect = hero_intro.get_rect(center=(400,150))

#------------------intro screen----------------------------------
game_name = test_font.render("Currier " + " Knight", False, 'blue')
game_name_rect = game_name.get_rect(center = (400,290))
game_message = test_font.render("Press Space to Start", False, 'blue')
game_message_rect = game_message.get_rect(center = (400,340))

#------------Timer-------------------------------------------------
obstacle_timer = pygame.USEREVENT + 1  # +1 to separate from events reserved for pygame
pygame.time.set_timer(obstacle_timer, 1500)

knight_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(knight_animation_timer, 500)

witch_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(witch_animation_timer, 500)

#-----------------------Game Body----------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # and hero_rect.bottom >= 380:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and hero_rect.bottom >= 380:
                if hero_rect.collidepoint(event.pos):
                    hero_gravity = -25
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and hero_rect.bottom >= 380:
                    hero_gravity = -25
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

        if game_active:
            if event.type == obstacle_timer:
               if randint(0,2):
                    obstacle_rect_list.append(knight.get_rect(midbottom=(randint(900,1100), 385)))
               else:
                    obstacle_rect_list.append(witch.get_rect(midbottom=(randint(900,1100), 210)))

#-----------------------Game Body-Knight and Witch Animation--------
            if event.type == knight_animation_timer:
                if knight_index ==0: knight_index = 1
                else: knight_index =0
                knight = knight_animation[knight_index]

            if event.type == witch_animation_timer:
                if witch_index ==0: witch_index = 1
                else: witch_index =0
                witch = witch_animation[witch_index]
#--------------------------Mouse------------------------------------
        #if event.type == pygame.MOUSEMOTION:
       #if hero_rect.collidepoint(event.pos): print('collision')
#--------------------------Background images and objects------------
    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,100))
        pygame.draw.ellipse(screen, "Yellow", pygame.Rect (550,50,100,100))  # create rect in a figure
        score = display_score()
        #pygame.draw.rect(screen, "red", knight_rect)
        #pygame.draw.rect(screen, "blue", hero_rect)
        #pygame.draw.line(screen, "Gold", (0,0),(800,400), 10)
        #screen.blit(score_surface, score_rect)

    #---------------------Knight movement---------------
        #screen.blit(knight, knight_rect)
        #knight_rect.right -=10
        #if knight_rect.right <= 0: knight_rect.left = 800

    #--------------------gravity and surface-------------
        hero_gravity +=1
        hero_rect.y += hero_gravity
        if hero_rect.bottom >= 380: hero_rect.bottom = 380
        hero_animation()
        screen.blit(hero, hero_rect)
        #hero_rect.left += 1

    #---------------------Obstacle movement-------------
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
    #---------------------Keyboard-----------------------------
    #    keys = pygame.key.get_pressed()
    #    if keys[pygame.K_SPACE]:
    #----------------------------------------------------------
        #mouse_pos = pygame.mouse.get_pos()
        #hero_rect.colliderect(knight_rect)
        #if hero_rect.collidepoint(mouse_pos):
            #print("collision")
            #print(pygame.mouse.get_pressed())

    #----------------------collision-------------------------------
        game_active = collision(hero_rect,obstacle_rect_list)

        #if knight_rect.colliderect(hero_rect):
        #    knight_rect = knight.get_rect(midbottom=((650, 350)))
        #    knight_rect.inflate_ip(-50,-75)
        #    game_active = False
    #----------------------Game Start / End -----------------------
    else:
         screen.fill("light blue")
         #screen.blit(bg,(0,0))
         screen.blit(hero_intro_scaled,hero_intro_rect)
         hero_rect.midbottom = (100, 400)
         hero_gravity =0

         score_message = test_font.render(f'Your score is {score}', False, 'blue')
         score_message_rect= score_message.get_rect(center = (400,340))
         screen.blit(game_name,game_name_rect)

         if score == 0: screen.blit(game_message,game_message_rect)
         else: screen.blit(score_message,score_message_rect)
         obstacle_rect_list = []

            #pygame.quit()
            #exit()
#------------------------------------------------------------------
    pygame.display.update()
    clock.tick(60)