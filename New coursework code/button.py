import pygame as pg
import PIL

class Button():
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):

        action = False
        #draw button
        surface.blit(self.image, self.rect)

        #get mouse pos
        pos = pg.mouse.get_pos()

        #check if mouseover or clicked
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                if self.single_click:
                    self.clicked = True

                return action

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
            return action

