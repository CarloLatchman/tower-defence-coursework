import pygame as pg
from pygame.math import Vector2
import math
class Enemy(pg.sprite.Sprite): #sprite class to reduce bloat
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = 0
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.waypoints = waypoints
        self.speed = 5
        self.pos = self.waypoints[0]
        self.target_waypoint = 1
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        #define target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #enemy has reached the end of the path
            self.kill()
        #calculate distance to target
        dist = self.movement.length()
        #check if dist > speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1


    def rotate(self):
        #calculate dist to next waypoint
        dist = self.target - self.pos
        #use dist to calculate angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        #rotate the sprite and update the rectangle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos