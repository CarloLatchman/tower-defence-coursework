import pygame
import pygame as pg
import json
import constants as c
from enemy import Enemy
from turret import Turret
from world import World
from button import Button

#initialise pygame
pg.init()

#make a clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("super cool game")

#game variables
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
game_over = False
game_outcome = 0
menu_state = "main menu"
paused = False

#load map
map_image = pg.image.load("levels/final map.png").convert_alpha()

#turret spritesheet
turret_spritesheets = []
for x in range (1, c.MAX_LEVEL + 1):
    turret_sheet = pg.image.load(f"assets/Turrets/turret_{x}.png").convert_alpha()
    turret_spritesheets.append(turret_sheet)
#turret image for cursor
cursor_turret = pg.image.load("assets/turrets/cursor_turret.png").convert_alpha()

#enemies
enemy_images = {
    "low" : pg.image.load("assets/enemy/enemy_1.png").convert_alpha(),
    "medium" : pg.image.load("assets/enemy/enemy_2.png").convert_alpha(),
    "high" : pg.image.load("assets/enemy/enemy_3.png").convert_alpha(),
    "top" : pg.image.load("assets/enemy/enemy_4.png").convert_alpha()
}

#button images
fast_forward_image = pg.image.load("assets/buttons/Fast_Forward_Button.png").convert_alpha()
buy_turret_image = pg.image.load("assets/buttons/Buy_turret_icon.png").convert_alpha()
cancel_button_image = pg.image.load("assets/buttons/cancel button.png").convert_alpha()
upgrade_turret_image = pg.image.load("assets/buttons/Upgrade_button.png").convert_alpha()
begin_image = pg.image.load("assets/buttons/Green_play_button.png").convert_alpha()
restart_image = pg.image.load("assets/buttons/restart.png").convert_alpha()
home_image = pg.image.load("assets/buttons/home_button.png").convert_alpha()
Leader_Board_image = pg.image.load("assets/buttons/Leader_board_button.png").convert_alpha()
Leader_Board_menu_image = pg.image.load("assets/buttons/Leader_board_button_menu.png").convert_alpha()
Controls_image = pg.image.load("assets/buttons/Controls_button.png").convert_alpha()
Play_image = pg.image.load("assets/buttons/Play_button.png").convert_alpha()
Back_image = pg.image.load("assets/buttons/Back_button.png").convert_alpha()
#gui
heart_image = pg.image.load("assets/gui/heart.png").convert_alpha()
coin_image = pg.image.load("assets/gui/coin.png").convert_alpha()

#load sounds
shot_fx = pg.mixer.Sound("assets/sounds/shot.wav")
shot_fx.set_volume(0.5)
music_fx = pg.mixer.Sound("assets/sounds/music.mp3")
music_fx.set_volume(0.03)

#load json waypoints
with open("levels/final map.tmj") as file:
    world_data = json.load(file)

#load text
text_font = pg.font.SysFont("arial", 24, bold = True)
large_font = pg.font.SysFont("arial", 36)

#function to output onscreen text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    pg.draw.rect(screen, "grey0",(c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
    draw_text("LEVEL:  " + str(world.level), text_font, "white", 0, 70)
    screen.blit(heart_image,(0, 0))
    draw_text(str(world.health), text_font, "red", 35, 0)
    screen.blit(coin_image,(0, 35))
    draw_text(str(world.money), text_font, "yellow", 35, 35)

def display_menu():
    global menu_state
    pg.draw.rect(screen, "dark green", (0, 0,c.SCREEN_WIDTH + c.SIDE_PANEL,c.SCREEN_HEIGHT))
    pg.draw.rect(screen, "black", (350, 150, 500, 75))
    pg.draw.rect(screen, "black", (350, 300, 500, 75))
    pg.draw.rect(screen, "black", (350, 450, 500, 100))
    if Leader_Board_button_menu.draw(screen) == True:
        menu_state = "leader board"
    if Controls_button.draw(screen) == True:
        menu_state = "controls"
    if Play_button.draw(screen) == True:
        menu_state = "none"
        return menu_state

def display_controls():
    global menu_state
    pg.draw.rect(screen, "black", (0, 0, c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
    draw_text("MUTE SOUND EFFECTS:     M", large_font, "white", 50, 50)
    draw_text("UNMUTE SOUND EFFECTS:   N", large_font, "white", 50, 100)
    draw_text("PAUSE GAME:             P", large_font, "white", 50, 150)
    if Back_button.draw(screen) == True:
        menu_state = "main menu"

def display_leader_board():
    global menu_state
    pg.draw.rect(screen, "black", (0, 0, c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
    if Back_button.draw(screen) == True:
        menu_state = "main menu"

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    #calculate the number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLUMNS) + mouse_tile_x
    #check if tile is grass or obstacle
    if world.tile_map[mouse_tile_num] == 39 and world.plant_layer[mouse_tile_num] == 0:
        #check there is not already a turret there
        free_space = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                free_space = False
        #if space is free, place turret
        if free_space == True:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)
            #charge for making turret
            world.money -= c.BUY_COST

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False


#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()


#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()


#create buttons
turret_button = Button(c.SCREEN_WIDTH + 10, 10, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 120, 10, cancel_button_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 120, 120, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 280, begin_image, True)
restart_button = Button( 400, 400, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 60, 300, fast_forward_image, False)
home_button = Button( 345, 300, home_image, True)
Leader_Board_button = Button( 250, 407, Leader_Board_image, True)
Play_button = Button( 550, 150, Play_image, True)
Leader_Board_button_menu = Button( 450, 300, Leader_Board_menu_image, True)
Controls_button = Button( 500, 450, Controls_image, True)
Back_button = Button(800, 500, Back_image, True)

#game loop
run = True
while run:
    screen.fill("white")
    clock.tick(c.FPS)
    music_fx.play(99)

    #draw map
    if menu_state == "none":
        world.draw(screen)
        if paused == False:
            #draw buttons
            #if not placing turrets, show turret icon
            if turret_button.draw(screen) == True:
                placing_turrets = True
            #if placing turrets, show cancel
            if paused == False:
                if placing_turrets == True:
                    #show cursor turret
                    cursor_rect = cursor_turret.get_rect()
                    cursor_pos = pg.mouse.get_pos()
                    cursor_rect.center = cursor_pos
                    if cursor_pos[0] <= c.SCREEN_WIDTH:
                        screen.blit(cursor_turret, cursor_rect)
                    if cancel_button.draw(screen) == True:
                        placing_turrets = False
                #if selected, show upgrade button
                if selected_turret:
                    if selected_turret.upgrade_level <c.MAX_LEVEL:
                        if upgrade_button.draw(screen):
                            if world.money >= c.UPGRADE_COST:
                                world.money -= c.UPGRADE_COST
                                selected_turret.upgrade()

            if game_over == False:
                #check if player has lost
                if world.health <= 0:
                    game_over = True
                    game_outcome = -1 #lost
                #check if player has won
                if world.level > c.TOTAL_LEVELS:
                    game_over = True
                    game_outcome = 1 #won


                #update groups
                enemy_group.update(world)
                turret_group.update(enemy_group, world)

                #show selected turret
                if selected_turret:
                    selected_turret.selected = True

            #draw groups
            enemy_group.draw(screen)
            for turret in turret_group:
                turret.draw(screen)

            display_data()
            if game_over == False:
                #check if level started is true
                if level_started == False:
                    if begin_button.draw(screen):
                            level_started = True
                else:
                    #fast forward
                    world.game_speed = 1
                    if fast_forward_button.draw(screen):
                        world.game_speed = 2
                    #spawn enemies
                    if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                        if world.spawned_enemies < len(world.enemy_list):
                            enemy_type = world.enemy_list[world.spawned_enemies]
                            enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                            enemy_group.add(enemy)
                            world.spawned_enemies += 1
                            last_enemy_spawn = pg.time.get_ticks()
            else:
                pg.draw.rect(screen, "#3F48CC", (200, 200, 400, 400), border_radius = 30)
                if game_outcome == -1:
                    draw_text("YOU LOSE", large_font, "grey100", 330,230)
                elif game_outcome == 1:
                    draw_text("YOU WIN", large_font, "grey100", 330,230)
                #home button
                if home_button.draw(screen):
                    game_over = False
                    level_started = False
                    placing_turrets = False
                    selected_turret = None
                    last_enemy_spawn = pg.time.get_ticks()
                    world = World(world_data, map_image)
                    world.process_data()
                    world.process_enemies()
                    # empty groups
                    enemy_group.empty()
                    turret_group.empty()
                    menu_state = "main menu"
                    paused == False
                #leaderboard button
                if Leader_Board_button.draw(screen):
                    paused == False
                    menu_state = "leader board"
                #restart level
                if restart_button.draw(screen):
                    game_over = False
                    level_started = False
                    placing_turrets = False
                    selected_turret = None
                    last_enemy_spawn = pg.time.get_ticks()
                    world = World(world_data, map_image)
                    world.process_data()
                    world.process_enemies()
                    #empty groups
                    enemy_group.empty()
                    turret_group.empty()
                    paused == False

        #check if round ended
        if world.check_level_complete() == True:
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()
            world.money += 200

    elif menu_state == "main menu":
        display_menu()
    elif menu_state == "controls":
        display_controls()
    elif menu_state == "leader board":
        display_leader_board()

    #event handler
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False
        #key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = True
            if event.key == pygame.K_u:
                paused = False
            if event.key == pygame.K_m:
                pygame.mixer.music.pause()
            if event.key == pygame.K_n:
                pygame.mixer.music.unpause()
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #check if mouse is on game window
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                #clear selected turrets
                selected_turret = None
                clear_selection()
                if placing_turrets == True:
                    #check if the player has enough money
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    #update display
    pg.display.flip()
pg.quit()