import pygame as pg
from enemy import Enemy
from world import World
import constants as c

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

#load images
#map
map_image = pg.image.load("levels/grass_map.png").convert_alpha()
#enemies
enemy_image = pg.image.load("assets/images/enemies/enemy_1.png").convert_alpha()

#create world
world = World(map_image)

#create groups of enemies
enemy_group = pg.sprite.Group()

waypoints = [
  (100, 100),
  (1200, 600),
  (500, 700),
  (200, 500)
]

enemy = Enemy(waypoints,enemy_image)
enemy_group.add(enemy)


#game loop
run = True
while run:

  clock.tick(c.FPS)

  screen.fill("grey100")

  #draw level
  world.draw(screen)

  #draw enemy path
  pg.draw.lines(screen, "grey0", False, waypoints)

  #update groups
  enemy_group.update()

  #draw groups
  enemy_group.draw(screen)

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False

  #update display
  pg.display.flip()

pg.quit()