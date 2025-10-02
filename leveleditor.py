import pygame
from os import system
from time import sleep
import math

pygame.init()
screen = pygame.display.set_mode((320, 640))
white = pygame.Color(255, 255, 255)
desiredlevel = "underworks 1-1"


class Point:
    def __init__(self, xcoord=0, ycoord=0):
        self.x = xcoord
        self.y = ycoord


class Rectangle:
    def __init__(self, bottom_left, top_right):
        self.bottom_left = bottom_left
        self.top_right = top_right

    def intersects(self, other):
        return not (
            self.top_right.x < other.bottom_left.x
            or self.bottom_left.x > other.top_right.x
            or self.top_right.y < other.bottom_left.y
            or self.bottom_left.y > other.top_right.y
        )
    
    def inside(self, point):
        return (
            self.top_right.x > point.x > self.bottom_left.x and
            self.top_right.y > point.y > self.bottom_left.y
        )


def RenderComponentSpritesheet(component_name):
    component_name = "assets/Level assets/" + component_name + ".png"
    returnsprite = pygame.transform.scale_by(pygame.image.load(component_name), 0.25)
    return returnsprite

desiredlevelcomponentlist = open(f"levels/{desiredlevel}.txt", "r").read().split("\n")
desiredlevelcomponentlist = [[i.split(":")[0], (i.split(":")[1].split(",")[0], i.split(":")[1].split(",")[1])] for i in desiredlevelcomponentlist]
print(desiredlevelcomponentlist)


while True:
    mousex, mousey = pygame.mouse.get_pos()
    screen.fill(white)
    for i in desiredlevelcomponentlist:
        screen.blit(RenderComponentSpritesheet(i[0]), (int(i[1][0])*0.25,640-int(i[1][1])*0.25))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            not_clicked = False