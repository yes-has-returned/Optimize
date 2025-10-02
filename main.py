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


def ProcessESprite(spritename):
    spritename = "assets/Enemy sprites/" + spritename + ".png"
    returnsprite = pygame.image.load(spritename)
    return returnsprite


picturedict = {
    "Underworks 1-1": ProcessTile("Underworks 1-1"),
    "Underworks 2-1": ProcessTile("Underworks 2-1"),
    "Underworks 3-1": ProcessTile("Underworks 3-1"),
    "Underworks 4-1": ProcessTile("Underworks 4-1"),
    "Underworks 5-1": ProcessTile("Underworks 5-1"),
    "Underworks 1-2": ProcessTile("Underworks 1-2"),
    "Underworks 2-2": ProcessTile("Underworks 2-2"),
    "Underworks 3-2": ProcessTile("Underworks 3-2"),
    "Underworks 4-2": ProcessTile("Underworks 4-2"),
    "Underworks 5-2": ProcessTile("Underworks 5-2"),
}

difficultydict = {
    1: ["Underworks 1-1", "Underworks 1-2"],
    2: ["Underworks 2-1", "Underworks 2-2"],
    3: ["Underworks 3-1", "Underworks 3-2"],
    4: ["Underworks 4-1", "Underworks 4-2"],
    5: ["Underworks 5-1", "Underworks 5-2"],
}

tiledict = {}
for i in difficultydict.keys():
    for j in difficultydict[i]:
        tiledict[j] = i

playerspritedict = {
    "hitbox sprite": ProcessPSprite("Player hitbox"),
    "dash hitbox sprite": ProcessPSprite("Player dash hitbox"),
    "afterimage hitbox sprite": ProcessPSprite("Player dash afterimage hitbox"),
    "player right attack hitbox sprite": ProcessPSprite("Player L_R attack hitbox"),
    "player left attack hitbox sprite": pygame.transform.flip(
        ProcessPSprite("Player L_R attack hitbox"), True, False
    ),
    "player up attack hitbox sprite": ProcessPSprite("Player U_D attack hitbox"),
    "player down attack hitbox sprite": pygame.transform.flip(
        ProcessPSprite("Player U_D attack hitbox"), False, True
    ),
}

dummyspritedict = {
    "hitbox sprite": ProcessESprite("Enemy hitbox"),
    "hurt hitbox sprite": ProcessESprite("Enemy hurt hitbox"),
}


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
    def __init__(self, sprites, gravity):
        self.xcor = 0
        self.ycor = 0
        self.grounded = False
        self.x2d = 0
        self.y2d = 0
        self.sprites = sprites
        self.current_sprite = "hitbox sprite"
        self.vertmomentum = 0
        self.hormomentum = 0
        self.gravity = gravity
        self.jumppower = 35
        self.uprecoilpower = 35
        self.accel = 2
        self.max_speed = 20
        self.dash_speed = 50
        self.dash_speed_decrease = 5
        self.dash_dir = 1
        self.added_speed = 0
        self.dashing = False
        self.dashcooldown = 100
        self.cdashcooldown = 0
        self.prevdashpositions = []
        self.dashafterimagenum = 10
        self.walljump = True
        self.wallrecoil = 0
        self.maxwallrecoil = 10
        self.facing = "right"
        self.attack_pos = None
        self.attack_sprite = "player right hitbox sprite"
        self.attack_cd = 0
        self.max_attack_cd = 30
        self.attack_duration = 0
        self.max_attack_duration = 10

    def move(
        self, keypress, jkeypress, dashpress, attackpress, opress, uprecoil, friction=10
    ):

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
            self.walljump = True
        else:
            self.grounded = False

        # jumping
        if jkeypress == "w":
            self.facing = "up"
            if self.grounded == True:
                self.vertmomentum += self.jumppower
                self.facing = "up"
        elif jkeypress == "s":
            self.facing = "down"

        # left/right movement
        if self.wallrecoil == 0:
            if keypress == "a":
                self.hormomentum -= self.accel
                self.facing = "left"

            elif keypress == "d":
                self.hormomentum += self.accel
                self.facing = "right"

        # alternate U/D choice without jumping
        if opress == "q":
            self.facing = "up"
        elif opress == "e":
            self.facing = "down"

        # attacking
        attackrect = None
        if attackpress == True and self.attack_cd == 0:
            if self.facing == "left":
                self.attack_pos = (self.x2d - 48, self.y2d)
                attackrect = Rectangle(
                    Point(self.x2d - 48, self.y2d), Point(self.x2d, self.y2d + 32)
                )
            elif self.facing == "right":
                self.attack_pos = (self.x2d + 32, self.y2d)
                attackrect = Rectangle(
                    Point(self.x2d + 32, self.y2d), Point(self.x2d + 80, self.y2d + 32)
                )
            elif self.facing == "up":
                self.attack_pos = (self.x2d - 16, self.y2d + 24)
                attackrect = Rectangle(
                    Point(self.x2d - 16, self.y2d + 24),
                    Point(self.x2d + 48, self.y2d + 48),
                )
            elif self.facing == "down":
                self.attack_pos = (self.x2d - 16, self.y2d - 32)
                attackrect = Rectangle(
                    Point(self.x2d - 16, self.y2d - 32), Point(self.x2d + 48, self.y2d)
                )
            self.attack_duration = self.max_attack_duration
            self.attack_cd = self.max_attack_cd
        elif self.attack_duration > 0:
            if self.facing == "left":
                self.attack_pos = (self.x2d - 48, self.y2d)
                attackrect = Rectangle(
                    Point(self.x2d - 48, self.y2d), Point(self.x2d, self.y2d + 32)
                )
            elif self.facing == "right":
                self.attack_pos = (self.x2d + 32, self.y2d)
                attackrect = Rectangle(
                    Point(self.x2d + 32, self.y2d), Point(self.x2d + 80, self.y2d + 32)
                )
            elif self.facing == "up":
                self.attack_pos = (self.x2d - 16, self.y2d + 24)
                attackrect = Rectangle(
                    Point(self.x2d - 16, self.y2d + 24),
                    Point(self.x2d + 48, self.y2d + 48),
                )
            elif self.facing == "down":
                self.attack_pos = (self.x2d - 16, self.y2d - 32)
        else:
            self.attack_pos = None

        # dashing
        if dashpress == True and self.cdashcooldown == 0:
            self.cdashcooldown = self.dashcooldown
            if self.hormomentum < 0:
                self.dash_dir = -1

            elif self.hormomentum > 0:
                self.dash_dir = 1

            self.added_speed = self.added_speed + self.dash_speed

        # wall jump
        if self.x2d < 0 and self.walljump == True and self.y2d > 0:
            self.x2d = 0
            self.hormomentum = self.hormomentum * -1
            self.dash_dir *= -1
            self.vertmomentum = self.jumppower / 1.1
            self.walljump = False
            self.wallrecoil = self.maxwallrecoil
            self.facing = "right"
        elif self.x2d > 1248 and self.walljump == True and self.y2d > 0:
            self.x2d = 1248
            self.hormomentum = self.hormomentum * -1
            self.dash_dir *= -1
            self.vertmomentum = self.jumppower / 1.1
            self.walljump = False
            self.wallrecoil = self.maxwallrecoil
            self.facing = "left"

        # wall collision
        elif self.x2d > 1248:
            self.x2d = 1248
            self.hormomentum = self.hormomentum * -1
            self.dash_dir *= -1
            self.facing = "right"
        elif self.x2d < 0:
            self.x2d = 0
            self.hormomentum = self.hormomentum * -1
            self.dash_dir *= -1
            self.facing = "left"

        # max speed
        if self.hormomentum > self.max_speed:
            self.hormomentum = self.max_speed
        elif self.hormomentum < -self.max_speed:
            self.hormomentum = -self.max_speed

        # cooldown handling
        self.cdashcooldown -= 1
        if self.cdashcooldown < 0:
            self.cdashcooldown = 0

        self.wallrecoil -= 1
        if self.wallrecoil < 0:
            self.wallrecoil = 0

        self.attack_cd -= 1
        if self.attack_cd < 0:
            self.attack_cd = 0

        self.attack_duration -= 1
        if self.attack_duration < 0:
            self.attack_duration = 0

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

        # attack sprite handling
        self.attack_sprite = f"player {self.facing} attack hitbox sprite"

        # pogo
        if uprecoil == True:
            self.vertmomentum += self.uprecoilpower

        return attackrect


class Enemy:
    def __init__(self, xcor, ycor, spritedict, gravity):
        self.xcor = xcor
        self.ycor = ycor
        self.spritedict = spritedict
        self.hormomentum = 0
        self.vertmomentum = 0
        self.current_sprite = "hitbox sprite"
        self.staggeramountmain = 10
        self.staggeramountsecondary = 40
        self.staggeramountvert = 20
        self.grounded = True
        self.gravity = gravity
        self.hurttimer = 0
        self.maxhurttimer = 10
        self.hitbox = Rectangle(Point(xcor, ycor), Point(xcor + 32, ycor + 32))

    def move(self, hitdir, attackrect, friction=10):
        self.hitbox = Rectangle(
            Point(self.xcor, self.ycor), Point(self.xcor + 32, self.ycor + 32)
        )
        if attackrect != None:
            if self.hitbox.intersects(attackrect):
                pass
            else:
                hitdir = None
        else:
            hitdir = None
        # movement
        print(self.vertmomentum)
        self.xcor += self.hormomentum
        self.ycor += self.vertmomentum

        # friction
        if self.grounded == True:
            self.hormomentum = self.hormomentum * (100 - friction) / 100
            self.vertmomentum = 0

        # gravity
        self.vertmomentum -= self.gravity

        # ground collision
        if self.ycor <= 0:
            self.ycor = 0
            self.grounded = True
        else:
            self.grounded = False

        # hit recoil
        if hitdir != None:
            if hitdir == "left":
                self.hormomentum += -self.staggeramountmain
                self.vertmomentum += self.staggeramountsecondary
            elif hitdir == "right":
                self.hormomentum += self.staggeramountmain
                self.vertmomentum += self.staggeramountsecondary
            elif hitdir == "up":
                self.vertmomentum += self.staggeramountvert
                self.grounded = False
            elif hitdir == "down":
                self.vertmomentum += -self.staggeramountvert
            self.hurttimer = self.maxhurttimer

        # wall collision
        if self.xcor > 1248:
            self.xcor = 1248
            self.hormomentum = self.hormomentum * -1
        elif self.xcor < 0:
            self.xcor = 0
            self.hormomentum = self.hormomentum * -1

        # sprite handling
        if self.hurttimer > 0:
            self.current_sprite = "hurt hitbox sprite"
        else:
            self.current_sprite = "hitbox sprite"

        self.hurttimer -= 1
        if self.hurttimer < 0:
            self.hurttimer = 0
        if hitdir == "down":
            return True
        else:
            return False


gravity = 2.5
running = True
testing_mode = "battling" #battling or navigation
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
M = Gmap(picturedict, "Underworks 1-1", difficultydict, tiledict)
P = Player(playerspritedict, gravity)
uprecoil = False
dummy1 = Enemy(100, 0, dummyspritedict, gravity)
time_stop = True
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
        screen.blit(
            dummy1.spritedict[dummy1.current_sprite], (dummy1.xcor, 688 - dummy1.ycor)
        )
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        keypress = ""
        jkeypress = ""
        opress = ""
        dashpress = False
        attackpress = False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            jkeypress = "w"

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            jkeypress = "s"

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            keypress = "d"

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            keypress = "a"

        if keys[pygame.K_SPACE] == True:
            dashpress = True

        if keys[pygame.K_q] == True:
            opress = "q"

        elif keys[pygame.K_e] == True:
            opress = "e"

        if mouse[0] == True:
            attackpress = True

        attackrect = P.move(
            keypress, jkeypress, dashpress, attackpress, opress, uprecoil
        )
        uprecoil = dummy1.move(P.facing, attackrect)

        if P.attack_pos != None:
            screen.blit(
                P.sprites[P.attack_sprite], (P.attack_pos[0], 688 - P.attack_pos[1])
            )

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                not_clicked = False

    sleep(0.01)
