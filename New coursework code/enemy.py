import pygame as pg
from pygame.math import Vector2
import math
from enemy_data import ENEMY_DATA
import constants as c
class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        #to change the speed of each enemy
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        if self.target_waypoint <len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #enemy reaches the end
            self.kill()
            world.health -= 1
            world.missed_enemies += 1

        #find the distance to the target waypoint
        distance = self.movement.length()
        if distance >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize()*(self.speed * world.game_speed)
        else:
            if distance != 0:
                self.pos += self.movement.normalize() * distance
            self.target_waypoint += 1

    def rotate(self):
        #calculate the distance to the next waypoint
        distance = self.target - self.pos
        #calculate the rotation angle
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
        #rotate image and update rectangle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()