
import random
import pygame
from os import system
from time import sleep
import math


pygame.init()
events = pygame.event.get()
screen = pygame.display.set_mode((1280, 720))

def ProcessTile(tilename):
    tilename = "Tile art/" + tilename + ".png"
    returntile = pygame.transform.scale_by(pygame.image.load(tilename),3)
    return returntile

picturedict = {
    "Underworks 1":ProcessTile("Underworks 1-1"),
    "Underworks 2":ProcessTile("Underworks 2-1"),
    "Underworks 3":ProcessTile("Underworks 3-1"),
    "Underworks 4":ProcessTile("Underworks 4-1"),
    "Underworks 5":ProcessTile("Underworks 5-1"),
}

difficultydict = {
    1:["Underworks 1"],
    2:["Underworks 2"],
    3:["Underworks 3"],
    4:["Underworks 4"],
    5:["Underworks 5"],
}

tiledict = {
    "Underworks 1":1,
    "Underworks 2":2,
    "Underworks 3":3,
    "Underworks 4":4,
    "Underworks 5":5,
}

class Gmap:
    def __init__(self, picturedict, starttile, difficultydict, tiledict):
        self.picturedict = picturedict
        self.gamemap = {(0,0):starttile}
        self.difficultydict = difficultydict
        self.tiledict = tiledict
        self.levelname = "Underworks"
        self.move_player(0,0)

    def move_player(self, xcor, ycor):
        for i in [xcor, xcor-1, xcor+1]:
            for j in [ycor, ycor-1, ycor+1]:
                if (i,j) not in self.gamemap:
                    self.load_tile((i,j))

    def load_tile(self, tile_coordinates):
        possibilities = []
        for i in [tile_coordinates[0], tile_coordinates[0]+1, tile_coordinates[0]-1]:
            for j in [tile_coordinates[1], tile_coordinates[1]+1, tile_coordinates[1]-1]:
                if (i,j) in self.gamemap.keys():
                    possibilities.append(self.tiledict[self.gamemap[(i,j)]])
                    if self.tiledict[self.gamemap[(i,j)]]+1 <= max(list(self.difficultydict.keys())):
                        possibilities.append(self.tiledict[self.gamemap[(i,j)]]+1)
                    if self.tiledict[self.gamemap[(i,j)]]-1 >= min(list(self.difficultydict.keys())):
                        possibilities.append(self.tiledict[self.gamemap[(i,j)]]-1)

        loaded_tile_difficulty = random.choice(possibilities)
        loaded_tile_possibilities = []
        for i in difficultydict[loaded_tile_difficulty]:
            if self.levelname in i:
                loaded_tile_possibilities.append(i)
        
        self.gamemap[tile_coordinates] = random.choice(loaded_tile_possibilities)

    def GenerateMap(self,playerx,playery):
        todolist = []
        for i in self.gamemap.keys():
            tilex = i[0]
            tiley = i[1]
            tile = self.gamemap[i]
            if tilex == playerx and tiley == playery:
                todolist.append([tile,640,360,0,0])
            
            else:
                addedy = 0
                addedx = 0
                tempx = tilex
                tempy = tiley
                if tilex > playerx:
                    while tempx > playerx:
                        addedx += 60
                        addedy += 30
                        tempx -= 1


                elif tilex < playerx:
                    while tempx < playerx:
                        addedx -= 60
                        addedy -= 30
                        tempx += 1


                if tiley > playery:
                    while tempy > playery:
                        addedx -= 60
                        addedy += 30
                        tempy -= 1

                elif tiley < playery:
                    while tempy < playery:
                        addedx += 60
                        addedy -= 30
                        tempy += 1
                temp = [tile,640+addedx,360+addedy]
                todolist.append(temp)
        todolist.sort(key = lambda x:x[2])
        return todolist

class Player:
    def __init__(self):
        self.xcor = 0
        self.ycor = 0

running = True
black = pygame.Color(0,0,0)
M = Gmap(picturedict, "Underworks 1", difficultydict, tiledict)
P = Player()
while running:
    t = M.GenerateMap(P.xcor, P.ycor)
    for i in t:
        screen.blit(picturedict[i[0]],(i[1],i[2]))
    pygame.display.update()
    screen.fill(black)
    pygame.event.pump()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] == True:
        P.ycor -= 1

    elif keys[pygame.K_s] == True:
        P.ycor += 1
    
    elif keys[pygame.K_d] == True:
        P.xcor += 1

    elif keys[pygame.K_a] == True:
        P.xcor -= 1

    M.move_player(P.xcor, P.ycor)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            not_clicked = False
