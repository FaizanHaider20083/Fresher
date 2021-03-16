import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *

pygame.init() #begin pygame

#variables to be used through the program
vec = pygame.math.Vector2 #vector object
height = 350 #height of screen
width = 700 #width of screen
acc = 0.3 #acceleration
fric = -0.10 #friction  
fps = 60 #fps
fps_clock = pygame.time.Clock() #clock object to use wiith fps
count = 0
hit_cooldown = pygame.USEREVENT + 1
world = 0


displaysurface = pygame.display.set_mode((width,height)) #creates window
pygame.display.set_caption("Fresher") #caption

health_ani = [pygame.image.load("heart0.png"),
        pygame.image.load("heart.png"),
        pygame.image.load("heart2.png"),
        pygame.image.load("heart3.png"),
        pygame.image.load("heart4.png"),
        pygame.image.load("heart5.png"),]

class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("castle.png")

    def update(self):
        if self.hide == False:
            displaysurface.blit(self.image,(400,80))


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("Background.png")
        self.bgY = 0
        self.bgX = 0
    def render(self):
        displaysurface.blit(self.bgimage,(self.bgX,self.bgY)) #bgx and bgy are x and y coordinates respectively

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.rect  = self.image.get_rect(center = (350,350) )
    def render (self):
        displaysurface.blit(self.image,(self.rect.x,self.rect.y))




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()
        self.health = 5

        #Position and direction
        self.vx = 0
        self.pos = vec((340,240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "Right"
        self.jumping = False
        self.running = False
        self.move_frame = 0
        self.attacking = False
        self.cooldown = 0
        self.attack_frame = 0
        

    def move(self):
        # keeps a constant gravity of 0.5
        self.acc = vec(0,0.5) 
        #sets running to false if speed is too low
        if abs(self.vel.x)>0.3:
            self.running = True
        else :
            self.running = False
        #returns key pressed 
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -acc
        if pressed_keys[K_RIGHT]:
            self.acc.x = acc
        #formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * fric
        self. vel += self.acc
        self.pos += self.vel + 0.5*self.acc #updates position for new values

        #warping the character 
        if self.pos.x > width :
            self.pos.x = 0
        if self.pos.x<0 :
            self.pos.x = width 
        
        self.rect.midbottom = self.pos #updated rect with new postion
    
    def update(self):
        #Run animation for right 
        run_ani_R = [pygame.image.load("Player_Sprite_R.png"),
        pygame.image.load("Player_Sprite2_R.png"),
        pygame.image.load("Player_Sprite3_R.png"),
        pygame.image.load("Player_Sprite4_R.png"),
        pygame.image.load("Player_Sprite5_R.png"),
        pygame.image.load("Player_Sprite6_R.png"),
        pygame.image.load("Player_Sprite_R.png")
        

        ]

        run_ani_L =[pygame.image.load("Player_Sprite_L.png"),
        pygame.image.load("Player_Sprite2_L.png"),
        pygame.image.load("Player_Sprite3_L.png"),
        pygame.image.load("Player_Sprite4_L.png"),
        pygame.image.load("Player_Sprite5_L.png"),
        pygame.image.load("Player_Sprite6_L.png"),
        pygame.image.load("Player_Sprite_L.png"),]

        
        #Return to base frame if at end of movement sequence:
        if self.move_frame > 6 :
            self.move_frame = 0
            return
        #Move the character to the next frame if conditions are met
        if self.jumping == False and self.running == True :
            if self.vel.x>0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "Right"
            elif self.vel.x <0:
                self.image = run_ani_L[self.move_frame]
                self.direction = "Left"
            self.move_frame += 1

        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "Right":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "Left":
                self.image = run_ani_L[self.move_frame]


    def attack(self):
        attack_ani_R = [pygame.image.load("Player_Sprite_R.png"),
        pygame.image.load("Player_Attack_R.png"),
        pygame.image.load("Player_Attack2_R.png"),
        pygame.image.load("Player_Attack2_R.png"),
        pygame.image.load("Player_Attack3_R.png"),
        pygame.image.load("Player_Attack3_R.png"),
        pygame.image.load("Player_Attack4_R.png"),
        pygame.image.load("Player_Attack4_R.png"),
        pygame.image.load("Player_Attack5_R.png"),
        pygame.image.load("Player_Attack5_R.png"),
        pygame.image.load("Player_Sprite_R.png")
        ]

        attack_ani_L = [pygame.image.load("Player_Sprite_L.png"),
        pygame.image.load("Player_Attack_L.png"),
        pygame.image.load("Player_Attack2_L.png"),
        pygame.image.load("Player_Attack2_L.png"),
        pygame.image.load("Player_Attack3_L.png"),
        pygame.image.load("Player_Attack3_L.png"),
        pygame.image.load("Player_Attack4_L.png"),
        pygame.image.load("Player_Attack4_L.png"),
        pygame.image.load("Player_Attack5_L.png"),
        pygame.image.load("Player_Attack5_L.png"),
        pygame.image.load("Player_Sprite_L.png"),]

        #If attack frame has reached end of sequence,return to base frame
        if self.attack_frame > 10 :
            self.attack_frame = 0
            self.attacking = False
        # Check direction of attack
        if self.direction == "Right" :
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "Left":
            self.correction()
            self.image = attack_ani_L[self.attack_frame]
        
        self.attack_frame += 1



    def jump(self):
        self.rect.x += 1

        #check to see if player is in contact with the ground 
        hits = pygame.sprite.spritecollide(self,ground_group,False)
        self.rect.x -= 1
        #If touching the ground, and not currently jumping -> jump
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12

    def gravity_check(self):
        hits  = pygame.sprite.spritecollide(player,ground_group,False)
        if self.vel.y > 0 :
            if hits :
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom :
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    #lines to incorporate platformer genre
    
    def correction(self):
        # Function used to correct an error
        if self.attack_frame == 1:
            self.pos.x -= 20
        if self.attack_frame == 10:
            self.pos.x += 20
    
    def player_hit(self):
        if self.cooldown == False:
            self.cooldown = True 
            pygame.time.set_timer(hit_cooldown,1000)

            self.health -= 1
            health.image = health_ani[self.health]

            if self.health <= 0:
                self.kill()
                pygame.display.update()

        




class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        print ("Enemy created")
        self.image =  pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.direction = random.randint(0,1)#0for right,1 for left
        self.vel.x = random.randint(2,6) #random velocity for the gen enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 235
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 235
    def move(self):
        if self.pos.x >= (width-20) :
            self.direction =1 
        elif self.pos.x <= 0:
            self.direction = 0
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x
        
        self.rect.topleft = self.pos

    def render(self):
            #display the enemy 
            displaysurface.blit(self.image,(self.pos.x,self.pos.y))
            


    
    def update(self):
        #checks for collision with the player
        hits = pygame.sprite.spritecollide(self,Playergroup,False)
        #collision with fireballs
        f_hits = pygame.sprite.spritecollide(self, Fireballs, False)

        #Activates upon either of the two expression 
        if hits and player.attacking == True or f_hits :
            self.kill()
            

            print("Enemy killed")

        #if player not attacking
        elif hits and player.attacking == False :
            player.player_hit()

    

class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.stage = 1
        self.battle = False
        self.enemy_generation =  pygame.USEREVENT + 1
        self.stage_enemies = []
        for x in range(1,21):
            self.stage_enemies.append(int(x**2/2 )+1)

    def stage_handler(self):
        #Code for the stage selector
        background.bgimage = pygame.image.load("background2.jpg")
        world = 1
        pygame.time.set_timer(self.enemy_generation,2000)
        castle.hide = True
        self.battle = True
         

   
        #Custom backgrounds, unique enemies, spawn rates, ground visuals are just a few of many things you can tweak.
    def next_stage(self):
        self.stage += 1
        self.enemy_count = 0
        print("Stage: " + str(self.stage))
        pygame.time.set_timer(self.enemy_generation,1500 - (50*self.stage))

        
class Healthbar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("heart5.png")
    def render(self):
        displaysurface.blit(self.image,(10,10))

class fireball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = player.direction
        if self.direction == "Right" :
            self.image = pygame.image.load("fireball1_R.png")
        else :
            self.image = pygame.image.load("fireball1_L.png")
        self.rect = self.image.get_rect(center = player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40

    def fire(self):
        if -10<self.rect.x<710:
            if self.direction == "Right":
                self.image = pygame.image.load("fireball1_R.png")
                displaysurface.blit(self.image,self.rect)
            else :
                self.image = pygame.image.load("fireball1_L.png")
                displaysurface.blit(self.image,self.rect)
            
            if self.direction == "Right":
                self.rect.move_ip(12,0)
            else:
                self.rect.move_ip(-12,0)
        else:
            self.kill()
            player.attacking = False

    def update(self):
        f_hits = pygame.sprite.spritecollide(self, Enemies, False)

        if f_hits:
            self.kill()








background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)
health = Healthbar()
castle = Castle()
handler = EventHandler()
Enemies = pygame.sprite.Group()

Fireballs = pygame.sprite.Group()


#creating the game and event loop()

while True:
    player.gravity_check()
    background.render()
    castle.update()
    ground.render()
    player.update()
    if player.attacking == True:
        player.attack()
    player.move()
    if player.health > 0 :
        displaysurface.blit(player.image,player.rect)
    health.render()
    

    
    
    

    
    for event in pygame.event.get():
        #will execute when the close window is pressed
        if event.type == QUIT :
            pygame.quit()
            sys.exit()

        #for events that occur upon clicking the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        #Event handling for a range of different key presses 
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_n:
                if handler.battle == True and len(Enemies) == 0:
                    handler.next_stage()
            if event.key == pygame.K_e and 450 < player.rect.x<550 :
                handler.stage_handler()
            if event.key == pygame.K_SPACE :
                player.jump()
            if event.key == pygame.K_RETURN:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True
            if event.key == pygame.K_m:
                player.attacking = True
                Fireball = fireball()
                Fireballs.add(Fireball)

        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown,0)

        if event.type == handler.enemy_generation:
            
            while handler.enemy_count < handler.stage_enemies[handler.stage -1]:
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1
    
        
    for entity in Enemies:
                
        entity.render()
        entity.update()
        entity.move()
    for ball in Fireballs:
        ball.fire()
        
                
    pygame.display.update()
    fps_clock.tick(fps)
    




        







