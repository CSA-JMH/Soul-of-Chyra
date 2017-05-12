#Joshua Hinojosa
#Mr.Davis
#5/7/17
#Adv. Comp. Programming
#The Soul of Chyra
#v1.0

'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>

An exciting adventure/dungeon combat game where a player is challenged to
survive through a long dungeon to escape while defeating enemies along the way.


VERSION 1.0 Update Details:
The game is now completed. The game now has saving and loading. Stage 3 has been added as the final stage. The final boss has also been added.
The inventory now shows ALL of the player's stats. A game win screen has also been added which runs when a player has beaten the final boss.'''

import pygame, sys, random, time
from pygame.locals import *
pygame.init()

#####################BUTTON CLASSES################################################################
class Option:           #Creates class for hovering over the option buttons
    hovered = False

    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:            #if mouse is hovered then the color changes
            return (155, 155, 155)
        else:
            return (195, 195, 195)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
pygame.init()
menu_font = pygame.font.Font(None, 72)      #sets the font type and size for buttons
######################################SAVING AND LOADING MECHANICS#######################################################################################################################################################################################################################################################
def savegame(): #saves players place in the game along with the player's stats to a txt file
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain
    savefile = open("playersaves.txt", "w")
    heroinv=",".join(heroinventory)
    data = "Hero Class : " + hero.pclass + " : Max HP : " + str(hero.maxhp) + " : HP : " + str(herohp) + " : Attack : " +  str(hero.attack)+ " : LVL : "+ str(playerlvl) + " : XP : " + str(heroexp)+ " : Stage : " + str(stage) + " : Enemies Defeated : " + str(enemiesdefeated) + " : Inventory : " + str(heroinv) + " : Weapon Equipped : " + str(hero.weapon)+ " : Weapon Stats : " + str(weaponstats)
    savefile.write(data)
    savefile.close()

def loadgame(): #gets player's last save along with all of the player's stats
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain, stage
    try:
        loadfile= open("playersaves.txt", "r")
        line=loadfile.readline()
        data=line.split(" : ")
        if data[1]== "Warrior":
            hero=Warrior()
        elif data[1]== "Mage":
            hero=Mage()
        elif data[1]== "Juggernaut":
            hero=Juggernaut()
        loadfile.close()
        hero.maxhp= int(data[3])
        herohp= data[5]
        hero.attack=int(data[7])
        playerlvl=data[9]
        heroexp=data[11]
        enemiesdefeated=int(data[15])
        heroinventory= data[17]. split(",")
        hero.weapon=data[19]
        weaponstats=data[21]
        stage=data[13]
        if stage == '0':
            startgame()
        elif stage== '1':
            room_no_enemy()
        elif stage == '2':
            room_no_enemy()
        elif stage == '3':
            room_no_enemy()
        elif stage == 'boss1':
            boss1()
        elif stage == 'boss2':
            boss2()
        elif stage == 'boss3':
            boss3()
        loadfile.close()
    except FileNotFoundError:
        pass
######################################LEVELING UP MECHANICS###########################################################################################################################################
def lvl_up():  # player level up function- lets a player choose an attribute to increase once a certain amount of xp is earned
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain, attackhit_fx
    level_up_IMG=pygame.image.load('level_up_img.png')
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    if int(playerlvl)== 1:
        if int(heroexp) >= 14:
            playerlvl = str(int(playerlvl) + 1)
            heroexp = str(int(heroexp) - 14)
            pygame.mixer.music.load('Victory.ogg')
            pygame.mixer.music.play()
            while True:
                screen.fill(BLACK)
                screen.blit(level_up_IMG, (-150, -100))
                AttacktBTN = [Option("Attack", (150, 500))]
                HPBTN = [Option("Health", (300, 500))]
                for option1 in AttacktBTN:  # check to see if the quit button is hovered by mouse
                    if option1.rect.collidepoint(pygame.mouse.get_pos()):
                        option1.hovered = True
                    else:
                        option1.hovered = False
                    option1.draw()
                for option2 in HPBTN:  # check to see if the save button is hovered by mouse
                    if option2.rect.collidepoint(pygame.mouse.get_pos()):
                        option2.hovered = True
                    else:
                        option2.hovered = False
                    option2.draw()
                stats_title_tx=font1.render(" Class         HP           Attack", 10, WHITE)
                stats_txt= font1.render(str(hero.pclass) + "        " + str(hero.hp) + "            " + str(hero.attack), 10, WHITE)
                attribute_q_txt= font1.render("Which attribute would you like to increase?", 10, WHITE)
                screen.blit(stats_title_tx,(100, 300))
                screen.blit(stats_txt, (100, 340))
                screen.blit(attribute_q_txt,(75, 400))
                for event in pygame.event.get():  # event handling loop
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if option1.hovered == True:  # if the player selects the New Game
                            hero.attack = hero.attack + 1
                            increased_stat_txt= font1. render("Player attack increased by 1!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            pygame.display.flip()
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                        elif option2.hovered == True:
                            hero.maxhp = hero.maxhp + 10
                            increased_stat_txt = font1.render("Player max health increased by 10!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            pygame.display.flip()
                            hero.hp = hero.maxhp
                            herohp=str(hero.hp)
                            time.sleep(2)
                            randomitem()
                pygame.display.flip()
                clock.tick(60)

    elif int(playerlvl) == 2:
        if int(heroexp) >= 40:
            playerlvl = str(int(playerlvl) + 1)
            heroexp = str(int(heroexp) - 40)
            pygame.mixer.music.load('Victory.ogg')
            pygame.mixer.music.play()
            while True:
                screen.fill(BLACK)
                screen.blit(level_up_IMG, (-150, -100))
                AttacktBTN = [Option("Attack", (150, 500))]
                HPBTN = [Option("Health", (300, 500))]
                for option1 in AttacktBTN:  # check to see if the quit button is hovered by mouse
                    if option1.rect.collidepoint(pygame.mouse.get_pos()):
                        option1.hovered = True
                    else:
                        option1.hovered = False
                    option1.draw()
                for option2 in HPBTN:  # check to see if the save button is hovered by mouse
                    if option2.rect.collidepoint(pygame.mouse.get_pos()):
                        option2.hovered = True
                    else:
                        option2.hovered = False
                    option2.draw()

                stats_title_tx=font1.render(" Class    HP    Attack", 10, WHITE)
                stats_txt= font1.render(str(hero.pclass) + "    " + str(hero.hp) + "    " + str(hero.attack), 10, WHITE)
                attribute_q_txt= font1.render("Which attribute would you like to increase?", 10, WHITE)
                screen.blit(stats_title_tx, (100, 300))
                screen.blit(stats_txt, (100, 340))
                screen.blit(attribute_q_txt, (75, 400))
                for event in pygame.event.get():  # event handling loop
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if option1.hovered == True:  # if the player selects the New Game
                            hero.attack = hero.attack + 1
                            increased_stat_txt= font1. render("Player attack increased by 1!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            pygame.display.flip()
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                        elif option2.hovered == True:
                            hero.maxhp = hero.maxhp + 10
                            increased_stat_txt = font1.render("Player max health increased by 10!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            pygame.display.flip()
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                pygame.display.flip()
                clock.tick(60)
    elif int(playerlvl) == 3:
        if int(heroexp) >= 65:
            playerlvl = str(int(playerlvl) + 1)
            heroexp = str(int(heroexp) - 65)
            pygame.mixer.music.load('Victory.ogg')
            pygame.mixer.music.play()
            while True:
                screen.fill(BLACK)
                screen.blit(level_up_IMG, (-150, -100))
                AttacktBTN = [Option("Attack", (150, 500))]
                HPBTN = [Option("Health", (300, 500))]
                for option1 in AttacktBTN:  # check to see if the quit button is hovered by mouse
                    if option1.rect.collidepoint(pygame.mouse.get_pos()):
                        option1.hovered = True
                    else:
                        option1.hovered = False
                    option1.draw()
                for option2 in HPBTN:  # check to see if the save button is hovered by mouse
                    if option2.rect.collidepoint(pygame.mouse.get_pos()):
                        option2.hovered = True
                    else:
                        option2.hovered = False
                    option2.draw()

                stats_title_tx=font1.render(" Class    HP    Attack", 10, WHITE)
                stats_txt= font1.render(str(hero.pclass) + "    " + str(hero.hp) + "    " + str(hero.attack), 10, WHITE)
                attribute_q_txt= font1.render("Which attribute would you like to increase?", 10, WHITE)
                screen.blit(stats_title_tx, (100, 300))
                screen.blit(stats_txt, (100, 340))
                screen.blit(attribute_q_txt, (75, 400))
                for event in pygame.event.get():  # event handling loop
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if option1.hovered == True:  # if the player selects the New Game
                            hero.attack = hero.attack + 1
                            increased_stat_txt= font1. render("Player attack increased by 1!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                        elif option2.hovered == True:
                            hero.maxhp = hero.maxhp + 10
                            increased_stat_txt = font1.render("Player max health increased by 10!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                pygame.display.flip()
                clock.tick(60)
    elif int(playerlvl) == 4:
        if int(heroexp) >= 100:
            playerlvl = str(int(playerlvl) + 1)
            heroexp = str(int(heroexp) - 100)
            pygame.mixer.music.load('Victory.ogg')
            pygame.mixer.music.play()
            while True:
                screen.fill(BLACK)
                screen.blit(level_up_IMG, (-150, -100))
                AttacktBTN = [Option("Attack", (150, 500))]
                HPBTN = [Option("Health", (300, 500))]
                for option1 in AttacktBTN:  # check to see if the quit button is hovered by mouse
                    if option1.rect.collidepoint(pygame.mouse.get_pos()):
                        option1.hovered = True
                    else:
                        option1.hovered = False
                    option1.draw()
                for option2 in HPBTN:  # check to see if the save button is hovered by mouse
                    if option2.rect.collidepoint(pygame.mouse.get_pos()):
                        option2.hovered = True
                    else:
                        option2.hovered = False
                    option2.draw()

                stats_title_tx=font1.render(" Class    HP    Attack", 10, WHITE)
                stats_txt= font1.render(str(hero.pclass) + "    " + str(hero.hp) + "    " + str(hero.attack), 10, WHITE)
                attribute_q_txt= font1.render("Which attribute would you like to increase?", 10, WHITE)
                screen.blit(stats_title_tx, (100, 300))
                screen.blit(stats_txt, (100, 340))
                screen.blit(attribute_q_txt, (75, 400))
                for event in pygame.event.get():  # event handling loop
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if option1.hovered == True:  # if the player selects the New Game
                            hero.attack = hero.attack + 1
                            increased_stat_txt= font1. render("Player attack increased by 1!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                        elif option2.hovered == True:
                            hero.maxhp = hero.maxhp + 10
                            increased_stat_txt = font1.render("Player max health increased by 10!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                pygame.display.flip()
                clock.tick(60)

    elif int(playerlvl) == 5:
        if int(heroexp) >= 120:
            playerlvl = str(int(playerlvl) + 1)
            heroexp = str(int(heroexp) - 120)
            pygame.mixer.music.load('Victory.ogg')
            pygame.mixer.music.play()
            while True:
                screen.fill(BLACK)
                screen.blit(level_up_IMG, (-150, -100))
                AttacktBTN = [Option("Attack", (150, 500))]
                HPBTN = [Option("Health", (300, 500))]
                for option1 in AttacktBTN:  # check to see if the quit button is hovered by mouse
                    if option1.rect.collidepoint(pygame.mouse.get_pos()):
                        option1.hovered = True
                    else:
                        option1.hovered = False
                    option1.draw()
                for option2 in HPBTN:  # check to see if the save button is hovered by mouse
                    if option2.rect.collidepoint(pygame.mouse.get_pos()):
                        option2.hovered = True
                    else:
                        option2.hovered = False
                    option2.draw()

                stats_title_tx = font1.render(" Class    HP    Attack", 10, WHITE)
                stats_txt = font1.render(str(hero.pclass) + "    " + str(hero.hp) + "    " + str(hero.attack), 10,
                                         WHITE)
                attribute_q_txt = font1.render("Which attribute would you like to increase?", 10, WHITE)
                screen.blit(stats_title_tx, (100, 300))
                screen.blit(stats_txt, (100, 340))
                screen.blit(attribute_q_txt, (75, 400))
                for event in pygame.event.get():  # event handling loop
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if option1.hovered == True:  # if the player selects the New Game
                            hero.attack = hero.attack + 1
                            increased_stat_txt = font1.render("Player attack increased by 1!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                        elif option2.hovered == True:
                            hero.maxhp = hero.maxhp + 10
                            increased_stat_txt = font1.render("Player max health increased by 10!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                pygame.display.flip()
                clock.tick(60)
    elif int(playerlvl) == 6:
        if int(heroexp) >= 240:
            playerlvl = str(int(playerlvl) + 1)
            heroexp = str(int(heroexp) - 240)
            pygame.mixer.music.load('Victory.ogg')
            pygame.mixer.music.play()
            while True:
                screen.fill(BLACK)
                screen.blit(level_up_IMG, (-150, -100))
                AttacktBTN = [Option("Attack", (150, 500))]
                HPBTN = [Option("Health", (300, 500))]
                for option1 in AttacktBTN:  # check to see if the quit button is hovered by mouse
                    if option1.rect.collidepoint(pygame.mouse.get_pos()):
                        option1.hovered = True
                    else:
                        option1.hovered = False
                    option1.draw()
                for option2 in HPBTN:  # check to see if the save button is hovered by mouse
                    if option2.rect.collidepoint(pygame.mouse.get_pos()):
                        option2.hovered = True
                    else:
                        option2.hovered = False
                    option2.draw()

                stats_title_tx = font1.render(" Class    HP    Attack", 10, WHITE)
                stats_txt = font1.render(str(hero.pclass) + "    " + str(hero.hp) + "    " + str(hero.attack), 10,
                                         WHITE)
                attribute_q_txt = font1.render("Which attribute would you like to increase?", 10, WHITE)
                screen.blit(stats_title_tx, (100, 300))
                screen.blit(stats_txt, (100, 340))
                screen.blit(attribute_q_txt, (75, 400))
                for event in pygame.event.get():  # event handling loop
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if option1.hovered == True:  # if the player selects the New Game
                            hero.attack = hero.attack + 1
                            increased_stat_txt = font1.render("Player attack increased by 1!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                        elif option2.hovered == True:
                            hero.maxhp = hero.maxhp + 10
                            increased_stat_txt = font1.render("Player max health increased by 10!", 10, WHITE)
                            screen.blit(increased_stat_txt, (100, 600))
                            hero.hp = hero.maxhp
                            herohp = str(hero.hp)
                            time.sleep(2)
                            randomitem()
                pygame.display.flip()
                clock.tick(60)
##############################################HERO DEATH#################################################
def herodeath():  # when a player's health reaches 0 the player dies and the player's
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, background, weaponstats, hpgain
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    backgrndImg = pygame.image.load('Brick-Background.png')
    backgrndImg = pygame.transform.scale(backgrndImg, (600, 900))
    font3=pygame.font.SysFont("monospace", 56)
    RED=(255, 0, 0)
    pygame.mixer.music.load('game_over.wav')
    pygame.mixer.music.play(-1, 0)
    while True:
        screen.blit(backgrndImg, (0,0))
        gameover_txt = font3.render("GAME OVER", 10, RED)
        screen.blit(gameover_txt, (175, 300))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(10)
        menu()
##############################GAME WIN SCREEN#############################################
def endingscreen():
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, background, weaponstats, hpgain
    font3 = pygame.font.SysFont("monospace", 24)
    BLACK = (0, 0, 0)
    pygame.mixer.music.load('Gamewin.ogg')
    pygame.mixer.music.play()
    while True:
        screen.fill(BLACK)
        gameover_txt1 = font3.render("You defeated the final boss! ",10, WHITE)
        gameover_txt2 = font3.render("He dropped a key to a door which leads ",10, WHITE)
        gameover_txt3 = font3.render("out of the dungeon...", 10, WHITE)
        screen.blit(gameover_txt1, (10, 200))
        screen.blit(gameover_txt2, (10, 250))
        screen.blit(gameover_txt3, (10, 300))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(11)
        menu()
##########################################CLASS FORMATS##################################
class Character:                #character class format
    def __init__(self,name,pclass,maxhp,hp,attack,inventory,exp,lvl,weapon):
        self.name=name
        self.pclass=pclass
        self.maxhp=maxhp
        self.hp=hp
        self.attack=attack
        self.inventory=inventory
        self.exp=exp
        self.lvl=lvl
        self.weapon=weapon

class Enemy:                    #Enemy class format
    def __init__(self,name,hp,attack,exp,lvl):
        self.name=name
        self.hp=hp
        self.attack=attack
        self.exp=exp
        self.lvl=lvl
####################################UNEQUIP#################################################
def unequip():
    if hero.weapon == "Small Dagger":
        hero.attack = hero.attack - 2
        hero.weapon = hero.weapon.replace("Small Dagger", "")
    elif hero.weapon == "Short staff":
        hero.attack = hero.attack - 3
        hero.weapon = hero.weapon.replace("Short Staff", "")
    elif hero.weapon == "Dull Mace":
        hero.attack = hero.attack - 2
        hero.weapon = hero.weapon.replace("Dull Mace", "")
    elif hero.weapon == "Club":
        hero.attack = hero.attack - 2
        hero.weapon = hero.weapon.replace("Club", "")
    elif hero.weapon == "Dagger":
        hero.attack = hero.attack - 2
        hero.weapon = hero.weapon.replace("Dagger", "")
    elif hero.weapon == "Battleaxe":
        hero.attack = hero.attack - 4
        hero.weapon = hero.weapon.replace("Battleaxe", "")
    elif hero.weapon == "Shortsword":
        hero.attack = hero.attack - 3
        hero.weapon = hero.weapon.replace("Shortsword", "")
    elif hero.weapon == "Longsword":
        hero.attack = hero.attack - 5
        hero.weapon = hero.weapon.replace("Longsword", "")
    elif hero.weapon == "Greatsword":
        hero.attack = hero.attack - 8
        hero.weapon = hero.weapon.replace("Greatsword", "")
##################################ITEMS###############################################
def smallhpvial():
    global herohp, hpgain
    hpgain=20
    herohp = str(int(herohp) + 20)
    if hero.maxhp < int(herohp):
        h = int(herohp) - hero.maxhp
        herohp = str(int(herohp) - h)

def largehpvial():
    global herohp, hpgain
    hpgain= 40
    herohp = str(int(herohp) + 40)
    if hero.maxhp < int(herohp):
        h = int(herohp) - hero.maxhp
        herohp =str(int(herohp) - h)

def club():
    global weaponstats
    unequip()
    hero.attack = hero.attack + 2
    hero.weapon += "Club"
    weaponstats = "Damage: +2"
def dagger():
    global weaponstats
    unequip()
    hero.attack = hero.attack + 2
    hero.weapon += "Dagger"
    weaponstats = "Damage: +2"
def battleaxe():
    global weaponstats
    unequip()
    hero.attack = hero.attack + 4
    hero.weapon += "Battleaxe"
    weaponstats = "Damage: +4"
def shortsword():
    global weaponstats
    unequip()
    hero.attack = hero.attack + 3
    hero.weapon += "Shortsword"
    weaponstats = "Damage: +3"
def longsword():
    global weaponstats
    unequip()
    hero.attack = hero.attack + 5
    hero.weapon += "Longsword"
    weaponstats = "Damage: +5"
def greatsword():
    global weaponstats
    unequip()
    hero.attack = hero.attack + 8
    hero.weapon += "Greatsword"
    weaponstats = "Damage: +8"
#####################################################RANDOM ITEMS###############################
def randomitem():  # gives user a random item
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, background, weaponstats, hpgain, BLACK
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    if stage=='boss1':
        nums="12"
    elif stage=='boss2':
        nums = "1"
    elif stage=='boss3':
        nums = "1"
    else:
        nums = "012"
    randnum = random.choice(nums)
    mystery_itemBG_img= pygame.image.load('mystery_itemBG.png')
    randtempitem=False
    randweapitem=False
    background=BLACK
    if stage==1:
        if randnum == "1":
            randnums = "123"
            randweap = random.choice(randnums)
            randweapitem = True
        elif randnum == "2":
            ranums = "1234"
            randtemp = random.choice(ranums)
            randtempitem = True
    elif stage==2:
        if randnum == "1":
            randnums = "34"
            randweap = random.choice(randnums)
            randweapitem = True
        elif randnum == "2":
            ranums = "12345"
            randtemp = random.choice(ranums)
            randtempitem = True
    elif stage==3:
        if randnum == "1":
            randnums = "45"
            randweap = random.choice(randnums)
            randweapitem = True
        elif randnum == "2":
            ranums = "123456"
            randtemp = random.choice(ranums)
            randtempitem = True
    elif stage == 'boss1':
        if randnum == "1":
            randnums = "345"
            randweap = random.choice(randnums)
            randweapitem = True
        elif randnum == "2":
            ranums = "2345"
            randtemp = random.choice(ranums)
            randtempitem = True
    elif stage == 'boss2':
        if randnum == "1":
            randnums = "456"
            randweap = random.choice(randnums)
            randweapitem = True
        elif randnum == "2":
            ranums = "23456"
            randtemp = random.choice(ranums)
            randtempitem = True
    elif stage == 'boss3':
        if randnum == "1":
            randnums = "56"
            randweap = random.choice(randnums)
            randweapitem = True
        elif randnum == "2":
            ranums = "23456"
            randtemp = random.choice(ranums)
            randtempitem = True

    if randnum == "0":
        while True:
            screen.fill(background)
            screen.blit(mystery_itemBG_img, (-50, 0))
            itemdrop_txt = font2.render("You received nothing from enemy", 10, WHITE)
            screen.blit(itemdrop_txt, (25, 425))
            pygame.display.flip()
            clock.tick(60)
            time.sleep(4)
            room_no_enemy()
    if randweapitem==True:
        if randweap == "1":
            if hero.weapon == "Club":
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt = font2.render("The enemy dropped a weapon you already have equipped", 10, WHITE)
                    screen.blit(itemdrop_txt, (25, 425))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(4)
                    room_no_enemy()
            else:
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt1 = font2.render("The enemy dropped a Club", 10, WHITE)
                    screen.blit(itemdrop_txt1, (25, 425))
                    itemdrop_txt2 = font2.render("Equip it? y/n Stats: Damage +2", 10, WHITE)
                    screen.blit(itemdrop_txt2, (25, 460))
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == K_y:
                                club()
                                room_no_enemy()
                            elif event.key == K_n:
                                pass
                                room_no_enemy()
                    pygame.display.flip()
                    clock.tick(60)
        elif randweap == "2":
            if hero.weapon == "Dagger":
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt = font2.render("The enemy dropped a weapon you already have equipped", 10, WHITE)
                    screen.blit(itemdrop_txt, (25, 425))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(4)
                    room_no_enemy()
            else:
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt1 = font2.render("The enemy dropped a Dagger", 10, WHITE)
                    screen.blit(itemdrop_txt1, (25, 425))
                    itemdrop_txt2 = font2.render("Equip it? y/n Stats: Damage +2", 10, WHITE)
                    screen.blit(itemdrop_txt2, (25, 460))
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == K_y:
                                dagger()
                                room_no_enemy()
                            elif event.key == K_n:
                                pass
                                room_no_enemy()
                    pygame.display.flip()

        elif randweap == "3":
            if hero.weapon == "Shortsword":

                    itemdrop_txt = font2.render("The enemy dropped an weapon you already have equipped", 10, WHITE)
                    screen.blit(itemdrop_txt, (25, 425))

                    time.sleep(4)
                    room_no_enemy()
            else:
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt1 = font2.render("The enemy dropped a Shortsword", 10, WHITE)
                    screen.blit(itemdrop_txt1, (25, 425))
                    itemdrop_txt2 = font2.render("Equip it? y/n Stats: Damage +3", 10, WHITE)
                    screen.blit(itemdrop_txt2, (25, 460))
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == K_y:
                                shortsword()
                                room_no_enemy()
                            elif event.key == K_n:
                                pass
                                room_no_enemy()
                    pygame.display.flip()

        elif randweap == "4":
            if hero.weapon == "Longsword":
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt = font2.render("The enemy dropped an item you already have equipped", 10, WHITE)
                    screen.blit(itemdrop_txt, (25, 425))

                    time.sleep(4)
                    room_no_enemy()
            else:
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt1 = font2.render("The enemy dropped a Longsword", 10, WHITE)
                    screen.blit(itemdrop_txt1, (25, 425))
                    itemdrop_txt2 = font2.render("Equip it? y/n Stats: Damage +5", 10, WHITE)
                    screen.blit(itemdrop_txt2, (25, 460))
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == K_y:
                                longsword()
                                room_no_enemy()
                            elif event.key == K_n:
                                pass
                                room_no_enemy()
                    pygame.display.flip()

        elif randweap == "5":
            if hero.weapon == "Battleaxe":
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt = font2.render("The enemy dropped an item you already have equipped", 10, WHITE)
                    screen.blit(itemdrop_txt, (25, 425))

                    time.sleep(4)
                    room_no_enemy()
            else:
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt1 = font2.render("The enemy dropped a Battleaxe", 10, WHITE)
                    screen.blit(itemdrop_txt1, (25, 425))
                    itemdrop_txt2 = font2.render("Equip it? y/n Stats: Damage +4", 10, WHITE)
                    screen.blit(itemdrop_txt2, (25, 460))
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == K_y:
                                battleaxe()
                                room_no_enemy()
                            elif event.key == K_n:
                                pass
                                room_no_enemy()
                    pygame.display.flip()


        elif randweap == "6":
            if hero.weapon == "Greatsword":
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt = font2.render("You already have item dropped, equipped", 10, WHITE)
                    screen.blit(itemdrop_txt, (25, 425))

                    time.sleep(4)
                    room_no_enemy()
            else:
                while True:
                    screen.fill(background)
                    screen.blit(mystery_itemBG_img, (-50, 0))
                    itemdrop_txt1 = font2.render("The enemy dropped a Greatsword", 10, WHITE)
                    screen.blit(itemdrop_txt1, (25, 425))
                    itemdrop_txt2 = font2.render("Equip it? y/n Stats: Damage +8", 10, WHITE)
                    screen.blit(itemdrop_txt2, (25, 460))
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == K_y:
                                greatsword()
                                room_no_enemy()
                            elif event.key == K_n:
                                pass
                                room_no_enemy()
                    pygame.display.flip()
                    clock.tick(60)

    if randtempitem==True:
        if randtemp == "1":
            while True:
                screen.fill(background)
                screen.blit(mystery_itemBG_img, (-50, 0))
                heroinventory.append("Small Potion of Health")
                itemdrop_txt = font2.render("The enemy dropped a Small Potion of Health", 10, WHITE)
                screen.blit(itemdrop_txt, (25, 425))
                pygame.display.flip()
                clock.tick(60)
                time.sleep(4)
                room_no_enemy()
        elif randtemp == "2":
            while True:
                screen.fill(background)
                screen.blit(mystery_itemBG_img, (-50, 0))
                heroinventory.append("Large Potion of Health")
                itemdrop_txt = font2.render("The enemy dropped a Large Potion of Health", 10, WHITE)
                screen.blit(itemdrop_txt, (25, 425))
                pygame.display.flip()
                clock.tick(60)
                time.sleep(4)
                room_no_enemy()
        elif randtemp == "3":
            while True:
                screen.fill(background)
                screen.blit(mystery_itemBG_img, (-50, 0))
                heroinventory.append("Potion of Poison")
                itemdrop_txt = font2.render("The enemy dropped a Potion of Poison", 10, WHITE)
                screen.blit(itemdrop_txt, (25, 425))
                pygame.display.flip()
                clock.tick(60)
                time.sleep(4)
                room_no_enemy()
        elif randtemp == "4":
            while True:
                screen.fill(background)
                screen.blit(mystery_itemBG_img, (-50, 0))
                heroinventory.append("Shortbow and Arrow")
                itemdrop_txt = font2.render("The enemy dropped a Shortbow and Arrow", 10, WHITE)
                screen.blit(itemdrop_txt, (25, 425))
                pygame.display.flip()
                clock.tick(60)
                time.sleep(4)
                room_no_enemy()
        elif randtemp == "5":
            while True:
                screen.fill(background)
                screen.blit(mystery_itemBG_img, (-50, 0))
                heroinventory.append("Maple Longbow and Fire Arrow")
                itemdrop_txt = font2.render("The enemy dropped a M Longbow and Fire Arrow", 10, WHITE)
                screen.blit(itemdrop_txt, (25, 425))
                pygame.display.flip()
                clock.tick(60)
                time.sleep(4)
                room_no_enemy()
        elif randtemp == "6":
            while True:
                screen.fill(background)
                screen.blit(mystery_itemBG_img, (-50, 0))
                heroinventory.append("Meteor Strike")
                itemdrop_txt = font2.render("The enemy dropped a Meteor Strike", 10, WHITE)
                screen.blit(itemdrop_txt, (25, 425))
                pygame.display.flip()
                clock.tick(60)
                time.sleep(4)
                room_no_enemy()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

########################INVENTORY MECHANICS###########################
def use_inv_item():
    global itemdmg, ui, WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, weaponstats, hpgain, attackhit_fx
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    if ui == "Small Potion of Health":
        smallhpvial()
        heroinventory.remove(ui)
        paction_txt1 = font2.render("You used " + ui, 10, WHITE)
        paction_txt2 = font2.render("and gained " + str(hpgain) + " health", 10, WHITE)
        screen.blit(paction_txt1, (180, 650))
        screen.blit(paction_txt2, (180, 680))
        pygame.display.flip()
        clock.tick(60)
    elif ui == "Large Potion of Health":
        largehpvial()
        heroinventory.remove(ui)
        paction_txt1 = font2.render("You used " + ui, 10, WHITE)
        paction_txt2 = font2.render("and gained " + str(hpgain) + " health", 10, WHITE)
        screen.blit(paction_txt1, (180, 650))
        screen.blit(paction_txt2, (180, 680))
        pygame.display.flip()
        clock.tick(60)
    else:
        if ui == "Potion of Poison":
            itemdmg = 11
            heroinventory.remove(ui)

        elif ui == "Shortbow and Arrow":
            itemdmg = 17
            heroinventory.remove(ui)

        elif ui == "Maple Longbow and Fire Arrow":
            itemdmg = 27
            heroinventory.remove(ui)

        elif ui == "Meteor Strike":
            itemdmg = 40
            hero.inventory.remove(ui)
        paction_txt1 = font2.render("You used " + ui, 10, WHITE)
        paction_txt2 = font2.render(" on enemy and did " + str(itemdmg) + " damage", 10, WHITE)
        screen.blit(paction_txt1, (180, 650))
        screen.blit(paction_txt2, (180, 680))
        pygame.display.flip()
        clock.tick(60)
        attackhit_fx.play()
        time.sleep(2)

def use_inv_item_notinbattle():
    global itemdmg, ui, WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, weaponstats, hpgain, attackhit_fx
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    if ui == "Small Potion of Health":
        smallhpvial()
        heroinventory.remove(ui)
        paction_txt1 = font2.render("You used " + ui, 10, WHITE)
        paction_txt2 = font2.render("and gained " + str(hpgain) + " health", 10, WHITE)
        screen.blit(paction_txt1, (180, 650))
        screen.blit(paction_txt2, (180, 680))
        pygame.display.flip()
        clock.tick(60)
        time.sleep(2)
    elif ui == "Large Potion of Health":
        largehpvial()
        heroinventory.remove(ui)
        paction_txt1 = font2.render("You used " + ui , 10, WHITE)
        paction_txt2 = font2.render("and gained " + str(hpgain) + " health", 10, WHITE)
        screen.blit(paction_txt1, (180, 650))
        screen.blit(paction_txt2, (180, 680))
        pygame.display.flip()
        clock.tick(60)
        time.sleep(2)
    else:
        paction_txt1 = font2.render("Can't use item outside", 10, WHITE)
        paction_txt2 = font2.render("of a battle!", 10, WHITE)
        screen.blit(paction_txt1, (180, 650))
        screen.blit(paction_txt2, (180, 680))
        pygame.display.flip()
        clock.tick(60)
        time.sleep(2)
##################################PLAYER CLASSES###################################################
class Warrior(Character):
    def __init__(self):
        super().__init__(name="", pclass="Warrior", attack=9,
                         maxhp=80, hp=80, inventory=['Small Potion of Health'], exp=0, lvl=1, weapon="Small Dagger")

    prof = "warrior"

class Juggernaut(Character):
    def __init__(self):
        super().__init__(name="", pclass="Juggernaut", attack=7,
                         maxhp=100, hp=100, inventory=['Small Potion of Health'], exp=0, lvl=1, weapon="Dull Mace")

    prof = "juggernaut"


class Mage(Character):
    def __init__(self):
        super().__init__(name="", pclass="Mage", attack=11,
                         maxhp=60, hp=60, inventory=['Small Potion of Health'], exp=0, lvl=1, weapon="Short Staff")
    prof = "mage"


##########ENEMY CLASSES###############################################################################
class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Goblin",
                         hp=18, attack=5, exp=5, lvl=1)


class Skeleton(Enemy):
    def __init__(self):
        super().__init__(name="Skeleton",
                         hp=20, attack=7, exp=7, lvl=1)


class GiantSpider(Enemy):
    def __init__(self):
        super().__init__(name="Giant Spider",
                         hp=24, attack=9, exp=9, lvl=1)


class Boss1(Enemy):
    def __init__(self):
        super().__init__(name="Armored Wraith",
                         hp=50, attack=12, exp=25, lvl=5)


class armoredskeleton(Enemy):
    def __init__(self):
        super().__init__(name="Armored Skeleton",
                         hp=28, attack=9, exp=15, lvl=5)


class troll(Enemy):
    def __init__(self):
        super().__init__(name="Troll",
                         hp=35, attack=10, exp=19, lvl=5)


class orc(Enemy):
    def __init__(self):
        super().__init__(name="Orc",
                         hp=34, attack=11, exp=17, lvl=5)


class undeadsoldier(Enemy):
    def __init__(self):
        super().__init__(name="Undead Soldier",
                         hp=32, attack=13, exp=22, lvl=5)


class Boss2(Enemy):
    def __init__(self):
        super().__init__(name="Possessed Mage",
                         hp=75, attack=17, exp=45, lvl=5)

class griffin(Enemy):
    def __init__(self):
        super().__init__(name="Griffin",
                         hp=38, attack=15, exp=27, lvl=1)

class dragon(Enemy):
    def __init__(self):
        super().__init__(name="Dragon",
                         hp=40, attack=17, exp=30, lvl=1)

class demon(Enemy):
    def __init__(self):
        super().__init__(name="Demon",
                         hp=42, attack=17, exp=27, lvl=1)

class Boss3(Enemy):
    def __init__(self):
        super().__init__(name="Evil Penguin",
                         hp=100, attack=19, exp=27, lvl=1)
##########################STAGES###################################################################################
def stage1():
    global enemiesdefeated
    if enemiesdefeated<5:
        randenemystage1()
    elif enemiesdefeated==5:
        boss1()
    else:
        font = pygame.font.SysFont("monospace", 56)
        while True:
            screen.fill(background)
            stage1_txt = font.render("STAGE 2", 10, WHITE)
            screen.blit(stage1_txt, (280, 425))
            pygame.display.flip()
            clock.tick(60)
            time.sleep(1.5)
            filler = True
            if filler == True:
                stage2()
def stage2():
    global enemiesdefeated
    if enemiesdefeated<10:
        randenemystage2()
    elif enemiesdefeated==10:
        boss2()
    else:
        font = pygame.font.SysFont("monospace", 56)
        while True:
            screen.fill(background)
            stage1_txt = font.render("STAGE 3", 10, WHITE)
            screen.blit(stage1_txt, (280, 425))
            pygame.display.flip()
            clock.tick(60)
            time.sleep(1.5)
            filler = True
            if filler == True:
                stage3()
def stage3():
    global enemiesdefeated
    if enemiesdefeated<14:
        randenemystage3()
    elif enemiesdefeated==14:
        boss3()
    else:
        endingscreen()

def room_no_enemy():
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, weaponstats, hpgain, ui, GRAY, inv_bg
    pygame.mixer.music.load('Dungeon Theme.ogg')
    pygame.mixer.music.play(-1, 0)
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    while True:
        screen.blit(dungeonBGImg, (0, 0))
        screen.blit(character_viewImg, (200, 650))
        player_hp_txt = font2.render("HP:" + herohp, 10, WHITE, GRAY)
        screen.blit(player_hp_txt, (40, 10))
        exp_txt = font2.render("XP:" + heroexp, 10, WHITE, GRAY)
        screen.blit(exp_txt, (500, 850))
        inventoryhub_txt = font2.render("Inventory['e']", 10, WHITE, GRAY)
        playerlvl_txt = font2.render("Player Level:" + playerlvl, 10, WHITE, GRAY)
        screen.blit(playerlvl_txt, (375, 10))
        screen.blit(inventoryhub_txt, (5, 850))
        menu_font = pygame.font.Font(None, 42)
        attackBTN = [Option("ATTACK", (10, 200))]
        defendBTN = [Option("DEFEND", (10, 275))]
        saveBTN = [Option("SAVE", (75, 50))]
        for option1 in attackBTN:  # check to see if the quit button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in defendBTN:  # check to see if the save button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in saveBTN:  # check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==MOUSEBUTTONDOWN:
                if option3.hovered==True:
                    savegame()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    while True:
                        screen.fill(background)
                        pygame.display.flip()
                        clock.tick(60)
                        time.sleep(1.5)
                        filler = True
                        if filler == True:
                            if enemiesdefeated<6:
                                stage1()
                            elif enemiesdefeated<11:
                                stage2()
                            elif enemiesdefeated>=11:
                                stage3()
                elif event.key == K_e:  #if 'e' key is pressed it pulls up the player's inventory
                    openinv = True
                    while openinv:
                        screen.blit(inv_bg, (0, 0))
                        font3 = pygame.font.SysFont("Times New Roman", 24)
                        font4 = pygame.font.SysFont("Times New Roman", 56)
                        e_close_txt = font3.render("Press [e] to close inventory", 10, WHITE)
                        inventoryhub_title = font4.render("Inventory", 10, WHITE)
                        player_stats_title = font3.render("Player Stats:", 10, WHITE)
                        player_stats_txt = font3.render(
                            "Hero Class: " + hero.pclass + "   HP: " + str(herohp) + "/" + str(
                                hero.maxhp) + "   Attack: " + str(hero.attack), 10, WHITE)
                        player_stats_txt1 = font3.render(
                            "LVL: " + str(playerlvl) + "   XP: " + str(heroexp) + "   Stage: " + str(
                                stage) + "   Enemies Defeated: " + str(enemiesdefeated), 10, WHITE)
                        screen.blit(player_stats_title, (40, 170))
                        screen.blit(player_stats_txt, (40, 210))
                        screen.blit(player_stats_txt1, (40, 250))
                        inv_weap_equipped_txt = font3.render(
                            "Weapon Equipped:" + str(hero.weapon) + " | Stats: " + weaponstats, 10, WHITE)
                        inv_items_titletxt = font3.render("Items: ", 10, WHITE)
                        if len(heroinventory)>0:
                            item1_txt=font3.render("Item 1:" + str(heroinventory[0]),10, WHITE)
                            screen.blit(item1_txt, (40, 400))
                            if len(heroinventory)>1:
                                item2_txt = font3.render("Item 2:" + str(heroinventory[1]), 10, WHITE)
                                screen.blit(item2_txt, (40, 425))
                                if len(heroinventory) > 2:
                                    item3_txt = font3.render("Item 3:" + str(heroinventory[2]), 10, WHITE)
                                    screen.blit(item3_txt, (40, 450))
                                    if len(heroinventory) > 3:
                                        item4_txt = font3.render("Item 4:" + str(heroinventory[3]), 10, WHITE)
                                        screen.blit(item4_txt, (40, 475))
                                        if len(heroinventory) > 4:
                                            item5_txt = font3.render("Item 5:" + str(heroinventory[4]), 10, WHITE)
                                            screen.blit(item5_txt, (40, 500))
                                            if len(heroinventory) >5:
                                                item6_txt = font3.render("Item 6:" + str(heroinventory[5]), 10, WHITE)
                                                screen.blit(item6_txt, (40, 525))
                                                if len(heroinventory) > 6:
                                                    item7_txt = font3.render("Item 7:" + str(heroinventory[6]), 10, WHITE)
                                                    screen.blit(item7_txt, (40, 550))
                                                    if len(heroinventory) >7:
                                                        item8_txt = font3.render("Item 8:" + str(heroinventory[7]), 10, WHITE)
                                                        screen.blit(item8_txt, (40, 575))
                                                        if len(heroinventory) > 8:
                                                            item9_txt = font3.render("Item 9:" + str(heroinventory[8]), 10, WHITE)
                                                            screen.blit(item9_txt, (40, 600))
                                                            if len(heroinventory) > 9:
                                                                item10_txt = font3.render("Item 10:" + str(heroinventory[9]), 10, WHITE)
                                                                screen.blit(item10_txt, (40, 625))
                        screen.blit(inventoryhub_title, (170, 100))
                        screen.blit(inv_weap_equipped_txt, (40, 300))
                        screen.blit(inv_items_titletxt, (40, 350))
                        screen.blit(e_close_txt, (40, 780))
                        pygame.display.flip()
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_e: #when the 'e' key is pressed when inventory is open, it closes inventory
                                    openinv = False
                                elif event.key == K_1:  # number pressed corresponds with items in inventory-- to use items
                                    try:
                                        if len(heroinventory) >= 1:
                                            ui = heroinventory[0]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                                elif event.key == K_2:
                                    try:
                                        if len(heroinventory) >= 2:
                                            ui = heroinventory[1]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                                elif event.key == K_3:
                                    try:
                                        if len(heroinventory) > 2:
                                            ui = heroinventory[2]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                                elif event.key == K_4:
                                    try:
                                        if len(heroinventory) > 3:
                                            ui = heroinventory[3]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                                elif event.key == K_5:
                                    try:
                                        if len(heroinventory) > 4:
                                            ui = heroinventory[4]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                                elif event.key == K_6:
                                    try:
                                        if len(heroinventory) > 5:
                                            ui = heroinventory[5]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                                elif event.key == K_7:
                                    try:
                                        if len(heroinventory) > 6:
                                            ui = heroinventory[6]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        print('no item in slot')
                                elif event.key == K_8:
                                    try:
                                        if len(heroinventory) > 7:
                                            ui = heroinventory[7]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                                elif event.key == K_9:
                                    try:
                                        if len(heroinventory) > 8:
                                            ui = heroinventory[8]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                                elif event.key == K_0:
                                    try:
                                        if len(heroinventory) > 9:
                                            ui = heroinventory[9]
                                            use_inv_item_notinbattle()
                                            openinv = False
                                        else:
                                            pass
                                    except IndexError:
                                        pass
                else:
                    pass

        pygame.display.flip()
        clock.tick(60)
def boss3():
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain, attackhit_fx, inv_bg, stage
    stage = 'boss3'
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    pygame.mixer.music.load('United We Stand - Divided We Fall.mp3')
    pygame.mixer.music.play(-1, 0)
    evilpenguinIMG = pygame.image.load('evilpenguin_img.png')
    evilpenguinIMG = pygame.transform.scale(evilpenguinIMG, (275, 350))
    enemy = Boss3()
    enemyhp = str(enemy.hp)
    enemyname = enemy.name
    enemy_img = evilpenguinIMG
    attackhit_fx = pygame.mixer.Sound('Swords_Collide-Sound.wav')
    attackmiss_fx = pygame.mixer.Sound('Swoosh_sound.wav')
    enemy_deathfx = pygame.mixer.Sound('enemy_death.wav')
    while True:  # displays the player in the dungeon with hp and explaining controls
        player_hp_txt = font2.render("HP:" + herohp, 10, WHITE, GRAY)
        exp_txt = font2.render("XP:" + heroexp, 10, WHITE, GRAY)
        enemy_hp_txt = font2.render("HP:" + enemyhp, 10, WHITE, GRAY)
        enemy_name_txt = font2.render("BOSS: " + enemyname, 10, WHITE, GRAY)
        inventoryhub_txt = font2.render("Inventory['e']", 10, WHITE, GRAY)
        playerlvl_txt = font2.render("Player Level:" + playerlvl, 10, WHITE, GRAY)
        screen.blit(dungeonBGImg, (0, 0))
        screen.blit(character_viewImg, (200, 650))
        screen.blit(enemy_img, (200, 250))
        screen.blit(exp_txt, (500, 850))
        screen.blit(player_hp_txt, (40, 10))
        screen.blit(enemy_hp_txt, (200, 260))
        screen.blit(enemy_name_txt, (200, 220))
        screen.blit(playerlvl_txt, (375, 10))
        screen.blit(inventoryhub_txt, (5, 850))

        menu_font = pygame.font.Font(None, 42)
        attackBTN = [Option("ATTACK", (10, 200))]
        defendBTN = [Option("DEFEND", (10, 275))]
        saveBTN = [Option("SAVE", (75, 50))]
        for option1 in attackBTN:  # check to see if the quit button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in defendBTN:  # check to see if the save button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in saveBTN:  # check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_e:  # when the 'e' key is pressed, it pulls up the player's inventory
                    openinv = True
                    while openinv:
                        screen.blit(inv_bg, (0, 0))
                        font3 = pygame.font.SysFont("Times New Roman", 24)
                        font4 = pygame.font.SysFont("Times New Roman", 56)
                        e_close_txt = font3.render("Press [e] to close inventory", 10, WHITE)
                        inventoryhub_title = font4.render("Inventory", 10, WHITE)
                        player_stats_title = font3.render("Player Stats:", 10, WHITE)
                        player_stats_txt = font3.render(
                            "Hero Class: " + hero.pclass + "   HP: " + str(herohp) + "/" + str(
                                hero.maxhp) + "   Attack: " + str(hero.attack), 10, WHITE)
                        player_stats_txt1 = font3.render(
                            "LVL: " + str(playerlvl) + "   XP: " + str(heroexp) + "   Stage: " + str(
                                stage) + "   Enemies Defeated: " + str(enemiesdefeated), 10, WHITE)
                        screen.blit(player_stats_title, (40, 170))
                        screen.blit(player_stats_txt, (40, 210))
                        screen.blit(player_stats_txt1, (40, 250))
                        inv_weap_equipped_txt = font3.render(
                            "Weapon Equipped:" + str(hero.weapon) + " | Stats: " + weaponstats, 10, WHITE)
                        inv_items_titletxt = font3.render("Items: ", 10, WHITE)
                        if len(heroinventory) > 0:
                            item1_txt = font3.render("Item 1:" + str(heroinventory[0]), 10, WHITE)
                            screen.blit(item1_txt, (40, 400))
                            if len(heroinventory) > 1:
                                item2_txt = font3.render("Item 2:" + str(heroinventory[1]), 10, WHITE)
                                screen.blit(item2_txt, (40, 425))
                                if len(heroinventory) > 2:
                                    item3_txt = font3.render("Item 3:" + str(heroinventory[2]), 10, WHITE)
                                    screen.blit(item3_txt, (40, 450))
                                    if len(heroinventory) > 3:
                                        item4_txt = font3.render("Item 4:" + str(heroinventory[3]), 10, WHITE)
                                        screen.blit(item4_txt, (40, 475))
                                        if len(heroinventory) > 4:
                                            item5_txt = font3.render("Item 5:" + str(heroinventory[4]), 10, WHITE)
                                            screen.blit(item5_txt, (40, 500))
                                            if len(heroinventory) > 5:
                                                item6_txt = font3.render("Item 6:" + str(heroinventory[5]), 10, WHITE)
                                                screen.blit(item6_txt, (40, 525))
                                                if len(heroinventory) > 6:
                                                    item7_txt = font3.render("Item 7:" + str(heroinventory[6]), 10,
                                                                             WHITE)
                                                    screen.blit(item7_txt, (40, 550))
                                                    if len(heroinventory) > 7:
                                                        item8_txt = font3.render("Item 8:" + str(heroinventory[7]), 10,
                                                                                 WHITE)
                                                        screen.blit(item8_txt, (40, 575))
                                                        if len(heroinventory) > 8:
                                                            item9_txt = font3.render("Item 9:" + str(heroinventory[8]),
                                                                                     10, WHITE)
                                                            screen.blit(item9_txt, (40, 600))
                                                            if len(heroinventory) > 9:
                                                                item10_txt = font3.render(
                                                                    "Item 10:" + str(heroinventory[9]), 10, WHITE)
                                                                screen.blit(item10_txt, (40, 625))
                        screen.blit(inventoryhub_title, (170, 100))
                        screen.blit(inv_weap_equipped_txt, (40, 300))
                        screen.blit(inv_items_titletxt, (40, 350))
                        screen.blit(e_close_txt, (40, 780))
                        pygame.display.flip()
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_e:  # when the 'e' key is pressed when inventory is open, it closes inventory
                                    openinv = False
                                elif event.key == K_1:  # number pressed corresponds with items in inventory-- to use items
                                    try:
                                        ui = heroinventory[0]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass

                                elif event.key == K_2:
                                    try:
                                        ui = heroinventory[1]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_3:
                                    try:
                                        ui = heroinventory[2]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_4:
                                    try:
                                        ui = heroinventory[3]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_5:
                                    try:
                                        ui = heroinventory[4]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_6:
                                    try:
                                        ui = heroinventory[5]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_7:
                                    try:
                                        ui = heroinventory[6]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_8:
                                    try:
                                        ui = heroinventory[7]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_9:
                                    try:
                                        ui = heroinventory[8]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_0:
                                    try:
                                        ui = heroinventory[9]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
            elif event.type == MOUSEBUTTONDOWN:
                if option1.hovered == True:
                    cdmg = random.randint(0, hero.attack)
                    if cdmg == 0:
                        paction_txt = font2.render("You missed", 10, WHITE, GRAY)
                        screen.blit(paction_txt, (360, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        paction_txt1 = font2.render("You attacked and", 10, WHITE, GRAY)
                        paction_txt2 = font2.render("did " + str(cdmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 650))
                        screen.blit(paction_txt2, (400, 680))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    enemyhp = str(int(enemyhp) - cdmg)

                    if int(enemyhp) <= 0:
                        enemyhp = 0
                        paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                        paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 710))
                        screen.blit(paction_txt2, (400, 740))
                        pygame.display.flip()
                        clock.tick(60)
                        enemy_deathfx.play()
                        heroexp = str(int(heroexp) + enemy.exp)
                        enemiesdefeated += 1
                        time.sleep(3)
                        endingscreen()
                    edmg = random.randint(0, enemy.attack)
                    if edmg == 0:
                        eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                        screen.blit(eaction_txt, (360, 350))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                        eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(eaction_txt1, (360, 350))
                        screen.blit(eaction_txt2, (360, 380))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    herohp = str(int(herohp) - edmg)
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option2.hovered == True:
                    paction_txt = font2.render("You defended", 10, WHITE, GRAY)
                    screen.blit(paction_txt, (360, 650))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(1.5)
                    edmg = random.randint(0, enemy.attack)
                    eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                    eaction_txt2 = font2.render("did " + str(edmg / 2) + " damage", 10, WHITE, GRAY)
                    screen.blit(eaction_txt1, (360, 350))
                    screen.blit(eaction_txt2, (360, 380))
                    pygame.display.flip()
                    clock.tick(60)
                    attackhit_fx.play()
                    time.sleep(2)
                    herohp = str(int(int(herohp) - (edmg / 2)))
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option3.hovered == True:
                    savegame()

        pygame.display.flip()
        clock.tick(60)
def boss2():
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain, attackhit_fx, inv_bg, stage
    stage = 'boss2'
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    pygame.mixer.music.load('United We Stand - Divided We Fall.mp3')
    pygame.mixer.music.play()
    posssessedmageIMG= pygame.image.load('possessed_mage_img.png')
    posssessedmageIMG = pygame.transform.scale(posssessedmageIMG, (200, 300))
    enemy=Boss2()
    enemyhp = str(enemy.hp)
    enemyname = enemy.name
    enemy_img = posssessedmageIMG
    attackhit_fx = pygame.mixer.Sound('Swords_Collide-Sound.wav')
    attackmiss_fx = pygame.mixer.Sound('Swoosh_sound.wav')
    enemy_deathfx = pygame.mixer.Sound('enemy_death.wav')
    while True:  # displays the player in the dungeon with hp and explaining controls
        player_hp_txt = font2.render("HP:" + herohp, 10, WHITE, GRAY)
        exp_txt = font2.render("XP:" + heroexp, 10, WHITE, GRAY)
        enemy_hp_txt = font2.render("HP:" + enemyhp, 10, WHITE, GRAY)
        enemy_name_txt = font2.render("BOSS: " + enemyname, 10, WHITE, GRAY)
        inventoryhub_txt = font2.render("Inventory['e']", 10, WHITE, GRAY)
        playerlvl_txt = font2.render("Player Level:" + playerlvl, 10, WHITE, GRAY)
        screen.blit(dungeonBGImg, (0, 0))
        screen.blit(character_viewImg, (200, 650))
        screen.blit(enemy_img, (200, 325))
        screen.blit(exp_txt, (500, 850))
        screen.blit(player_hp_txt, (40, 10))
        screen.blit(enemy_hp_txt, (200, 260))
        screen.blit(enemy_name_txt, (200, 220))
        screen.blit(playerlvl_txt, (375, 10))
        screen.blit(inventoryhub_txt, (5, 850))

        menu_font = pygame.font.Font(None, 42)
        attackBTN = [Option("ATTACK", (10, 200))]
        defendBTN = [Option("DEFEND", (10, 275))]
        saveBTN = [Option("SAVE", (75, 50))]
        for option1 in attackBTN:  # check to see if the quit button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in defendBTN:  # check to see if the save button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in saveBTN:  # check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_e:  # when the 'e' key is pressed, it pulls up the player's inventory
                    openinv = True
                    while openinv:
                        screen.blit(inv_bg, (0, 0))
                        font3 = pygame.font.SysFont("Times New Roman", 24)
                        font4 = pygame.font.SysFont("Times New Roman", 56)
                        e_close_txt = font3.render("Press [e] to close inventory", 10, WHITE)
                        inventoryhub_title = font4.render("Inventory", 10, WHITE)
                        player_stats_title = font3.render("Player Stats:", 10, WHITE)
                        player_stats_txt = font3.render(
                            "Hero Class: " + hero.pclass + "   HP: " + str(herohp) + "/" + str(
                                hero.maxhp) + "   Attack: " + str(hero.attack), 10, WHITE)
                        player_stats_txt1 = font3.render(
                            "LVL: " + str(playerlvl) + "   XP: " + str(heroexp) + "   Stage: " + str(
                                stage) + "   Enemies Defeated: " + str(enemiesdefeated), 10, WHITE)
                        screen.blit(player_stats_title, (40, 170))
                        screen.blit(player_stats_txt, (40, 210))
                        screen.blit(player_stats_txt1, (40, 250))
                        inv_weap_equipped_txt = font3.render(
                            "Weapon Equipped:" + str(hero.weapon) + " | Stats: " + weaponstats, 10, WHITE)
                        inv_items_titletxt = font3.render("Items: ", 10, WHITE)
                        if len(heroinventory)>0:
                            item1_txt=font3.render("Item 1:" + str(heroinventory[0]),10, WHITE)
                            screen.blit(item1_txt, (40, 400))
                            if len(heroinventory)>1:
                                item2_txt = font3.render("Item 2:" + str(heroinventory[1]), 10, WHITE)
                                screen.blit(item2_txt, (40, 425))
                                if len(heroinventory) > 2:
                                    item3_txt = font3.render("Item 3:" + str(heroinventory[2]), 10, WHITE)
                                    screen.blit(item3_txt, (40, 450))
                                    if len(heroinventory) > 3:
                                        item4_txt = font3.render("Item 4:" + str(heroinventory[3]), 10, WHITE)
                                        screen.blit(item4_txt, (40, 475))
                                        if len(heroinventory) > 4:
                                            item5_txt = font3.render("Item 5:" + str(heroinventory[4]), 10, WHITE)
                                            screen.blit(item5_txt, (40, 500))
                                            if len(heroinventory) >5:
                                                item6_txt = font3.render("Item 6:" + str(heroinventory[5]), 10, WHITE)
                                                screen.blit(item6_txt, (40, 525))
                                                if len(heroinventory) > 6:
                                                    item7_txt = font3.render("Item 7:" + str(heroinventory[6]), 10, WHITE)
                                                    screen.blit(item7_txt, (40, 550))
                                                    if len(heroinventory) >7:
                                                        item8_txt = font3.render("Item 8:" + str(heroinventory[7]), 10, WHITE)
                                                        screen.blit(item8_txt, (40, 575))
                                                        if len(heroinventory) > 8:
                                                            item9_txt = font3.render("Item 9:" + str(heroinventory[8]), 10, WHITE)
                                                            screen.blit(item9_txt, (40, 600))
                                                            if len(heroinventory) > 9:
                                                                item10_txt = font3.render("Item 10:" + str(heroinventory[9]), 10, WHITE)
                                                                screen.blit(item10_txt, (40, 625))
                        screen.blit(inventoryhub_title, (170, 100))
                        screen.blit(inv_weap_equipped_txt, (40, 300))
                        screen.blit(inv_items_titletxt, (40, 350))
                        screen.blit(e_close_txt, (40, 780))
                        pygame.display.flip()
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_e:  # when the 'e' key is pressed when inventory is open, it closes inventory
                                    openinv = False
                                elif event.key == K_1:  # number pressed corresponds with items in inventory-- to use items
                                    try:
                                        ui = heroinventory[0]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass

                                elif event.key == K_2:
                                    try:
                                        ui = heroinventory[1]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_3:
                                    try:
                                        ui = heroinventory[2]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_4:
                                    try:
                                        ui = heroinventory[3]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(5)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_5:
                                    try:
                                        ui = heroinventory[4]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_6:
                                    try:
                                        ui = heroinventory[5]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_7:
                                    try:
                                        ui = heroinventory[6]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_8:
                                    try:
                                        ui = heroinventory[7]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_9:
                                    try:
                                        ui = heroinventory[8]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_0:
                                    try:
                                        ui = heroinventory[9]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
            elif event.type == MOUSEBUTTONDOWN:
                if option1.hovered == True:
                    cdmg = random.randint(0, hero.attack)
                    if cdmg == 0:
                        paction_txt = font2.render("You missed", 10, WHITE, GRAY)
                        screen.blit(paction_txt, (360, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        paction_txt1 = font2.render("You attacked and", 10, WHITE, GRAY)
                        paction_txt2 = font2.render("did " + str(cdmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 650))
                        screen.blit(paction_txt2, (400, 680))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    enemyhp = str(int(enemyhp) - cdmg)

                    if int(enemyhp) <= 0:
                        enemyhp = 0
                        paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                        paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 710))
                        screen.blit(paction_txt2, (400, 740))
                        pygame.display.flip()
                        clock.tick(60)
                        enemy_deathfx.play()
                        heroexp = str(int(heroexp) + enemy.exp)
                        enemiesdefeated+=1
                        stage=3
                        time.sleep(3)
                        lvl_up()
                        randomitem()
                    edmg = random.randint(0, enemy.attack)
                    if edmg == 0:
                        eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                        screen.blit(eaction_txt, (360, 350))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                        eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(eaction_txt1, (360, 350))
                        screen.blit(eaction_txt2, (360, 380))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    herohp = str(int(herohp) - edmg)
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option2.hovered == True:
                    paction_txt = font2.render("You defended", 10, WHITE, GRAY)
                    screen.blit(paction_txt, (360, 650))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(1.5)
                    edmg = random.randint(0, enemy.attack)
                    eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                    eaction_txt2 = font2.render("did " + str(edmg / 2) + " damage", 10, WHITE, GRAY)
                    screen.blit(eaction_txt1, (360, 350))
                    screen.blit(eaction_txt2, (360, 380))
                    pygame.display.flip()
                    clock.tick(60)
                    attackhit_fx.play()
                    time.sleep(2)
                    herohp = str(int(int(herohp) - (edmg / 2)))
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option3.hovered == True:
                    savegame()

        pygame.display.flip()
        clock.tick(60)
def boss1():
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain, attackhit_fx, inv_bg, stage
    stage='boss1'
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    pygame.mixer.music.load('United We Stand - Divided We Fall.mp3')
    pygame.mixer.music.play(-1, 0)
    wraithIMG= pygame.image.load('wraith_image.png')
    wraithIMG = pygame.transform.scale(wraithIMG, (150, 250))
    enemy=Boss1()
    enemyhp = str(enemy.hp)
    enemyname = enemy.name
    enemy_img = wraithIMG
    attackhit_fx = pygame.mixer.Sound('Swords_Collide-Sound.wav')
    attackmiss_fx = pygame.mixer.Sound('Swoosh_sound.wav')
    enemy_deathfx = pygame.mixer.Sound('enemy_death.wav')
    while True:  # displays the player in the dungeon with hp and explaining controls
        player_hp_txt = font2.render("HP:" + herohp, 10, WHITE, GRAY)
        exp_txt = font2.render("XP:" + heroexp, 10, WHITE, GRAY)
        enemy_hp_txt = font2.render("HP:" + enemyhp, 10, WHITE, GRAY)
        enemy_name_txt = font2.render("BOSS: " + enemyname, 10, WHITE, GRAY)
        inventoryhub_txt = font2.render("Inventory['e']", 10, WHITE, GRAY)
        playerlvl_txt = font2.render("Player Level:" + playerlvl, 10, WHITE, GRAY)
        screen.blit(dungeonBGImg, (0, 0))
        screen.blit(character_viewImg, (200, 650))
        screen.blit(enemy_img, (200, 325))
        screen.blit(exp_txt, (500, 850))
        screen.blit(player_hp_txt, (40, 10))
        screen.blit(enemy_hp_txt, (200, 260))
        screen.blit(enemy_name_txt, (200, 220))
        screen.blit(playerlvl_txt, (375, 10))
        screen.blit(inventoryhub_txt, (5, 850))

        menu_font = pygame.font.Font(None, 42)
        attackBTN = [Option("ATTACK", (10, 200))]
        defendBTN = [Option("DEFEND", (10, 275))]
        saveBTN = [Option("SAVE", (75, 50))]
        for option1 in attackBTN:  # check to see if the quit button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in defendBTN:  # check to see if the save button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in saveBTN:  # check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_e:  # when the 'e' key is pressed, it pulls up the player's inventory
                    openinv = True
                    while openinv:
                        screen.blit(inv_bg, (0, 0))
                        font3 = pygame.font.SysFont("Times New Roman", 24)
                        font4 = pygame.font.SysFont("Times New Roman", 56)
                        e_close_txt = font3.render("Press [e] to close inventory", 10, WHITE)
                        inventoryhub_title = font4.render("Inventory", 10, WHITE)
                        player_stats_title = font3.render("Player Stats:", 10, WHITE)
                        player_stats_txt = font3.render(
                            "Hero Class: " + hero.pclass + "   HP: " + str(herohp) + "/" + str(
                                hero.maxhp) + "   Attack: " + str(hero.attack), 10, WHITE)
                        player_stats_txt1 = font3.render(
                            "LVL: " + str(playerlvl) + "   XP: " + str(heroexp) + "   Stage: " + str(
                                stage) + "   Enemies Defeated: " + str(enemiesdefeated), 10, WHITE)
                        screen.blit(player_stats_title, (40, 170))
                        screen.blit(player_stats_txt, (40, 210))
                        screen.blit(player_stats_txt1, (40, 250))
                        inv_weap_equipped_txt = font3.render(
                            "Weapon Equipped:" + str(hero.weapon) + " | Stats: " + weaponstats, 10, WHITE)
                        inv_items_titletxt = font3.render("Items: ", 10, WHITE)
                        if len(heroinventory)>0:
                            item1_txt=font3.render("Item 1:" + str(heroinventory[0]),10, WHITE)
                            screen.blit(item1_txt, (40, 400))
                            if len(heroinventory)>1:
                                item2_txt = font3.render("Item 2:" + str(heroinventory[1]), 10, WHITE)
                                screen.blit(item2_txt, (40, 425))
                                if len(heroinventory) > 2:
                                    item3_txt = font3.render("Item 3:" + str(heroinventory[2]), 10, WHITE)
                                    screen.blit(item3_txt, (40, 450))
                                    if len(heroinventory) > 3:
                                        item4_txt = font3.render("Item 4:" + str(heroinventory[3]), 10, WHITE)
                                        screen.blit(item4_txt, (40, 475))
                                        if len(heroinventory) > 4:
                                            item5_txt = font3.render("Item 5:" + str(heroinventory[4]), 10, WHITE)
                                            screen.blit(item5_txt, (40, 500))
                                            if len(heroinventory) >5:
                                                item6_txt = font3.render("Item 6:" + str(heroinventory[5]), 10, WHITE)
                                                screen.blit(item6_txt, (40, 525))
                                                if len(heroinventory) > 6:
                                                    item7_txt = font3.render("Item 7:" + str(heroinventory[6]), 10, WHITE)
                                                    screen.blit(item7_txt, (40, 550))
                                                    if len(heroinventory) >7:
                                                        item8_txt = font3.render("Item 8:" + str(heroinventory[7]), 10, WHITE)
                                                        screen.blit(item8_txt, (40, 575))
                                                        if len(heroinventory) > 8:
                                                            item9_txt = font3.render("Item 9:" + str(heroinventory[8]), 10, WHITE)
                                                            screen.blit(item9_txt, (40, 600))
                                                            if len(heroinventory) > 9:
                                                                item10_txt = font3.render("Item 10:" + str(heroinventory[9]), 10, WHITE)
                                                                screen.blit(item10_txt, (40, 625))
                        screen.blit(inventoryhub_title, (170, 100))
                        screen.blit(inv_weap_equipped_txt, (40, 300))
                        screen.blit(inv_items_titletxt, (40, 350))
                        screen.blit(e_close_txt, (40, 780))
                        pygame.display.flip()
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_e:  # when the 'e' key is pressed when inventory is open, it closes inventory
                                    openinv = False
                                elif event.key == K_1:  # number pressed corresponds with items in inventory-- to use items
                                    try:
                                        ui = heroinventory[0]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass

                                elif event.key == K_2:
                                    try:
                                        ui = heroinventory[1]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_3:
                                    try:
                                        ui = heroinventory[2]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_4:
                                    try:
                                        ui = heroinventory[3]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_5:
                                    try:
                                        ui = heroinventory[4]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_6:
                                    try:
                                        ui = heroinventory[5]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_7:
                                    try:
                                        ui = heroinventory[6]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_8:
                                    try:
                                        ui = heroinventory[7]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_9:
                                    try:
                                        ui = heroinventory[8]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_0:
                                    try:
                                        ui = heroinventory[9]
                                        itemdmg = 0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE,
                                                                        GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp) <= 0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
            elif event.type == MOUSEBUTTONDOWN:
                if option1.hovered == True:
                    cdmg = random.randint(0, hero.attack)
                    if cdmg == 0:
                        paction_txt = font2.render("You missed", 10, WHITE, GRAY)
                        screen.blit(paction_txt, (360, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        paction_txt1 = font2.render("You attacked and", 10, WHITE, GRAY)
                        paction_txt2 = font2.render("did " + str(cdmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 650))
                        screen.blit(paction_txt2, (400, 680))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    enemyhp = str(int(enemyhp) - cdmg)

                    if int(enemyhp) <= 0:
                        enemyhp = 0
                        paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                        paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 710))
                        screen.blit(paction_txt2, (400, 740))
                        pygame.display.flip()
                        clock.tick(60)
                        enemy_deathfx.play()
                        heroexp = str(int(heroexp) + enemy.exp)
                        enemiesdefeated+=1
                        stage=2
                        time.sleep(3)
                        lvl_up()
                        randomitem()
                    edmg = random.randint(0, enemy.attack)
                    if edmg == 0:
                        eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                        screen.blit(eaction_txt, (360, 350))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                        eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(eaction_txt1, (360, 350))
                        screen.blit(eaction_txt2, (360, 380))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    herohp = str(int(herohp) - edmg)
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option2.hovered == True:
                    paction_txt = font2.render("You defended", 10, WHITE, GRAY)
                    screen.blit(paction_txt, (360, 650))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(1.5)
                    edmg = random.randint(0, enemy.attack)
                    eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                    eaction_txt2 = font2.render("did " + str(edmg / 2) + " damage", 10, WHITE, GRAY)
                    screen.blit(eaction_txt1, (360, 350))
                    screen.blit(eaction_txt2, (360, 380))
                    pygame.display.flip()
                    clock.tick(60)
                    attackhit_fx.play()
                    time.sleep(2)
                    herohp = str(int(int(herohp) - (edmg / 2)))
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option3.hovered == True:
                    savegame()

        pygame.display.flip()
        clock.tick(60)
def randenemystage3():  #generates  enemy battles for stage 1
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain, attackhit_fx, inv_bg, stage
    stage=3
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    pygame.mixer.music.load('battle_theme.ogg')
    pygame.mixer.music.play(-1, 0)
    griffinImg=pygame.image.load('griffin_img.png')
    griffinImg=pygame.transform.scale(griffinImg, (250, 325))
    dragonIMG = pygame.image.load('dragon_img.png')
    dragonIMG = pygame.transform.scale(dragonIMG, (200, 275))
    demonIMG = pygame.image.load('demon_img.png')
    demonIMG = pygame.transform.scale(demonIMG, (250, 300))
    enums = "123"
    enmy = random.choice(enums)
    if enmy == "1":
        enemy = griffin()
        enemy_img=griffinImg
    elif enmy == "2":
        enemy = dragon()
        enemy_img=dragonIMG
    elif enmy == "3":
        enemy = demon()
        enemy_img=demonIMG
    enemyhp=str(enemy.hp)
    enemyname=enemy.name
    attackhit_fx = pygame.mixer.Sound('Swords_Collide-Sound.wav')
    attackmiss_fx=pygame.mixer.Sound('Swoosh_sound.wav')
    enemy_deathfx=pygame.mixer.Sound('enemy_death.wav')
    while True: #displays the player in the dungeon with hp and explaining controls
        player_hp_txt= font2.render("HP:"+herohp, 10, WHITE, GRAY)
        exp_txt = font2.render("XP:" + heroexp, 10, WHITE, GRAY)
        enemy_hp_txt= font2.render("HP:"+enemyhp, 10, WHITE, GRAY)
        enemy_name_txt= font2.render("Enemy:"+enemyname, 10, WHITE, GRAY)
        inventoryhub_txt = font2.render("Inventory['e']", 10, WHITE, GRAY)
        playerlvl_txt = font2.render("Player Level:" + playerlvl, 10, WHITE, GRAY)
        screen.blit(dungeonBGImg, (0, 0))
        screen.blit(character_viewImg, (200, 650))
        screen.blit(enemy_img, (200, 325))
        screen.blit(exp_txt, (500, 850))
        screen.blit(player_hp_txt,(40, 10))
        screen.blit(enemy_hp_txt, (200, 260))
        screen.blit(enemy_name_txt, (200, 220))
        screen.blit(playerlvl_txt, (375, 10))
        screen.blit(inventoryhub_txt,(5, 850))

        menu_font = pygame.font.Font(None, 42)
        attackBTN = [Option("ATTACK", (10, 200))]
        defendBTN = [Option("DEFEND", (10, 275))]
        saveBTN = [Option("SAVE", (75, 50))]
        for option1 in attackBTN:  # check to see if the quit button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in defendBTN:  # check to see if the save button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in saveBTN:  # check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_e:    #when the 'e' key is pressed, it pulls up the player's inventory
                    openinv = True
                    while openinv:
                        screen.blit(inv_bg, (0, 0))
                        font3 = pygame.font.SysFont("Times New Roman", 24)
                        font4 = pygame.font.SysFont("Times New Roman", 56)
                        e_close_txt = font3.render("Press [e] to close inventory", 10, WHITE)
                        inventoryhub_title = font4.render("Inventory", 10, WHITE)
                        player_stats_title = font3.render("Player Stats:", 10, WHITE)
                        player_stats_txt = font3.render(
                            "Hero Class: " + hero.pclass + "   HP: " + str(herohp) + "/" + str(
                                hero.maxhp) + "   Attack: " + str(hero.attack), 10, WHITE)
                        player_stats_txt1 = font3.render(
                            "LVL: " + str(playerlvl) + "   XP: " + str(heroexp) + "   Stage: " + str(
                                stage) + "   Enemies Defeated: " + str(enemiesdefeated), 10, WHITE)
                        screen.blit(player_stats_title, (40, 170))
                        screen.blit(player_stats_txt, (40, 210))
                        screen.blit(player_stats_txt1, (40, 250))
                        inv_weap_equipped_txt = font3.render(
                            "Weapon Equipped:" + str(hero.weapon) + " | Stats: " + weaponstats, 10, WHITE)
                        inv_items_titletxt = font3.render("Items: ", 10, WHITE)
                        if len(heroinventory)>0:
                            item1_txt=font3.render("Item 1:" + str(heroinventory[0]),10, WHITE)
                            screen.blit(item1_txt, (40, 400))
                            if len(heroinventory)>1:
                                item2_txt = font3.render("Item 2:" + str(heroinventory[1]), 10, WHITE)
                                screen.blit(item2_txt, (40, 425))
                                if len(heroinventory) > 2:
                                    item3_txt = font3.render("Item 3:" + str(heroinventory[2]), 10, WHITE)
                                    screen.blit(item3_txt, (40, 450))
                                    if len(heroinventory) > 3:
                                        item4_txt = font3.render("Item 4:" + str(heroinventory[3]), 10, WHITE)
                                        screen.blit(item4_txt, (40, 475))
                                        if len(heroinventory) > 4:
                                            item5_txt = font3.render("Item 5:" + str(heroinventory[4]), 10, WHITE)
                                            screen.blit(item5_txt, (40, 500))
                                            if len(heroinventory) >5:
                                                item6_txt = font3.render("Item 6:" + str(heroinventory[5]), 10, WHITE)
                                                screen.blit(item6_txt, (40, 525))
                                                if len(heroinventory) > 6:
                                                    item7_txt = font3.render("Item 7:" + str(heroinventory[6]), 10, WHITE)
                                                    screen.blit(item7_txt, (40, 550))
                                                    if len(heroinventory) >7:
                                                        item8_txt = font3.render("Item 8:" + str(heroinventory[7]), 10, WHITE)
                                                        screen.blit(item8_txt, (40, 575))
                                                        if len(heroinventory) > 8:
                                                            item9_txt = font3.render("Item 9:" + str(heroinventory[8]), 10, WHITE)
                                                            screen.blit(item9_txt, (40, 600))
                                                            if len(heroinventory) > 9:
                                                                item10_txt = font3.render("Item 10:" + str(heroinventory[9]), 10, WHITE)
                                                                screen.blit(item10_txt, (40, 625))
                        screen.blit(inventoryhub_title, (170, 100))
                        screen.blit(inv_weap_equipped_txt, (40, 300))
                        screen.blit(inv_items_titletxt, (40, 350))
                        screen.blit(e_close_txt, (40, 780))
                        pygame.display.flip()
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_e:  #when the 'e' key is pressed when inventory is open, it closes inventory
                                    openinv = False
                                elif event.key == K_1:                      #number pressed corresponds with items in inventory-- to use items
                                    try:
                                        ui = heroinventory[0]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass

                                elif event.key == K_2:
                                    try:
                                        ui = heroinventory[1]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False

                                    except IndexError:
                                        pass
                                elif event.key == K_3:
                                    try:
                                        ui = heroinventory[2]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_4:
                                    try:
                                        ui = heroinventory[3]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_5:
                                    try:
                                        ui = heroinventory[4]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False

                                    except IndexError:
                                        pass
                                elif event.key == K_6:
                                    try:
                                        ui = heroinventory[5]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_7:
                                    try:
                                        ui = heroinventory[6]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False

                                    except IndexError:
                                        pass
                                elif event.key == K_8:
                                    try:
                                        ui = heroinventory[7]
                                        openinv = False
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_9:
                                    try:
                                        ui = heroinventory[8]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_0:
                                    try:
                                        ui = heroinventory[9]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
            elif event.type == MOUSEBUTTONDOWN:
                if option1.hovered == True:
                    cdmg = random.randint(0, hero.attack)
                    if cdmg==0:
                        paction_txt = font2.render("You missed", 10, WHITE, GRAY)
                        screen.blit(paction_txt, (360, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        paction_txt1 = font2.render("You attacked and", 10, WHITE, GRAY)
                        paction_txt2 = font2.render("did " + str(cdmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 650))
                        screen.blit(paction_txt2, (400, 680))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    enemyhp = str(int(enemyhp) - cdmg)

                    if int(enemyhp)<=0:
                        enemyhp=0
                        paction_txt1 = font2.render("You slayed the ",10,WHITE, GRAY)
                        paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 710))
                        screen.blit(paction_txt2, (400, 740))
                        pygame.display.flip()
                        clock.tick(60)
                        enemy_deathfx.play()
                        heroexp=str(int(heroexp)+enemy.exp)
                        enemiesdefeated+=1
                        time.sleep(3)
                        lvl_up()
                        randomitem()
                    edmg = random.randint(0, enemy.attack)
                    if edmg==0:
                        eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                        screen.blit(eaction_txt, (360, 350))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                        eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(eaction_txt1, (360, 350))
                        screen.blit(eaction_txt2, (360, 380))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    herohp = str(int(herohp) - edmg)
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option2.hovered == True:
                    paction_txt = font2.render("You defended", 10, WHITE, GRAY)
                    screen.blit(paction_txt, (360, 650))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(1.5)
                    edmg = random.randint(0, enemy.attack)
                    eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                    eaction_txt2 = font2.render("did " + str(edmg/2) + " damage", 10, WHITE, GRAY)
                    screen.blit(eaction_txt1, (360, 350))
                    screen.blit(eaction_txt2, (360, 380))
                    pygame.display.flip()
                    clock.tick(60)
                    attackhit_fx.play()
                    time.sleep(2)
                    herohp= str(int(int(herohp)-(edmg/2)))
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option3.hovered == True:
                    savegame()

        pygame.display.flip()
        clock.tick(60)
def randenemystage2():  #generates  enemy battles for stage 1
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain, attackhit_fx, inv_bg, stage
    stage=2
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    pygame.mixer.music.load('battle_theme.ogg')
    pygame.mixer.music.play(-1, 0)
    armoredskeletonIMG=pygame.image.load('skeleton-image.png')
    armoredskeletonIMG=pygame.transform.scale(armoredskeletonIMG, (150, 250))
    orcIMG = pygame.image.load('orc_image.png')
    orcIMG = pygame.transform.scale(orcIMG, (200, 275))
    trollIMG = pygame.image.load('troll_image.png')
    trollIMG = pygame.transform.scale(trollIMG, (250, 300))
    undeadsoldierIMG = pygame.image.load('undead_soldier.png')
    undeadsoldierIMG = pygame.transform.scale(undeadsoldierIMG, (200, 300))
    enums = "1234"
    enmy = random.choice(enums)
    if enmy == "1":
        enemy = armoredskeleton()
        enemy_img=armoredskeletonIMG
    elif enmy == "2":
        enemy = orc()
        enemy_img=orcIMG
    elif enmy == "3":
        enemy = troll()
        enemy_img=trollIMG
    elif enmy == "4":
        enemy = undeadsoldier()
        enemy_img =undeadsoldierIMG
    enemyhp=str(enemy.hp)
    enemyname=enemy.name
    attackhit_fx = pygame.mixer.Sound('Swords_Collide-Sound.wav')
    attackmiss_fx=pygame.mixer.Sound('Swoosh_sound.wav')
    enemy_deathfx=pygame.mixer.Sound('enemy_death.wav')
    while True: #displays the player in the dungeon with hp and explaining controls
        player_hp_txt= font2.render("HP:"+herohp, 10, WHITE, GRAY)
        exp_txt = font2.render("XP:" + heroexp, 10, WHITE, GRAY)
        enemy_hp_txt= font2.render("HP:"+enemyhp, 10, WHITE, GRAY)
        enemy_name_txt= font2.render("Enemy:"+enemyname, 10, WHITE, GRAY)
        inventoryhub_txt = font2.render("Inventory['e']", 10, WHITE, GRAY)
        playerlvl_txt = font2.render("Player Level:" + playerlvl, 10, WHITE, GRAY)
        screen.blit(dungeonBGImg, (0, 0))
        screen.blit(character_viewImg, (200, 650))
        screen.blit(enemy_img, (200, 325))
        screen.blit(exp_txt, (500, 850))
        screen.blit(player_hp_txt,(40, 10))
        screen.blit(enemy_hp_txt, (200, 260))
        screen.blit(enemy_name_txt, (200, 220))
        screen.blit(playerlvl_txt, (375, 10))
        screen.blit(inventoryhub_txt,(5, 850))

        menu_font = pygame.font.Font(None, 42)
        attackBTN = [Option("ATTACK", (10, 200))]
        defendBTN = [Option("DEFEND", (10, 275))]
        saveBTN = [Option("SAVE", (75, 50))]
        for option1 in attackBTN:  # check to see if the quit button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in defendBTN:  # check to see if the save button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in saveBTN:  # check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_e:    #when the 'e' key is pressed, it pulls up the player's inventory
                    openinv = True
                    while openinv:
                        screen.blit(inv_bg, (0, 0))
                        font3 = pygame.font.SysFont("Times New Roman", 24)
                        font4 = pygame.font.SysFont("Times New Roman", 56)
                        e_close_txt = font3.render("Press [e] to close inventory", 10, WHITE)
                        inventoryhub_title = font4.render("Inventory", 10, WHITE)
                        player_stats_title = font3.render("Player Stats:", 10, WHITE)
                        player_stats_txt = font3.render( "Hero Class: " + hero.pclass + "   HP: " + str(herohp) + "/" + str(hero.maxhp) + "   Attack: " + str(hero.attack), 10, WHITE)
                        player_stats_txt1 = font3.render("LVL: " + str(playerlvl) + "   XP: " + str(heroexp) + "   Stage: " + str(stage) + "   Enemies Defeated: " + str(enemiesdefeated), 10, WHITE)
                        screen.blit(player_stats_title, (40, 170))
                        screen.blit(player_stats_txt, (40, 210))
                        screen.blit(player_stats_txt1, (40, 250))
                        inv_weap_equipped_txt = font3.render("Weapon Equipped:" + str(hero.weapon) + " | Stats: " + weaponstats, 10, WHITE)
                        inv_items_titletxt = font3.render("Items: ", 10, WHITE)
                        if len(heroinventory)>0:
                            item1_txt=font3.render("Item 1:" + str(heroinventory[0]),10, WHITE)
                            screen.blit(item1_txt, (40, 400))
                            if len(heroinventory)>1:
                                item2_txt = font3.render("Item 2:" + str(heroinventory[1]), 10, WHITE)
                                screen.blit(item2_txt, (40, 425))
                                if len(heroinventory) > 2:
                                    item3_txt = font3.render("Item 3:" + str(heroinventory[2]), 10, WHITE)
                                    screen.blit(item3_txt, (40, 450))
                                    if len(heroinventory) > 3:
                                        item4_txt = font3.render("Item 4:" + str(heroinventory[3]), 10, WHITE)
                                        screen.blit(item4_txt, (40, 475))
                                        if len(heroinventory) > 4:
                                            item5_txt = font3.render("Item 5:" + str(heroinventory[4]), 10, WHITE)
                                            screen.blit(item5_txt, (40, 500))
                                            if len(heroinventory) >5:
                                                item6_txt = font3.render("Item 6:" + str(heroinventory[5]), 10, WHITE)
                                                screen.blit(item6_txt, (40, 525))
                                                if len(heroinventory) > 6:
                                                    item7_txt = font3.render("Item 7:" + str(heroinventory[6]), 10, WHITE)
                                                    screen.blit(item7_txt, (40, 550))
                                                    if len(heroinventory) >7:
                                                        item8_txt = font3.render("Item 8:" + str(heroinventory[7]), 10, WHITE)
                                                        screen.blit(item8_txt, (40, 575))
                                                        if len(heroinventory) > 8:
                                                            item9_txt = font3.render("Item 9:" + str(heroinventory[8]), 10, WHITE)
                                                            screen.blit(item9_txt, (40, 600))
                                                            if len(heroinventory) > 9:
                                                                item10_txt = font3.render("Item 10:" + str(heroinventory[9]), 10, WHITE)
                                                                screen.blit(item10_txt, (40, 625))
                        screen.blit(inventoryhub_title, (170, 100))
                        screen.blit(inv_weap_equipped_txt, (40, 300))
                        screen.blit(inv_items_titletxt, (40, 350))
                        screen.blit(e_close_txt, (40, 780))
                        pygame.display.flip()
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_e:  #when the 'e' key is pressed when inventory is open, it closes inventory
                                    openinv = False
                                elif event.key == K_1:                      #number pressed corresponds with items in inventory-- to use items
                                    try:
                                        ui = heroinventory[0]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass

                                elif event.key == K_2:
                                    try:
                                        ui = heroinventory[1]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False

                                    except IndexError:
                                        pass
                                elif event.key == K_3:
                                    try:
                                        ui = heroinventory[2]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_4:
                                    try:
                                        ui = heroinventory[3]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_5:
                                    try:
                                        ui = heroinventory[4]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False

                                    except IndexError:
                                        pass
                                elif event.key == K_6:
                                    try:
                                        ui = heroinventory[5]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_7:
                                    try:
                                        ui = heroinventory[6]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False

                                    except IndexError:
                                        pass
                                elif event.key == K_8:
                                    try:
                                        ui = heroinventory[7]
                                        openinv = False
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_9:
                                    try:
                                        ui = heroinventory[8]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_0:
                                    try:
                                        ui = heroinventory[9]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
            elif event.type == MOUSEBUTTONDOWN:
                if option1.hovered == True:
                    cdmg = random.randint(0, hero.attack)
                    if cdmg==0:
                        paction_txt = font2.render("You missed", 10, WHITE, GRAY)
                        screen.blit(paction_txt, (360, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        paction_txt1 = font2.render("You attacked and", 10, WHITE, GRAY)
                        paction_txt2 = font2.render("did " + str(cdmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 650))
                        screen.blit(paction_txt2, (400, 680))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    enemyhp = str(int(enemyhp) - cdmg)

                    if int(enemyhp)<=0:
                        enemyhp=0
                        paction_txt1 = font2.render("You slayed the ",10,WHITE, GRAY)
                        paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 710))
                        screen.blit(paction_txt2, (400, 740))
                        pygame.display.flip()
                        clock.tick(60)
                        enemy_deathfx.play()
                        heroexp=str(int(heroexp)+enemy.exp)
                        enemiesdefeated+=1
                        time.sleep(3)
                        lvl_up()
                        randomitem()
                    edmg = random.randint(0, enemy.attack)
                    if edmg==0:
                        eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                        screen.blit(eaction_txt, (360, 350))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                        eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(eaction_txt1, (360, 350))
                        screen.blit(eaction_txt2, (360, 380))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    herohp = str(int(herohp) - edmg)
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option2.hovered == True:
                    paction_txt = font2.render("You defended", 10, WHITE, GRAY)
                    screen.blit(paction_txt, (360, 650))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(1.5)
                    edmg = random.randint(0, enemy.attack)
                    eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                    eaction_txt2 = font2.render("did " + str(edmg/2) + " damage", 10, WHITE, GRAY)
                    screen.blit(eaction_txt1, (360, 350))
                    screen.blit(eaction_txt2, (360, 380))
                    pygame.display.flip()
                    clock.tick(60)
                    attackhit_fx.play()
                    time.sleep(2)
                    herohp= str(int(int(herohp)-(edmg/2)))
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option3.hovered == True:
                    savegame()

        pygame.display.flip()
        clock.tick(60)

def randenemystage1():  #generates  enemy battles for stage 1
    global WHITE, screen, clock, hero, character_viewImg, herohp, heroexp, playerlvl, dungeonBGImg, enemiesdefeated, heroinventory, BLACK, weaponstats, ui, itemdmg, hpgain, attackhit_fx, inv_bg, stage
    stage=1
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    pygame.mixer.music.load('battle_theme.ogg')
    pygame.mixer.music.play(-1, 0)
    skeletonIMG=pygame.image.load('skeleton-image.png')
    skeletonIMG=pygame.transform.scale(skeletonIMG, (150, 250))
    goblinIMG = pygame.image.load('goblin_image.png')
    goblinIMG = pygame.transform.scale(goblinIMG, (150, 225))
    giantspiderIMG = pygame.image.load('giant_spider-image.png')
    giantspiderIMG = pygame.transform.scale(giantspiderIMG, (150, 200))
    enums = "123"
    enmy = random.choice(enums)
    if enmy == "1":
        enemy = Goblin()
        enemy_img=goblinIMG
    elif enmy == "2":
        enemy = Skeleton()
        enemy_img=skeletonIMG
    elif enmy == "3":
        enemy = GiantSpider()
        enemy_img=giantspiderIMG
    enemyhp=str(enemy.hp)
    enemyname=enemy.name
    attackhit_fx = pygame.mixer.Sound('Swords_Collide-Sound.wav')
    attackmiss_fx=pygame.mixer.Sound('Swoosh_sound.wav')
    enemy_deathfx=pygame.mixer.Sound('enemy_death.wav')
    while True: #displays the player in the dungeon with hp and explaining controls
        player_hp_txt= font2.render("HP:"+herohp, 10, WHITE, GRAY)
        exp_txt = font2.render("XP:" + heroexp, 10, WHITE, GRAY)
        enemy_hp_txt= font2.render("HP:"+enemyhp, 10, WHITE, GRAY)
        enemy_name_txt= font2.render("Enemy:"+enemyname, 10, WHITE, GRAY)
        inventoryhub_txt = font2.render("Inventory['e']", 10, WHITE, GRAY)
        playerlvl_txt = font2.render("Player Level:" + playerlvl, 10, WHITE, GRAY)
        screen.blit(dungeonBGImg, (0, 0))
        screen.blit(character_viewImg, (200, 650))
        screen.blit(enemy_img, (200, 325))
        screen.blit(exp_txt, (500, 850))
        screen.blit(player_hp_txt,(40, 10))
        screen.blit(enemy_hp_txt, (200, 260))
        screen.blit(enemy_name_txt, (200, 220))
        screen.blit(playerlvl_txt, (375, 10))
        screen.blit(inventoryhub_txt,(5, 850))

        menu_font = pygame.font.Font(None, 42)
        attackBTN = [Option("ATTACK", (10, 200))]
        defendBTN = [Option("DEFEND", (10, 275))]
        saveBTN = [Option("SAVE", (75, 50))]
        for option1 in attackBTN:  # check to see if the quit button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in defendBTN:  # check to see if the save button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in saveBTN:  # check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_e:    #when the 'e' key is pressed, it pulls up the player's inventory
                    openinv = True
                    while openinv:
                        screen.blit(inv_bg, (0, 0))
                        font3 = pygame.font.SysFont("Times New Roman", 24)
                        font4 = pygame.font.SysFont("Times New Roman", 56)
                        e_close_txt = font3.render("Press [e] to close inventory", 10, WHITE)
                        inventoryhub_title = font4.render("Inventory", 10, WHITE)
                        player_stats_title = font3.render("Player Stats:", 10, WHITE)
                        player_stats_txt = font3.render("Hero Class: " + hero.pclass + "   HP: " + str(herohp) + "/" + str(hero.maxhp) + "   Attack: " + str(hero.attack), 10, WHITE)
                        player_stats_txt1 = font3.render("LVL: " + str(playerlvl) + "   XP: " + str(heroexp) + "   Stage: " + str(stage) + "   Enemies Defeated: " + str(enemiesdefeated), 10, WHITE)
                        screen.blit(player_stats_title, (40, 170))
                        screen.blit(player_stats_txt, (40, 210))
                        screen.blit(player_stats_txt1, (40, 250))
                        inv_weap_equipped_txt = font3.render("Weapon Equipped:" + str(hero.weapon) + " | Stats: " + weaponstats, 10, WHITE)
                        inv_items_titletxt = font3.render("Items: ", 10, WHITE)
                        if len(heroinventory)>0:
                            item1_txt=font3.render("Item 1:" + str(heroinventory[0]),10, WHITE)
                            screen.blit(item1_txt, (40, 400))
                            if len(heroinventory)>1:
                                item2_txt = font3.render("Item 2:" + str(heroinventory[1]), 10, WHITE)
                                screen.blit(item2_txt, (40, 425))
                                if len(heroinventory) > 2:
                                    item3_txt = font3.render("Item 3:" + str(heroinventory[2]), 10, WHITE)
                                    screen.blit(item3_txt, (40, 450))
                                    if len(heroinventory) > 3:
                                        item4_txt = font3.render("Item 4:" + str(heroinventory[3]), 10, WHITE)
                                        screen.blit(item4_txt, (40, 475))
                                        if len(heroinventory) > 4:
                                            item5_txt = font3.render("Item 5:" + str(heroinventory[4]), 10, WHITE)
                                            screen.blit(item5_txt, (40, 500))
                                            if len(heroinventory) >5:
                                                item6_txt = font3.render("Item 6:" + str(heroinventory[5]), 10, WHITE)
                                                screen.blit(item6_txt, (40, 525))
                                                if len(heroinventory) > 6:
                                                    item7_txt = font3.render("Item 7:" + str(heroinventory[6]), 10, WHITE)
                                                    screen.blit(item7_txt, (40, 550))
                                                    if len(heroinventory) >7:
                                                        item8_txt = font3.render("Item 8:" + str(heroinventory[7]), 10, WHITE)
                                                        screen.blit(item8_txt, (40, 575))
                                                        if len(heroinventory) > 8:
                                                            item9_txt = font3.render("Item 9:" + str(heroinventory[8]), 10, WHITE)
                                                            screen.blit(item9_txt, (40, 600))
                                                            if len(heroinventory) > 9:
                                                                item10_txt = font3.render("Item 10:" + str(heroinventory[9]), 10, WHITE)
                                                                screen.blit(item10_txt, (40, 625))
                        screen.blit(inventoryhub_title, (170, 100))
                        screen.blit(inv_weap_equipped_txt, (40, 300))
                        screen.blit(inv_items_titletxt, (40, 350))
                        screen.blit(e_close_txt, (40, 780))
                        pygame.display.flip()
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_e:  #when the 'e' key is pressed when inventory is open, it closes inventory
                                    openinv = False
                                elif event.key == K_1:                      #number pressed corresponds with items in inventory-- to use items
                                    try:
                                        ui = heroinventory[0]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass

                                elif event.key == K_2:
                                    try:
                                        ui = heroinventory[1]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_3:
                                    try:
                                        ui = heroinventory[2]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_4:
                                    try:
                                        ui = heroinventory[3]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_5:
                                    try:
                                        ui = heroinventory[4]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False

                                    except IndexError:
                                        pass
                                elif event.key == K_6:
                                    try:
                                        ui = heroinventory[5]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_7:
                                    try:
                                        ui = heroinventory[6]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_8:
                                    try:
                                        ui = heroinventory[7]
                                        openinv = False
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_9:
                                    try:
                                        ui = heroinventory[8]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
                                elif event.key == K_0:
                                    try:
                                        ui = heroinventory[9]
                                        itemdmg=0
                                        use_inv_item()
                                        enemyhp = str(int(enemyhp) - itemdmg)
                                        if int(enemyhp) <= 0:
                                            enemyhp = 0
                                            paction_txt1 = font2.render("You slayed the ", 10, WHITE, GRAY)
                                            paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                                            screen.blit(paction_txt1, (400, 710))
                                            screen.blit(paction_txt2, (400, 740))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            enemy_deathfx.play()
                                            heroexp = str(int(heroexp) + enemy.exp)
                                            enemiesdefeated += 1
                                            time.sleep(3)
                                            lvl_up()
                                            randomitem()
                                        edmg = random.randint(0, enemy.attack)
                                        if edmg == 0:
                                            eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt, (360, 350))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackmiss_fx.play()
                                            time.sleep(1.5)
                                        else:
                                            eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                                            eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                                            screen.blit(eaction_txt1, (360, 350))
                                            screen.blit(eaction_txt2, (360, 380))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                        herohp = str(int(herohp) - edmg)
                                        if int(herohp)<=0:
                                            you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                                            screen.blit(you_died_txt, (245, 650))
                                            pygame.display.flip()
                                            clock.tick(60)
                                            attackhit_fx.play()
                                            time.sleep(2)
                                            herodeath()
                                        openinv = False
                                    except IndexError:
                                        pass
            elif event.type == MOUSEBUTTONDOWN:
                if option1.hovered == True:
                    cdmg = random.randint(0, hero.attack)
                    if cdmg==0:
                        paction_txt = font2.render("You missed", 10, WHITE, GRAY)
                        screen.blit(paction_txt, (360, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        paction_txt1 = font2.render("You attacked and", 10, WHITE, GRAY)
                        paction_txt2 = font2.render("did " + str(cdmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 650))
                        screen.blit(paction_txt2, (400, 680))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    enemyhp = str(int(enemyhp) - cdmg)

                    if int(enemyhp)<=0:
                        enemyhp=0
                        paction_txt1 = font2.render("You slayed the ",10,WHITE, GRAY)
                        paction_txt2 = font2.render(enemyname, 10, WHITE, GRAY)
                        screen.blit(paction_txt1, (400, 710))
                        screen.blit(paction_txt2, (400, 740))
                        pygame.display.flip()
                        clock.tick(60)
                        enemy_deathfx.play()
                        heroexp=str(int(heroexp)+enemy.exp)
                        enemiesdefeated+=1
                        time.sleep(3)
                        lvl_up()
                        randomitem()
                    edmg = random.randint(0, enemy.attack)
                    if edmg==0:
                        eaction_txt = font2.render("Enemy missed", 10, WHITE, GRAY)
                        screen.blit(eaction_txt, (360, 350))
                        pygame.display.flip()
                        clock.tick(60)
                        attackmiss_fx.play()
                        time.sleep(1.5)
                    else:
                        eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                        eaction_txt2 = font2.render("did " + str(edmg) + " damage", 10, WHITE, GRAY)
                        screen.blit(eaction_txt1, (360, 350))
                        screen.blit(eaction_txt2, (360, 380))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                    herohp = str(int(herohp) - edmg)
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option2.hovered == True:
                    paction_txt = font2.render("You defended", 10, WHITE, GRAY)
                    screen.blit(paction_txt, (360, 650))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(1.5)
                    edmg = random.randint(0, enemy.attack)
                    eaction_txt1 = font2.render("Enemy attacked and", 10, WHITE, GRAY)
                    eaction_txt2 = font2.render("did " + str(edmg/2) + " damage", 10, WHITE, GRAY)
                    screen.blit(eaction_txt1, (360, 350))
                    screen.blit(eaction_txt2, (360, 380))
                    pygame.display.flip()
                    clock.tick(60)
                    attackhit_fx.play()
                    time.sleep(2)
                    herohp= str(int(int(herohp)-(edmg/2)))
                    if int(herohp) <= 0:
                        you_died_txt = font1.render("YOU DIED!", 10, WHITE, GRAY)
                        screen.blit(you_died_txt, (245, 650))
                        pygame.display.flip()
                        clock.tick(60)
                        attackhit_fx.play()
                        time.sleep(2)
                        herodeath()
                elif option3.hovered == True:
                    savegame()

        pygame.display.flip()
        clock.tick(60)

def startgame():        #funciton starts the game off with the player in the dungeon
    global WHITE, screen, clock, hero, character_viewImg, herohp, playerlvl, heroexp, dungeonBGImg, background, heroinventory, BLACK, weaponstats,GRAY, inv_bg, stage
    #      R    G    B
    GRAY=(128, 128, 128)
    SBLUE=(70, 130, 180)
    pygame.mixer.music.load('Dungeon Theme.ogg')
    pygame.mixer.music.play(-1, 0)
    dungeonBGImg = pygame.image.load('original_dungeon_art.png')
    dungeonBGImg = pygame.transform.scale(dungeonBGImg, (600, 900))
    character_viewImg = pygame.image.load('3rd person character_view.png')
    character_viewImg = pygame.transform.scale(character_viewImg, (200, 250))
    inv_bg = pygame.image.load('inventory_bg.png')
    inv_bg = pygame.transform.scale(inv_bg, (600, 900))
    font1 = pygame.font.SysFont("sans bold", 36)
    font2 = pygame.font.SysFont("Times New Roman", 28)
    herohp=str(hero.hp)
    heroinventory=hero.inventory
    heroexp=str(hero.exp)
    playerlvl=str(hero.lvl)
    weaponstats='N/A'
    stage=0
    while True: #displays the player in the dungeon with hp and explaining controls
        screen.blit(dungeonBGImg,(0,0))
        screen.blit(character_viewImg,(200, 650))
        hp_txt= font2.render("HP:"+herohp, 10, WHITE, GRAY)
        screen.blit(hp_txt,(40, 10))
        exp_txt=font2.render("XP:"+heroexp, 10, WHITE, GRAY)
        screen.blit(exp_txt, (500,850))
        instructions_txt = font1.render("^ Use the save button to save game progress", 10, WHITE, SBLUE)
        instructions_txt1= font1.render("*Use the 'w' key to walk through", 10, WHITE, SBLUE)
        instructions_txt2= font1.render("doors when not in a battle*", 10, WHITE, SBLUE)
        instructions_txt3= font1.render("<- Use the attack button to attack an", 10, WHITE, SBLUE)
        instructions_txt4 = font1.render("enemy during a battle", 10, WHITE, SBLUE)
        instructions_txt5 = font1.render("<- Use the defend button to block half", 10, WHITE, SBLUE)
        instructions_txt6 = font1.render("the damage of an enemy during a battle", 10, WHITE, SBLUE)
        instructions_txt7= font1.render("*Use 'e' to open and close inventory and use the", 10, WHITE, SBLUE)
        instructions_txt8 = font1.render("number keys to use an item(max 10 items)*", 10, WHITE, SBLUE)
        inventoryhub_txt= font2.render("Inventory['e']", 10, WHITE, GRAY)
        playerlvl_txt = font2.render("Player Level:" + playerlvl, 10, WHITE, GRAY)
        screen.blit(playerlvl_txt, (375, 10))
        screen.blit(instructions_txt, (75, 100))
        screen.blit(instructions_txt1,(75, 400))        #displays instructions for controls
        screen.blit(instructions_txt2, (75, 450))
        screen.blit(inventoryhub_txt,(5, 850))
        screen.blit(instructions_txt3, (120, 195))
        screen.blit(instructions_txt4, (120, 230))
        screen.blit(instructions_txt5, (125, 275))
        screen.blit(instructions_txt6, (120, 310))
        screen.blit(instructions_txt7, (10, 525))
        screen.blit(instructions_txt8, (10, 565))
        attackBTN = [Option("ATTACK", (10, 200))]
        defendBTN = [Option("DEFEND", (10, 275))]
        saveBTN = [Option("SAVE", (75, 50))]
        inabattle=False
        for option1 in attackBTN:  # check to see if the attack button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in defendBTN:  # check to see if the defend button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in saveBTN:  # check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    font = pygame.font.SysFont("monospace", 56)
                    while True:
                        screen.fill(background)
                        stage1_txt=font.render("STAGE 1", 10, WHITE)
                        screen.blit(stage1_txt,(280, 425))
                        pygame.display.flip()
                        clock.tick(60)
                        time.sleep(1.5)
                        filler=True
                        if filler==True:
                            stage1()
                elif event.key == K_e:
                    openinv = True
                    while openinv:
                        screen.blit(inv_bg, (0,0))
                        font3 = pygame.font.SysFont("Times New Roman", 24)
                        font4 = pygame.font.SysFont("Times New Roman", 56)
                        e_close_txt=font3.render("Press [e] to close inventory", 10, WHITE)
                        inventoryhub_title = font4.render("Inventory", 10, WHITE)
                        player_stats_title= font3.render("Player Stats:",10,WHITE)
                        player_stats_txt = font3.render("Hero Class: " + hero.pclass + "   HP: " + str(herohp)+"/"+str(hero.maxhp) + "   Attack: " +  str(hero.attack), 10, WHITE)
                        player_stats_txt1= font3.render("LVL: "+ str(playerlvl) + "   XP: " + str(heroexp)+ "   Stage: " + str(stage) + "   Enemies Defeated: " + str(enemiesdefeated),10, WHITE)
                        screen.blit(player_stats_title,(40, 170))
                        screen.blit(player_stats_txt, (40, 210))
                        screen.blit(player_stats_txt1,(40, 250))
                        inv_weap_equipped_txt = font3.render("Weapon Equipped:" + str(hero.weapon) + " | Stats: " + weaponstats, 10, WHITE)
                        inv_items_titletxt = font3.render("Items: ", 10, WHITE)
                        if len(heroinventory)>0:
                            item1_txt=font3.render("Item 1:" + str(heroinventory[0]),10, WHITE)
                            screen.blit(item1_txt, (40, 400))
                            if len(heroinventory)>1:
                                item2_txt = font3.render("Item 2:" + str(heroinventory[1]), 10, WHITE)
                                screen.blit(item2_txt, (40, 425))
                                if len(heroinventory) > 2:
                                    item3_txt = font3.render("Item 3:" + str(heroinventory[2]), 10, WHITE)
                                    screen.blit(item3_txt, (40, 450))
                                    if len(heroinventory) > 3:
                                        item4_txt = font3.render("Item 4:" + str(heroinventory[3]), 10, WHITE)
                                        screen.blit(item4_txt, (40, 475))
                                        if len(heroinventory) > 4:
                                            item5_txt = font3.render("Item 5:" + str(heroinventory[4]), 10, WHITE)
                                            screen.blit(item5_txt, (40, 500))
                                            if len(heroinventory) >5:
                                                item6_txt = font3.render("Item 6:" + str(heroinventory[5]), 10, WHITE)
                                                screen.blit(item6_txt, (40, 525))
                                                if len(heroinventory) > 6:
                                                    item7_txt = font3.render("Item 7:" + str(heroinventory[6]), 10, WHITE)
                                                    screen.blit(item7_txt, (40, 550))
                                                    if len(heroinventory) >7:
                                                        item8_txt = font3.render("Item 8:" + str(heroinventory[7]), 10, WHITE)
                                                        screen.blit(item8_txt, (40, 575))
                                                        if len(heroinventory) > 8:
                                                            item9_txt = font3.render("Item 9:" + str(heroinventory[8]), 10, WHITE)
                                                            screen.blit(item9_txt, (40, 600))
                                                            if len(heroinventory) > 9:
                                                                item10_txt = font3.render("Item 10:" + str(heroinventory[9]), 10, WHITE)
                                                                screen.blit(item10_txt, (40, 625))
                        screen.blit(inventoryhub_title, (170, 100))
                        screen.blit(inv_weap_equipped_txt, (40, 300))
                        screen.blit(inv_items_titletxt, (40, 350))
                        screen.blit(e_close_txt, (40, 780))
                        pygame.display.flip()
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == K_e:
                                    openinv = False
                else:
                    pass
            elif event.type == MOUSEBUTTONDOWN:
                if inabattle==True:
                    if option1.hovered == True:
                        pass
                    elif option2.hovered == True:
                        pass
                if option3.hovered == True:
                    savegame()
                else:
                    pass
        pygame.display.flip()
        clock.tick(60)
def playerclass():                  #lets the player select a character class
    global WHITE, screen, menu_font, clock
    font1 = pygame.font.SysFont("monospace", 36)
    font2 = pygame.font.SysFont("monospace", 20)
    warriorImg = pygame.image.load('warrior_img.png')
    warriorImg = pygame.transform.scale(warriorImg, (100, 250))
    mageImg = pygame.image.load('mage_img.png')
    mageImg = pygame.transform.scale(mageImg, (150, 250))
    juggernautImg = pygame.image.load('juggernaut_img.png')
    juggernautImg = pygame.transform.scale(juggernautImg, (200, 250))
    backgrndImg = pygame.image.load('Brick-Background.png')
    backgrndImg = pygame.transform.scale(backgrndImg, (600, 900))
    menu_font = pygame.font.Font(None, 42)
    while True:
        screen.blit(backgrndImg, (0, 0))            #displays classes to choose from with corresponding class images
        screen.blit(warriorImg, (25, 150))
        screen.blit(juggernautImg, (175, 150))
        screen.blit(mageImg, (425, 150))
        warriorBTN = [Option("Warrior", (25, 500))]
        juggernautBTN = [Option("Juggernaut", (225, 500))]
        mageBTN = [Option("Mage", (450, 500))]
        instructions_txt = font1.render("Choose Your Class", 1, WHITE)
        screen.blit(instructions_txt, (100, 700))
        instructions_txt2= font2.render("<-- [Esc]", 1, WHITE)
        screen.blit(instructions_txt2, (15, 875))
        for option1 in warriorBTN:  # check to see if the warrior button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in juggernautBTN:  # check to see if the juggernaut button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in mageBTN:  # check to see if the mage button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type== pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    menu()
            elif event.type == MOUSEBUTTONDOWN:
                if option1.hovered == True:
                    Prof = Warrior()
                    return Prof
                elif option2.hovered == True:
                    Prof = Juggernaut()
                    return Prof
                elif option3.hovered == True:
                    Prof = Mage()
                    return Prof

        pygame.display.flip()
        clock.tick(60)

def choosehero():    #lets player choose character class
    global enemiesdefeated,hero, screen, clock, WHITE
    enemiesdefeated=0
    hero=playerclass()
    background = (0, 0, 0)
    font1 = pygame.font.SysFont("monospace", 24)
    explosion_fx=pygame.mixer.Sound('Explosion.ogg')
    while True: #the story intro
        screen.fill(background)
        explosion_fx.play()
        story_txt1=font1.render("There was an explosion from a cannon and",1,WHITE)
        story_txt2 = font1.render("you suddenly wake up in an underground ", 1, WHITE)
        story_txt3=font1.render("dungeon.", 1, WHITE)
        screen.blit(story_txt1,(10, 425))
        screen.blit(story_txt2, (10, 450))
        screen.blit(story_txt3, (10, 475))
        pygame.display.flip()
        clock.tick(60)
        time.sleep(5)
        story = True
        if story == True:
            startgame()
        clock.tick(60)

def menu(): #main menu function
    global screen, clock, menu_font, WHITE, titleImg, BLACK, GRAY, inv_bg, character_viewImg, dungeonBGImg
    pygame.mixer.music.load('Enspiron.mp3')
    pygame.mixer.music.play(-1, 0)
    #      R    G    B
    BLACK=(0,   0,   0)
    #      R    G    B
    GRAY = (128, 128, 128)
    inv_bg = pygame.image.load('inventory_bg.png')
    inv_bg = pygame.transform.scale(inv_bg, (600, 900))
    backgrndImg = pygame.image.load('Brick-Background.png')
    backgrndImg = pygame.transform.scale(backgrndImg, (600, 900))
    dungeonBGImg = pygame.image.load('original_dungeon_art.png')
    dungeonBGImg = pygame.transform.scale(dungeonBGImg, (600, 900))
    character_viewImg = pygame.image.load('3rd person character_view.png')
    character_viewImg = pygame.transform.scale(character_viewImg, (200, 250))
    menu_font = pygame.font.Font(None, 72)
    while True:
        screen.blit(backgrndImg,(0, 0))
        screen.blit(titleImg, (0, -200))
        startBTN = [Option("New Game", (175, 350))]
        loadBTN = [Option("Load Game", (175, 425))]
        quitBTN = [Option("Quit", (240, 500))]

        for option1 in startBTN:                 #check to see if the quit button is hovered by mouse
            if option1.rect.collidepoint(pygame.mouse.get_pos()):
                option1.hovered = True
            else:
                option1.hovered = False
            option1.draw()
        for option2 in loadBTN:                    #check to see if the save button is hovered by mouse
            if option2.rect.collidepoint(pygame.mouse.get_pos()):
                option2.hovered = True
            else:
                option2.hovered = False
            option2.draw()
        for option3 in quitBTN:                    #check to see if the save button is hovered by mouse
            if option3.rect.collidepoint(pygame.mouse.get_pos()):
                option3.hovered = True
            else:
                option3.hovered = False
            option3.draw()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if option1.hovered==True:   #if the player selects the New Game
                    choosehero()
                elif option2.hovered==True:
                    menu_font = pygame.font.Font(None, 42)
                    loadgame()
                elif option3.hovered==True:
                    pygame.quit()
                    sys.exit()
                    pass
        pygame.display.flip()
        clock.tick(60)

def titlescreen(): #displays title screen with game title and emblem
    global clock, screen, WHITE, titleImg
    pygame.mixer.music.load('Intro theme.ogg')
    pygame.mixer.music.play(-1, 0)
    titlebackgroundImg = pygame.image.load('brick_background.jpeg')
    titlebackgroundImg = pygame.transform.scale(titlebackgroundImg, (600, 900))
    titleImg=pygame.image.load('soul_of_chyra_title.png')
    titleImg = pygame.transform.scale(titleImg, (600, 900))
    title_emblemImg= pygame.image.load('emblem.png')
    font1 = pygame.font.SysFont("monospace", 20)
    while True:
        screen.blit(titlebackgroundImg, (0, 0))
        screen.blit(title_emblemImg,(-40, 250))
        screen.blit(titleImg, (0, -100))
        instructions_txt = font1.render("<Press space to continue>", 1, WHITE)
        screen.blit(instructions_txt, (175, 850))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    menu()
                else:
                    pass
        pygame.display.flip()
        clock.tick(60)
def introscreen():  #displays the intro screen with game intro text
    global screen, clock, WHITE, background, menu_font
    #           R     G     B
    background=(0,    0,    0)
    WHITE=     (255, 255, 255)
    window_width = 600
    window_height = 900
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('The Soul of Chyra')
    title_emblemIcon = pygame.image.load('crossed_swords_ico.png')
    title_emblemIcon = pygame.transform.scale(title_emblemIcon, (32, 32))
    pygame.display.set_icon(title_emblemIcon)
    menu_font = pygame.font.Font(None, 72)
    while True:
        screen.fill(background)
        font1 = pygame.font.SysFont("monospace", 20)
        intro_txt1 = font1.render("In a world...", 1, WHITE)
        intro_txt2 =font1.render("..where one soul is left to die after the", 1, WHITE)
        intro_txt3= font1.render("Great War has destroyed the city of Chyra.", 1, WHITE)
        screen.blit(intro_txt1, (15, 100,))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(2)
        screen.blit(intro_txt2, (15, 150,))
        screen.blit(intro_txt3, (15, 200,))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(5)
        introdone = True
        if introdone==True:
            titlescreen()
        clock.tick(60)
introscreen()