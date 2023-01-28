##CURRENT VERSION 8.30pm 27/1/23

#great - just fix up ending "you won" screen
#put in a restart and quit button
import pygame
import time

#may or may not use this
import pygame.gfxdraw

from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

#set up the display screen
screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The House of Belladonna')

#define the game variables
clock = pygame.time.Clock()
fps = 60
#Note: change name to font3 later
font3=pygame.font.Font("./FINAL_IMG/FONTS/Golden_Age.ttf",30)
white = (255,255,255)


tile_size = 25
game_over=0
flying=0
main_menu = True
potions = 0
books = 0
herbs = 0
crystals = 0
wand=0
level = 1
lives =3
spells=[]
vamp_lives=0
win=0

#Load images
bg_img = pygame.image.load("./FINAL_IMG/BACKGROUND/ROOM.png")

title_img=pygame.image.load("./FINAL_IMG/BANNERS AND BUTTONS/TITLE_SLIDE_FULL.png")
title_img = pygame.transform.scale(title_img, (1000, 600))

defeat_img=pygame.image.load("./FINAL_IMG/BANNERS AND BUTTONS/DEFEAT_COUNT.png")
defeat_img = pygame.transform.scale(defeat_img, (1000, 600))

flyinginst_img=pygame.image.load("./FINAL_IMG/BANNERS AND BUTTONS/FLYING_INST.png")
flyinginst_img = pygame.transform.scale(flyinginst_img, (500, 95))

wandinst_img=pygame.image.load("./FINAL_IMG/BANNERS AND BUTTONS/WAND_INST2.png")
wandinst_img = pygame.transform.scale(wandinst_img, (800, 80))

restart_img = pygame.image.load("./FINAL_IMG/BANNERS AND BUTTONS/RESTART_BUTTON.png")
restart_img = pygame.transform.scale(restart_img, (200, 85))
game_over_img= pygame.image.load("./FINAL_IMG/BANNERS AND BUTTONS/GAME_OVER_2.png")
game_over_img = pygame.transform.scale(game_over_img, (500, 250))

start_img = pygame.image.load("./FINAL_IMG/BANNERS AND BUTTONS/START_BUTTON.png")
start_img = pygame.transform.scale(start_img, (250, 100))

potion_score = pygame.image.load("./FINAL_IMG/SPRITES/POTION2.png")
potion_score = pygame.transform.scale(potion_score, (30, 40))

book_score = pygame.image.load("./FINAL_IMG/SPRITES/BOOK.png")
book_score = pygame.transform.scale(book_score, (35, 40))
herb_score=pygame.image.load("./FINAL_IMG/SPRITES/HERB2.png")
herb_score = pygame.transform.scale(herb_score, (40, 40))
crystal_score=pygame.image.load("./FINAL_IMG/SPRITES/CRYSTAL.png")
crystal_score = pygame.transform.scale(crystal_score, (40, 40))

#load sounds
#downloaded from https://opengameart.org/content/50-cc0-retro-synth-sfx
jump_fx=pygame.mixer.Sound("./FINAL_SOUNDS/jump.ogg")
#jump_fx.set_volume(0.5)#means 50% of original volume if needed

#collect potion
potions_fx=pygame.mixer.Sound("./FINAL_SOUNDS/score.ogg")

lost_life_fx=pygame.mixer.Sound("./FINAL_SOUNDS/retro_misc_05.ogg")

defeat_count=pygame.mixer.Sound("./FINAL_SOUNDS/life.ogg")



#BROOM SOUNDS FROM: Credit isn't necessary. If you want to give credit anyway, it can be attributed to "Ctskelgysth Inauaruat", "Ctskelgysth", or just "Ctske" depending on space limitations and what works best for your project.
##broom_fx=pygame.mixer.Sound("./FINAL_SOUNDS/square_partyjoin.ogg")
broom_fx=pygame.mixer.Sound("./FINAL_SOUNDS/positive.ogg")

wand_fx=pygame.mixer.Sound("./FINAL_SOUNDS/power_up_04.ogg")



#animal_fx
# SOUNDS FROM: Credit isn't necessary. If you want to give credit anyway, it can be attributed to "Ctskelgysth Inauaruat", "Ctskelgysth", or just "Ctske" depending on space limitations and what works best for your project.

animal_fx=pygame.mixer.Sound("./FINAL_SOUNDS/square_partyjoin.ogg")

#final round fx
final_fx=pygame.mixer.Sound("./FINAL_SOUNDS/warning.ogg")
final2_fx=pygame.mixer.Sound("./FINAL_SOUNDS/evil_laugh.ogg")
spell_fx=pygame.mixer.Sound("./FINAL_SOUNDS/twink.ogg")

#die
die_fx=pygame.mixer.Sound("./FINAL_SOUNDS/die.ogg")

#ambient horror sounds from Copyright/Attribution Notice: Attribute Little Robot Sound Factory, and provide this link where possible: www.littlerobotsoundfactory.com
pygame.mixer.music.load("./FINAL_SOUNDS/Ambience_Hell_01.ogg")
pygame.mixer.music.play(-1, 0.0,5000)




#create function to write text on screen

def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


#create classes
class Button():
        def __init__(self, x, y, image):
                self.image = image
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.click = False #detects if mouse button has been clicked
        def draw(self):
                action = False #whatever the mouse button does
                #get mouse position
                pos = pygame.mouse.get_pos() #will give x and y coordinates of mouse

                #check mouseover and clicked conditions
                if self.rect.collidepoint(pos): #checking for collision between button rect and mouse point
                        if pygame.mouse.get_pressed()[0]==1 and self.click==False: #looking for left mouse click which is 0
                                action = True
                                self.click = True
                              
                if pygame.mouse.get_pressed()[0]==0:
                        self.click=False
                #draw button
                screen.blit(self.image, self.rect)
                return action

class Player():
        def __init__(self, x, y):
                self.reset(x,y)

        def update(self, flying, game_over):
        
                dx = 0
                dy = 0

                walk_cooldown = 5
                fly_cooldown = 5


                if flying==0 and game_over==0:
                        #get keypresses
                        key = pygame.key.get_pressed()
                        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                                jump_fx.play()
                                self.vel_y = -15
                                self.jumped = True
                        if key[pygame.K_SPACE] == False:
                                self.jumped = False
                        if key[pygame.K_LEFT]:
                                dx -= 5
                                self.counter += 1
                                self.direction = -1
                        if key[pygame.K_RIGHT]:
                                dx += 5
                                self.counter += 1
                                self.direction = 1
                        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                                self.counter = 0
                                self.index = 0
                                if self.direction == 1:
                                        self.image = self.images_right[self.index]
                                if self.direction == -1:
                                        self.image = self.images_left[self.index]

                        #handle animation
                                        #troubleshooting commenting this out
                        if self.counter > walk_cooldown:
                                self.counter = 0        
                                self.index += 1
                                if self.index >= len(self.images_right):
                                        self.index = 0
                                if self.direction == 1:
                                        self.image = self.images_right[self.index]
                                if self.direction == -1:
                                        self.image = self.images_left[self.index]

                        #add gravity
                        self.vel_y += 1
                        if self.vel_y > 10:
                                self.vel_y = 10
                        dy += self.vel_y

                        #check for collision

                        self.in_air=True
                        for tile in world.tile_list:
                            #check for collision in x direction
                            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                    dx = 0
                            #check for collision in y direction
                            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                    #check if below the ground i.e. jumping
                                    if self.vel_y < 0:
                                            dy = tile[1].bottom - self.rect.top
                                            self.vel_y = 0
                                    #check if above the ground i.e. falling
                                    elif self.vel_y >= 0:
                                            dy = tile[1].top - self.rect.bottom
                                            self.vel_y = 0
                                            self.in_air=False

                        #check for collision with enemies

                        #check if collect broomstick
                        for broom in broom_group:
                                if pygame.sprite.spritecollide(self, broom_group, True):
                                        broom_group.remove(broom)
                                        broom_group.draw(screen)
                                        flying = 1
                                        broom_fx.play(loops=0)
                                
                        #update player coordinates
                        self.rect.x += dx
                        self.rect.y += dy

                        if self.rect.bottom > screen_height:
                                self.rect.bottom = screen_height

                                dy = 0
                
                elif flying ==1 and game_over==0:

                    
                    #new line here
                    if level==1:
                            screen.blit(flyinginst_img, (200,500))

                    #get keypresses
                    key = pygame.key.get_pressed()

                    if key[pygame.K_LEFT]:
                            dx -= 5
                            self.counter += 1
                            self.direction = -1
                    if key[pygame.K_RIGHT]:
                            dx += 5
                            self.counter += 1
                            self.direction = 1
                    if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                            self.counter = 0
                            self.fly_index = 0
                            if self.direction == 1:
                                    self.image = self.fly_images_right[self.fly_index]
                            if self.direction == -1:
                                    self.image = self.fly_images_left[self.fly_index]
                    #flying                
                    if key[pygame.K_UP]:
                            dy -= 5
                            self.counter += 1
                            self.direction = -1
                    if key[pygame.K_DOWN]:
                            dy += 5
                            self.counter += 1
                            self.direction = 1

                    #handle animation
                    if self.counter > fly_cooldown:
                            self.counter = 0        
                            self.fly_index += 1
                            if self.fly_index >= len(self.fly_images_right):
                                    self.fly_index = 0
                            if self.direction == 1:
                                    self.image = self.fly_images_right[self.fly_index]
                            if self.direction == -1:
                                    self.image = self.fly_images_left[self.fly_index]
                  #check for collision in level 1 world:
                    self.in_air=True
                    for tile in world.tile_list:
                                #check for collision in x direction
                        if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                dx = 0
                                #check for collision in y direction
                        if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                dy = 0

                    if pygame.sprite.spritecollide(self, spider_group, False):
                            game_over = -1
                            die_fx.play()


                    #new line
                    if pygame.sprite.spritecollide(self, bat_group, False):
                            game_over = -1
                            die_fx.play()

                    #update coordinates

                    self.rect.x += dx
                    self.rect.y += dy

                #draw player onto screen
                screen.blit(self.image, self.rect)
##                pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

                return flying


        def lost_life(self, lives):

            if pygame.sprite.spritecollide(self, spider_group, False):
                lost_life_fx.play(loops=0)
                lives -= 1
                self.reset(100, screen_height - 130)
                broom_group.draw(screen)

            if pygame.sprite.spritecollide(self, bat_group, False):
                lost_life_fx.play(loops=0)
                lives -= 1
                self.reset(30, screen_height - 130)
                broom_group.draw(screen)
                level3_action=False
                
            if pygame.sprite.spritecollide(self, final_bat_group, False):
                lost_life_fx.play(loops=0)
                lives -= 1
                self.reset(100, screen_height - 100)
                level3_action=False

            if pygame.sprite.spritecollide(self, final_spider_group, False):
                lost_life_fx.play(loops=0)
                lives -= 1
                self.reset(100, screen_height - 100)
                level3_action=False

            if pygame.sprite.spritecollide(self, vampire_group, False):
                lost_life_fx.play(loops=0)
                lives -= 1
                self.reset(100, screen_height - 100)
                level3_action=False
                    
            #draw player onto screen
            screen.blit(self.image, self.rect)
                   
            return lives


        def wand(self, wand):
            if pygame.sprite.spritecollide(self, wand_group, True):
                wand_fx.play(loops=0)
                self.images_right = []
                self.images_left = []
                wand=1

                for num in range(1, 5):
                        img_right = pygame.image.load(f'./FINAL_IMG/SPRITES/wandwitch{num}.png')
                        img_right = pygame.transform.scale(img_right, (60, 100))
                        img_left = pygame.transform.flip(img_right, True, False)
                        self.images_right.append(img_right)
                        self.images_left.append(img_left)
              
            return wand
                
        def reset(self, x, y):
            #regular images
                self.images_right = []
                self.images_left = []
                #flying images
                self.fly_images_right = []
                self.fly_images_left = []
                self.index = 0
                #flying index
                self.fly_index = 0
                self.counter = 0

                #regular images
                for num in range(1, 5):
                        img_right = pygame.image.load(f'./FINAL_IMG/SPRITES/witch{num}.png')
                        img_right = pygame.transform.scale(img_right, (60, 100))
                        img_left = pygame.transform.flip(img_right, True, False)
                        self.images_right.append(img_right)
                        self.images_left.append(img_left)

                #flying images
                for num in range(1, 4):
                    fly_right = pygame.image.load(f'./FINAL_IMG/SPRITES/WITCHFLY{num}.png')
                    fly_right = pygame.transform.scale(fly_right, (60, 100))
                    fly_left = pygame.transform.flip(fly_right, True, False)
                    self.fly_images_right.append(fly_right)
                    self.fly_images_left.append(fly_left)

##                self.dead_image = pygame.image.load("death.png")
##                self.dead_image = pygame.transform.scale(self.dead_image, (80,80))
                

                self.image = self.images_right[self.index]
                #same for flying
                self.fly_image = self.fly_images_right[self.fly_index]

                
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.width = self.image.get_width()
                self.height = self.image.get_height()
                self.vel_y = 0
                self.jumped = False
                self.direction = 0
                self.in_air = True #so player can't keep jumping indefinitely



class World():
        def __init__(self, data):
                self.tile_list = []

                #load images
##                dirt_img = pygame.image.load('./img/dirt.png')
##                grass_img = pygame.image.load('./img/grass.png')
                left_shelf=pygame.image.load("./FINAL_IMG/TILES/SHELF_LEFT.png")
                mid_shelf=pygame.image.load("./FINAL_IMG/TILES/SHELF_MID.png")
                right_shelf=pygame.image.load("./FINAL_IMG/TILES/SHELF_RIGHT.png")
                tl_corn=pygame.image.load("./FINAL_IMG/TILES/TL_CORN.png")
                tr_corn=pygame.image.load("./FINAL_IMG/TILES/TR_CORN.png")

                l_up=pygame.image.load("./FINAL_IMG/TILES/L_UP.png")
                r_up=pygame.image.load("./FINAL_IMG/TILES/R_UP.png")


                top=pygame.image.load("./FINAL_IMG/TILES/TOP.png")



                brick_img = pygame.image.load("./FINAL_IMG/TILES/STEP.png")
                tomb_img = pygame.image.load("./FINAL_IMG/SPRITES/TOMBSTONE3.png")
                web_img = pygame.image.load("./FINAL_IMG/SPRITES/WEB.png")
                branch3= pygame.image.load("./FINAL_IMG/SPRITES/BRANCH3.png")
                bigbranch= pygame.image.load("./FINAL_IMG/SPRITES/BIGBRANCH1.png")
                mid_img = pygame.image.load("./FINAL_IMG/TILES/MIDNIGHT.png")
                trunk_img = pygame.image.load("./FINAL_IMG/TILES/TRUNK.png")
                
                row_count = 0
                for row in data:
                        col_count = 0
                        for tile in row:
                                if tile == 2:
                                        img = pygame.transform.scale(brick_img, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)


                                if tile == 21:
                                        img = pygame.transform.scale(left_shelf, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)


                                if tile == 24:
                                        img = pygame.transform.scale(mid_shelf, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)
                                if tile == 23:
                                        img = pygame.transform.scale(right_shelf, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)



                                if tile == 25:
                                        img = pygame.transform.scale(tl_corn, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)



                                if tile == 26:
                                        img = pygame.transform.scale(l_up, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)


                                if tile == 28:
                                        img = pygame.transform.scale(tr_corn, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)

                                if tile == 27:
                                        img = pygame.transform.scale(top, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)
                                if tile == 29:
                                        img = pygame.transform.scale(r_up, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)



                                if tile == 60:
                                        img = pygame.transform.scale(bigbranch, (140, 40))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                if tile == 62:
                                        img = pygame.transform.scale(branch3, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                if tile == 4:
                                        img = pygame.transform.scale(tomb_img, (75, 100))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                if tile == 32:
                
                                        img = pygame.transform.scale(trunk_img, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)

                                if tile == 17:
                
                                        img = pygame.transform.scale(web_img, (2.5*tile_size, 2*tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)


                                if tile == 31:
                                        img = pygame.transform.scale(branch_img, (tile_size, tile_size/2))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        self.tile_list.append(tile)
                                
                                if tile ==3:
                                        spider = Enemy(col_count*tile_size, row_count*tile_size)
                                        spider_group.add(spider)



                                if tile ==39:
                                        final_spider = Final_Spider(col_count*tile_size, row_count*tile_size)
                                        final_spider_group.add(final_spider)
                                        
                                if tile ==22:
                                        bat = Bat(col_count*tile_size, row_count*tile_size)
                                        bat_group.add(bat)

                                if tile ==19:
                                        owl = Owl([owl_image1, owl_image2], col_count*tile_size, row_count*tile_size)
                                        owl_group.add(owl)

                                if tile ==5:
                                        potion =Potion(col_count*tile_size, row_count*tile_size)
                                        potion_group.add(potion)
                                if tile ==6:
                                        herb =Herb(col_count*tile_size, row_count*tile_size)
                                        herb_group.add(herb)

                                if tile ==1:
                                        crystal =Crystal(col_count*tile_size, row_count*tile_size)
                                        crystal_group.add(crystal)
                                        
                                if tile == 7:
                                        img = pygame.transform.scale(mid_img, (tile_size, tile_size))
                                        img_rect = img.get_rect()
                                        img_rect.x = col_count * tile_size
                                        img_rect.y = row_count * tile_size
                                        tile = (img, img_rect)
                                        
                                        self.tile_list.append(tile)

                                if tile ==9:
                                        book = Book(col_count*tile_size, row_count*tile_size)
                                        book_group.add(book)

                                if tile ==13:
                                        cat = Cat([cat_image1, cat_image2], col_count*tile_size, row_count*tile_size)
                                        cat_group.add(cat)

                                if tile ==99:
                                        vampire = Vampire(col_count*tile_size, row_count*tile_size)
                                        vampire_group.add(vampire)
                        
                                if tile ==33:
                                        final_bat = Final_Bat(col_count*tile_size, row_count*tile_size)
                                        final_bat_group.add(final_bat)
                                col_count += 1
                        row_count += 1

        def draw(self):
                for tile in self.tile_list:
                        screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                #change image for now
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/SPIDER.png")
                self.image = pygame.transform.scale(self.image, (53, 30))
                self.rect = self.image.get_rect()
                self.rect.x =x
                self.rect.y = y #positions enemy at coordinates supplies, maybe add pixels
                self.move_direction = 1
                self.move_count =0
                
        def update (self):
                self.rect.x += self.move_direction
                self.move_count += 1
                if self.move_count > 50:
                        self.move_direction *= -1
                        self.move_count =0


class Bat(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/BAT2.png")
                self.image = pygame.transform.scale(self.image, (86, 44))
                self.rect = self.image.get_rect()
                self.rect.x =x
                self.rect.y = y #positions enemy at coordinates supplies, maybe add pixels
                self.move_direction = 1
                self.move_count =0
                
        def update (self):
                self.rect.y += self.move_direction
                self.move_count += 1
                if self.move_count > 200:
                        self.move_direction *= -1
                        self.move_count =0

class Potion(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/POTION2.png")
                self.image = pygame.transform.scale(self.image, (48, 50))
                self.rect = self.image.get_rect(center=(x,y))


class Book(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/BOOK.png")
                self.image = pygame.transform.scale(self.image, (40, 50))
                self.rect = self.image.get_rect()
                self.rect.x=x
                self.rect.y=y


class Herb(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/HERB.png")
                self.image = pygame.transform.scale(self.image, (77, 70))
                self.rect = self.image.get_rect()
                self.rect.x=x
                self.rect.y=y


class Crystal(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/CRYSTAL.png")
                self.image = pygame.transform.scale(self.image, (75, 75))
                self.rect = self.image.get_rect()
                self.rect.x=x
                self.rect.y=y
                
class Wand(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/wand.png")
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.rect = self.image.get_rect()
                self.rect.x=x
                self.rect.y=y



class Broom(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/BROOM.png")
                self.image = pygame.transform.scale(self.image, (75, 75))
                self.rect = self.image.get_rect()
                self.rect.x=x
                self.rect.y=y

cat_image1 = pygame.image.load("./FINAL_IMG/SPRITES/CAT.png")
cat_image1 = pygame.transform.scale(cat_image1, (85, 85))
cat_image2 = pygame.image.load("./FINAL_IMG/SPRITES/CAT2.png")
cat_image2 = pygame.transform.scale(cat_image2, (85, 85))

class Cat(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        super().__init__()
        self.images = images
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 500 # animation speed in ms

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]




owl_image1 = pygame.image.load("./FINAL_IMG/SPRITES/OWL.png")
owl_image1 = pygame.transform.scale(owl_image1, (75, 75))
owl_image2 = pygame.image.load("./FINAL_IMG/SPRITES/OWL.png")
owl_image2 = pygame.transform.scale(owl_image2, (75, 78))

class Owl(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        super().__init__()
        self.images = images
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 500 # animation speed in ms

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[self.current_image]


class Vampire(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                #change image for now
                self.image = pygame.image.load("./FINAL_IMG/SPRITES/THE_COUNT.png")
                self.image = pygame.transform.scale(self.image, (65, 100))
                self.rect = self.image.get_rect()
                self.rect.x =x
                self.rect.y = y #positions enemy at coordinates supplies, maybe add pixels
                self.move_direction = 1
                self.move_count =0
##                pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
                
        def update (self):
##                pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
                self.rect.x += self.move_direction
                self.move_count += 1
                if self.move_count > 100:
                        self.move_direction *= -1
                        self.move_count =0

class Final_Bat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./FINAL_IMG/SPRITES/BAT2.png")
        self.image = pygame.transform.scale(self.image, (86, 44))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_pos = (x, y)


    def reset(self):
        self.rect.x, self.rect.y = self.original_pos

    def update(self):
        if self.rect.x <500:
            self.rect.x -= 1# move the sprite to the left
            self.rect.y +=1
        elif self.rect.x >500:
            self.rect.x += 1# move the sprite to the left
            self.rect.y +=1
        if self.rect.x < -50 or self.rect.x > 1050:  # if the sprite is off the left side of the screen
                self.reset()

class Final_Spider(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./FINAL_IMG/SPRITES/SPIDER.png")
        self.image = pygame.transform.scale(self.image, (53, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_pos = (x, y)


    def reset(self):
        self.rect.x, self.rect.y = self.original_pos

    def update(self):
        self.rect.y +=1
        if self.rect.y > 650:  # if the sprite is off the screen
                self.reset()


class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (255,0,0,28), (self.x, self.y), 10)
        self.rect = self.image.get_rect(center=(x,y))
        self.vel_x = vel_x
        self.vel_y = vel_y
        
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.x=self.x
        self.rect.y=self.y
                
world_data=[
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,21,24,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,21,24,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,9,0,9,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,21,24,23,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,21,24,23,0,0,0,0,0,0,0,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,24,24,24,24,24,24,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,27,27,27,27,27,27,27,27,2],
[2,9,0,0,0,0,0,0,0,21,24,23,0,0,0,0,0,21,24,23,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2],
[2,24,24,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,27,27,2,2,2,2,2,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,27,27,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
]


world_data_2=[
[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],
[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,19,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,60,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,60,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,60,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,4,0,0,0,0,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,62],
[7,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62],
[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],
]

world_data_3=[
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,33,0,0,0,0,0,0,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,99,33,0,0,0,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,39,0,0,0,39,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,27,27,27,27,27,27,28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,29,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,25,27,27,2,2,2,2,2,2,2,2,27,27,28,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2,2,2,2,29,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,39,0,26,2,2,2,2,2,2,2,2,2,2,2,2,29,39,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,25,27,27,2,2,2,2,2,2,2,2,2,2,2,2,2,2,27,27,28,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,29,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,27,28,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,25,27,27,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,29,0,0,0,0,0,0,0,0,0,0,0,2],
[2,27,27,27,27,27,27,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,29,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,27,27,27,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,25,27,27,27,2,2,2,2,2],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,2,2,2,2,2,2,2,2],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
]



player = Player(100, screen_height - 100)

spider_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
broom_group = pygame.sprite.Group()
book_group = pygame.sprite.Group()
cat_group = pygame.sprite.Group()
herb_group = pygame.sprite.Group()
crystal_group = pygame.sprite.Group()
bat_group = pygame.sprite.Group()
owl_group = pygame.sprite.Group()
vampire_group = pygame.sprite.Group()
wand_group = pygame.sprite.Group()

final_bat_group = pygame.sprite.Group()
final_spider_group = pygame.sprite.Group()
spells_group=pygame.sprite.Group()

world = World(world_data)

#create buttons
restart_button=Button(350,450, restart_img)
start_button = Button(350, 480, start_img)

broom1=Broom(425, 300)
broom2=Broom(75, 130)

potion1=Potion(540, 160)
potion2=Potion(385, 260)
potion3=Potion(635, 235)


wands=Wand(950,450)

level1_action = False
level2_action = False
level3_action = False
win_action = False
#this will help with the wand appearing
lost_life= False
lost_life1=False

run = True

while run:
        if pygame.sprite.spritecollide(player, cat_group, False):

            animal_fx.play(loops=0)
            level += 1

            flying =0
            player.reset(50, screen_height - 50)

        if pygame.sprite.spritecollide(player, owl_group, False):

            level += 1
            bat_group.empty()
            owl_group.empty()
            herb_group.empty()
            crystal_group.empty()
            final_fx.play(loops=0)
            final2_fx.play(loops=0)

            flying =0
            player.reset(50, screen_height - 15)



        clock.tick(fps)        
        screen.blit(bg_img, (0, 0))

        if main_menu==True:
                screen.blit(title_img, (0, 0))
                if start_button.draw():
                        main_menu = False

        else:
            if level==1 and not level1_action:
                broom_group.add(broom1)
                potion_group.add(potion1)
                potion_group.add(potion2)
                potion_group.add(potion3)


                level1_action=True
            elif level==1 and level1_action:
                    world.draw()
                    spider_group.update()
                    for cat in cat_group:
                            cat.animate()

                    spider_group.draw(screen)
                    potion_group.draw(screen)
                    broom_group.draw(screen)
                    book_group.draw(screen)
                    cat_group.draw(screen)
                                   
            elif level==2 and not level2_action:
                broom_group.add(broom2)
                spider_group.empty() 
                potion_group.empty() 
                book_group.empty() 
                cat_group.empty()
                bg_img=pygame.image.load("./FINAL_IMG/BACKGROUND/GRAVEYARD.png")
                world = World(world_data_2)
                world.draw()

                level2_action=True
                pygame.display.update()
            elif level==2 and level2_action:
                world.draw()
                bat_group.update()

                for owl in owl_group:
                        owl.animate()
                broom_group.draw(screen)
                herb_group.draw(screen)
                crystal_group.draw(screen)
                bat_group.draw(screen)
                owl_group.draw(screen)

            elif level==3 and not level3_action:

                wand_group.add(wands)

                spider_group.empty() 
                potion_group.empty() 
                book_group.empty() 
                cat_group.empty()
                crystal_group.empty()
                herb_group.empty()
                bg_img=pygame.image.load("./FINAL_IMG/BACKGROUND/ROOFTOP.png")
                world = World(world_data_3)
                world.draw()

                level3_action=True
            elif level==3 and level3_action:
                world.draw()
                spider_group.update()
                bat_group.update()
                vampire_group.update()
                final_bat_group.update()
                final_spider_group.update()

                spider_group.draw(screen)
                bat_group.draw(screen)
                owl_group.draw(screen)
                vampire_group.draw(screen)
                final_bat_group.draw(screen)
                wand_group.draw(screen)
                final_spider_group.draw(screen)

            if level==3 and lives ==2 and not lost_life:
                wand_group.add(wands)
                lost_life=True

            if level==3 and lives ==1 and not lost_life1:
                wand_group.add(wands)
                lost_life1=True

            draw_text("LEVEL " + str(level), font3, white, tile_size + 400, 10)
            draw_text("LIVES " + str(lives), font3, white, tile_size + 700, 10)



            if game_over ==0:
                #update score
                #check if potion collected, True will mean potions disappear once collected
                if pygame.sprite.spritecollide(player, potion_group, True):
                        potions_fx.play()
                        potions += 1

                screen.blit(potion_score, (10,3))
                draw_text(" " + str(potions), font3, white, 50, 10)

                #check if book collected, 
                if pygame.sprite.spritecollide(player, book_group, True):
                        potions_fx.play()
                        books += 1
                screen.blit(book_score, (80,3))
                draw_text(" " + str(books), font3, white, 120, 10)

                if pygame.sprite.spritecollide(player, herb_group, True):
                        potions_fx.play()
                        herbs += 1
                screen.blit(herb_score, (150,3))
                draw_text(" " + str(herbs), font3, white, 190, 10)


                if pygame.sprite.spritecollide(player, crystal_group, True):
                        potions_fx.play()
                        crystals += 1
                screen.blit(crystal_score, (220,3))
                draw_text(" " + str(crystals), font3, white, 260, 10)

            flying = player.update(flying, game_over)
            wand = player.wand(wand)
            lives=player.lost_life(lives)

            if lives==0:
                game_over = -1

            if wand ==1:
                screen.blit(wandinst_img, (100,40))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        spell_fx.play(loops=0)
                        if player.direction==1:

                            spells.append(Spell(player.rect.centerx, player.rect.centery, 10, -8))

                        elif player.direction==-1:
                            spells.append(Spell(player.rect.centerx, player.rect.centery, -10, -8))

                for proj in spells:
                    proj.update()
                    pygame.gfxdraw.aacircle(screen, proj.x, proj.y, 10, (0, 255, 255, 200))

                    collided_bats = pygame.sprite.spritecollide(proj, final_bat_group, True)
                    for sprite in collided_bats:
                        sprite.visible=False
                    collided_spider = pygame.sprite.spritecollide(proj, spider_group, True)
                    for sprite in collided_spider:
                        sprite.visible=False

                    collided_final_spider = pygame.sprite.spritecollide(proj, final_spider_group, True)
                    for sprite in collided_final_spider:
                        sprite.visible=False

                    collided_vamp=pygame.sprite.spritecollide(proj, vampire_group, False)
                    for sprite in collided_vamp:
                        vamp_lives +=1

            if vamp_lives >500:
                win=1
                screen.blit(defeat_img, (0,0))
                vampire_group.empty()
                player.reset(25, screen_height - 25)
                spider_group.empty()
                spells_group.empty()
                bat_group.empty()
                final_bat_group.empty()
                final_spider_group.empty()
 
                pygame.display.update()

            if win==1 and not win_action:
                    defeat_count.play(loops=0)
                    win_action = True

            if game_over == -1:
                    player.reset(25, screen_height - 25)
                    spider_group.empty() 
                    bat_group.empty()
                    owl_group.empty()
                    final_bat_group.empty()
                    final_spider_group.empty()
                    vampire_group.empty()
                    spells_group.empty()
 
                    screen.blit(game_over_img, (250,200))
                    if restart_button.draw():
                        main_menu = True
                        level1_action = False
                        level2_action = False
                        level3_action = False
                        win_action = False
                        bg_img=pygame.image.load("./FINAL_IMG/BACKGROUND/ROOM.png")
                        world = World(world_data)
                        pygame.display.update()
                        broom_group.add(broom1, broom2)
                        world.draw()
                        spider_group.update()
                        bat_group.update()
                        vampire_group.update()
                        final_bat_group.update()
                        final_spider_group.update()
                        for cat in cat_group:
                                cat.animate()
                        for owl in owl_group:
                                owl.animate()
                        spider_group.draw(screen)
                        potion_group.draw(screen)
                        broom_group.draw(screen)
                        book_group.draw(screen)
                        cat_group.draw(screen)
                        herb_group.draw(screen)
                        crystal_group.draw(screen)
                        bat_group.draw(screen)
                        owl_group.draw(screen)
                        vampire_group.draw(screen)
                        final_bat_group.draw(screen)
                        wand_group.draw(screen)
                        final_spider_group.draw(screen)

                        player.reset(100, screen_height - 100)
                        level1_action = False
                        level2_action = False
                        level3_action = False
                        win_action = False
                        #this will help with the wand appearing
                        lost_life= False
                        lost_life1=False
                        wand=0
                        level=1
                        game_over=0
                        potions=0
                        crystals=0
                        books=0
                        herbs=0
                        lives=3
                        flying=0
                        score =0
                        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False

        pygame.display.update()

pygame.quit()
