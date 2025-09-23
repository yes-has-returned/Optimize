import random
import pygame
from os import system
from time import sleep
import math

pygame.init()
events = pygame.event.get()
screen = pygame.display.set_mode((1280, 720))


def ProcessTile(tilename):
    tilename = "assets/Tile art/" + tilename + ".png"
    returntile = pygame.transform.scale_by(pygame.image.load(tilename), 3)
    return returntile


def ProcessPSprite(spritename):
    spritename = "assets/Player sprites/" + spritename + ".png"
    returnsprite = pygame.image.load(spritename)
    return returnsprite


picturedict = {
    "Underworks 1-1": ProcessTile("Underworks 1-1"),
    "Underworks 2-1": ProcessTile("Underworks 2-1"),
    "Underworks 3-1": ProcessTile("Underworks 3-1"),
    "Underworks 4-1": ProcessTile("Underworks 4-1"),
    "Underworks 5-1": ProcessTile("Underworks 5-1"),
}

difficultydict = {
    1: ["Underworks 1-1"],
    2: ["Underworks 2-1"],
    3: ["Underworks 3-1"],
    4: ["Underworks 4-1"],
    5: ["Underworks 5-1"],
}

tiledict = {}
for i in difficultydict.keys():
    for j in difficultydict[i]:
        tiledict[j] = i

playerspritedict = {
    "hitbox sprite": ProcessPSprite("Player hitbox"),
    "dash hitbox sprite": ProcessPSprite("Player dash hitbox"),
    "afterimage hitbox sprite": ProcessPSprite("Player dash afterimage hitbox"),
}


class Gmap:
    def __init__(self, picturedict, starttile, difficultydict, tiledict):
        self.picturedict = picturedict
        self.gamemap = {(0, 0): starttile}
        self.difficultydict = difficultydict
        self.tiledict = tiledict
        self.levelname = "Underworks"
        self.move_player(0, 0)

    def move_player(self, xcor, ycor):
        for i in [xcor, xcor - 1, xcor + 1]:
            for j in [ycor, ycor - 1, ycor + 1]:
                if (i, j) not in self.gamemap:
                    self.load_tile((i, j))

    def load_tile(self, tile_coordinates):
        possibilities = []
        for i in [
            tile_coordinates[0],
            tile_coordinates[0] + 1,
            tile_coordinates[0] - 1,
        ]:
            for j in [
                tile_coordinates[1],
                tile_coordinates[1] + 1,
                tile_coordinates[1] - 1,
            ]:
                if (i, j) in self.gamemap.keys():
                    possibilities.append(self.tiledict[self.gamemap[(i, j)]])
                    if self.tiledict[self.gamemap[(i, j)]] + 1 <= max(
                        list(self.difficultydict.keys())
                    ):
                        possibilities.append(self.tiledict[self.gamemap[(i, j)]] + 1)
                    if self.tiledict[self.gamemap[(i, j)]] - 1 >= min(
                        list(self.difficultydict.keys())
                    ):
                        possibilities.append(self.tiledict[self.gamemap[(i, j)]] - 1)

        loaded_tile_difficulty = random.choice(possibilities)
        loaded_tile_possibilities = []
        for i in difficultydict[loaded_tile_difficulty]:
            if self.levelname in i:
                loaded_tile_possibilities.append(i)

        self.gamemap[tile_coordinates] = random.choice(loaded_tile_possibilities)

    def GenerateMap(self, playerx, playery):
        todolist = []
        for i in self.gamemap.keys():
            tilex = i[0]
            tiley = i[1]
            tile = self.gamemap[i]
            if tilex == playerx and tiley == playery:
                todolist.append([tile, 640, 360, 0, 0])

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
                temp = [tile, 640 + addedx, 360 + addedy]
                todolist.append(temp)
        todolist.sort(key=lambda x: x[2])
        return todolist


class Player:
    def __init__(self, sprites):
        self.xcor = 0
        self.ycor = 0
        self.grounded = False
        self.x2d = 0
        self.y2d = 0
        self.sprites = sprites
        self.current_sprite = "hitbox sprite"
        self.vertmomentum = 0
        self.hormomentum = 0
        self.gravity = 5
        self.jumppower = 50
        self.accel = 5
        self.max_speed = 20
        self.dash_speed = 100
        self.dash_speed_decrease = 10
        self.dash_dir = 1
        self.added_speed = 0
        self.dashing = False
        self.dashcooldown = 100
        self.cdashcooldown = 0
        self.prevdashpositions = []
        self.dashafterimagenum = 10

    def move(self, keypress, jkeypress, dashpress, friction=20):
        print(self.cdashcooldown)

        # changing player position
        self.x2d = self.hormomentum + self.added_speed * self.dash_dir + self.x2d
        self.y2d += self.vertmomentum

        # friction
        if self.grounded == True:
            self.hormomentum = self.hormomentum * (100 - friction) / 100

        # gravity
        if self.dashing == True:
            self.vertmomentum = 0
        self.vertmomentum = self.vertmomentum - self.gravity

        # dash wears off
        if self.added_speed > 0:
            self.dashing = True
            self.added_speed -= self.dash_speed_decrease
        if self.added_speed <= 0:
            self.dashing = False
            self.added_speed = 0

        # floor collision
        if self.y2d <= 0:
            self.y2d = 0
            self.vertmomentum = 0
            self.grounded = True
        else:
            self.grounded = False

        # jumping
        if self.grounded == True:
            if jkeypress == "w":
                self.vertmomentum += self.jumppower

        # left/right movement
        if keypress == "a":
            self.hormomentum -= self.accel

        elif keypress == "d":
            self.hormomentum += self.accel

        # dashing
        if dashpress == True and self.cdashcooldown == 0:
            self.cdashcooldown = self.dashcooldown
            if self.hormomentum < 0:
                self.dash_dir = -1

            elif self.hormomentum > 0:
                self.dash_dir = 1

            self.added_speed = self.added_speed + self.dash_speed

        # wall collision
        if self.x2d < 0:
            self.x2d = 0
            self.hormomentum = self.hormomentum * -1
            self.dash_dir *= -1
        elif self.x2d > 1248:
            self.x2d = 1248
            self.hormomentum = self.hormomentum * -1
            self.dash_dir *= -1

        # max speed
        if self.hormomentum > self.max_speed:
            self.hormomentum = self.max_speed
        elif self.hormomentum < -self.max_speed:
            self.hormomentum = -self.max_speed

        # dash cooldown handling
        self.cdashcooldown -= 1
        if self.cdashcooldown < 0:
            self.cdashcooldown = 0

        # sprite handling
        if self.dashing == True:
            self.current_sprite = "dash hitbox sprite"
        else:
            self.current_sprite = "hitbox sprite"

        # dash afterimage handling
        if self.dashing == True:
            self.prevdashpositions.append((self.x2d, self.y2d))
            if len(self.prevdashpositions) > self.dashafterimagenum:
                self.prevdashpositions.pop(-1)
        elif self.dashing == False:
            self.prevdashpositions = []


running = True
testing_mode = "battling"
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
M = Gmap(picturedict, "Underworks 1-1", difficultydict, tiledict)
P = Player(playerspritedict)
while running:
    if testing_mode == "navigation":
        t = M.GenerateMap(P.xcor, P.ycor)
        for i in t:
            screen.blit(picturedict[i[0]], (i[1], i[2]))
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

    elif testing_mode == "battling":
        screen.fill(white)
        if P.prevdashpositions != []:
            for i in P.prevdashpositions:
                screen.blit(P.sprites["afterimage hitbox sprite"], (i[0], 688 - i[1]))
        screen.blit(P.sprites[P.current_sprite], (P.x2d, 688 - P.y2d))
        keys = pygame.key.get_pressed()
        keypress = ""
        jkeypress = ""
        dashpress = False
        if keys[pygame.K_w] == True:
            jkeypress = "w"

        elif keys[pygame.K_s] == True:
            jkeypress = "s"

        if keys[pygame.K_d] == True:
            keypress = "d"

        elif keys[pygame.K_a] == True:
            keypress = "a"

        if keys[pygame.K_SPACE] == True:
            dashpress = True

        P.move(keypress, jkeypress, dashpress)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                not_clicked = False

    sleep(0.01)
