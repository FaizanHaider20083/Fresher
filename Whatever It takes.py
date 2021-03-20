import pygame


import sys
import time
from pygame.locals import *
import random

multiple_enemies = 1
crossed_enemies = 0
enemies_killed = 0
height = 340
width = 680

fric = -0.1

acc = 0.3

pygame.init()

alive = 1
hit_cooldown = pygame.USEREVENT + 1



fps = 30
fps_clock = pygame.time.Clock()

displaysurface = pygame.display.set_mode((width,height))
pygame.display.set_caption("Whatever it takes")

vec = pygame.math.Vector2


red = (255,0,0)
black = (0,0,0)
pink =(255,192,203)


master_control = 1

health_ani = [pygame.image.load("heart0.png"),
        pygame.image.load("heart.png"),
        pygame.image.load("heart2.png"),
        pygame.image.load("heart3.png"),
        pygame.image.load("heart4.png"),
        pygame.image.load("heart5.png"),]




def countdown():
    start_time = time.time()
    

    
    if (time.time() - start_time) >10:
        time_count+=1
        return  1

   





class player(object):
    run_ani_R = [pygame.image.load("Player_Sprite_R.png"),
        pygame.image.load("Player_Sprite2_R.png"),
        pygame.image.load("Player_Sprite3_R.png"),
        pygame.image.load("Player_Sprite4_R.png"),
        pygame.image.load("Player_Sprite5_R.png"),
        pygame.image.load("Player_Sprite6_R.png"),
        pygame.image.load("Player_Sprite_R.png")
        

        ]

    
    
    jumpList = [10,6,6,9,3,4,4,4,4,4,4,0,-4,-2,-10,-2,-2,-2,-3,-3,-9,-11,-10]

    def __init__(self, x, y, width, height):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.run_frame = 0
        self.pos = vec(x,y)
        self.health = 2
        
        self.locus = 240
       


    def draw(self, win):

        
        self.locus += 4
    

        

        

        if self.run_frame <= 6:

            displaysurface.blit(self.run_ani_R[self.run_frame],(self.x,self.y))
        if self.run_frame >6 :
            self.run_frame = 0
        
        self.run_frame += 1



        
        if self.jumping == True:
            
            self.y -= self.jumpList[self.jumpCount] * 1.3
            if self.run_frame <= 6:
                displaysurface.blit(self.run_ani_R[self.run_frame], (self.x, self.y))
                self.run_frame += 1
            else :
                self.run_frame = 0
            self.jumpCount += 1
            if self.jumpCount >= len(self.jumpList):
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)
        


    

        
       
        

    

    


class player_level2(pygame.sprite.Sprite):
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
        # keeps a constant gravity of 1
        self.acc = vec(0,1) 
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
        #stop animation if speed decreases
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
            self.vel.y = -15

    def gravity_check(self):
        hits  = pygame.sprite.spritecollide(Player_Pro,ground_group,False)
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
                displaysurface.fill(red)
                pygame.time.delay(2000)
                sys.exit()
                pygame.display.update()

class Healthbar(pygame.sprite.Sprite):
    def __init__(self,i):
        super().__init__()
        if i == 5:
            self.image = pygame.image.load("heart5.png")
        if i == 2:
            self.image = pygame.image.load("heart2.png")
    def render(self):
        displaysurface.blit(self.image,(10,10))       



    


class melee_enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
         
        self.image =  pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.direction = random.randint(0,1)#0for right,1 for left
        self.vel.x = random.randint(1,5) #random velocity for the gen enemy
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
        global enemies_killed
        #checks for collision with the player
        hits = pygame.sprite.spritecollide(self,Player_Pro_group,False)
        #collision with fireballs
        f_hits = pygame.sprite.spritecollide(self, Fireballs, False)

        #Activates upon either of the two expression 
        if hits and Player_Pro.attacking == True or f_hits :
            self.kill()
            enemies_killed +=1
            

           

        #if player not attacking
        elif hits and Player_Pro.attacking == False :
            Player_Pro.player_hit()




class level1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("level1.jpeg")
        self.bgX1 = 0
        self.bgX2 = width
        self.speed = 4


    def update(self):
        self.bgX1 -= self.speed
        self.bgX2 -= self.speed

        if self.bgX1 == -width:
            self.bgX1 = width

        if self.bgX2 == -width:
            self.bgX2 = width

        

    def render(self):
        displaysurface.blit(self.image,(self.bgX1,0))
        displaysurface.blit(self.image,(self.bgX2,0))


class level2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("level2.jpeg")

    def render(self):
        displaysurface.blit(self.image,(0,0))



class Index():
    def __init__(self):
        self.poster_call = 1
        pygame.mixer.Sound("avengers.mp3").play()
        
        self.climax_call = 0
        
        self.render_level_2 = 0

        self.prologue_frame = 0
        self.climax_frame = 0

        self.epilogue_frame = 0
        self.prologue_images = [pygame.image.load("prologue1.png"),
        pygame.image.load("prologue2.png"),
        pygame.image.load("prologue3.png"),
        pygame.image.load("prologue4.png"),
        pygame.image.load("prologue5.png")
        
        ]

        self.epilogue_images = [pygame.image.load("epilogue1.png"),
        pygame.image.load("epilogue2.png"),
        pygame.image.load("epilogue3.png"),
        pygame.image.load("epilogue4.png"),
        pygame.image.load("epilogue5.png"),
        pygame.image.load("epilogue5.png")
        ]

        self.climax_images = [pygame.image.load("climax1.png"),
        pygame.image.load("climax2.png"),
        pygame.image.load("climax3.png"),
        pygame.image.load("climax4.png"),
        pygame.image.load("climax5.png"),
        pygame.image.load("climax5.png")
        ]

        self.poster = pygame.image.load("poster.png")
        self.image = 0
        self.first_time = 0
        self.first_frame = 1
    def epilogue(self):



        self.image = self.epilogue_images[self.epilogue_frame]
        displaysurface.blit(self.image,(0,0))
        if self.first_time != 0:
            pygame.time.delay(3000)
        self.first_time += 1
        self.epilogue_frame += 1
        if self.epilogue_frame == 6:
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()
        
    def prologue(self):
        print(self.prologue_frame)
        if self.prologue_frame < 5:
            self.image = self.prologue_images[self.prologue_frame]
            displaysurface.blit(self.image,(0,0))
            pygame.time.delay(4000)

            self.prologue_frame += 1
        if self.prologue_frame == 5:
            displaysurface.blit(self.poster,(0,0))
            pressed_key = pygame.key.get_pressed()
            
            if pressed_key[K_1] or pressed_key[K_SPACE]:
                pygame.time.delay(1000)
                
                self.poster_call = 0

                
            elif pressed_key [K_2]:
                pygame.quit()
                sys.exit

 
        

    def climax(self):
        if self.climax_frame < 6:
            self.image = self.climax_images[self.climax_frame]
            displaysurface.blit(self.image,(0,0))
            if self.first_frame != 1:
                pygame.time.delay(4000)
            self.first_frame = 0
            self.climax_frame += 1
        if self.climax_frame == 6:
            master_control =2
            handler.level = 2
            






    




class level_handler():
    def __init__(self):
        self.level = 1
        self.enemy_generation = pygame.USEREVENT + 1
        self.level_1_obs = 10
        self.obs_created = 0
        self.level2_enemy_generation = pygame.USEREVENT + 1
        self.level2_total_enemies = 20
        self.level2_generated = 0
        
    def level_1_handler(self):
        pygame.time.set_timer(self.enemy_generation,1000)

    def level_2_handler(self):



        pygame.time.set_timer(self.level2_enemy_generation,10000)

    


        






class solid_ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,286,25000,height - 242)
        pygame.draw.rect(displaysurface,black,self.rect)

    

class visible_ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.bgX1 = 0
        self.bgX2 = width
        self.speed = 4

    def update(self):
        self.bgX1 -= self.speed
        self.bgX2 -= self.speed

        if self.bgX1 == -width:
            self.bgX1 = width

        if self.bgX2 == -width:
            self.bgX2 = width

        

    def render(self):
        displaysurface.blit(self.image,(self.bgX1,270))
        displaysurface.blit(self.image,(self.bgX2,270))



class obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("grave.png")
        self.a = random.randint(1,20)
        self.b = random.randint(1,5)

        
        self.pos = vec((self.a * width)/self.b,250)
        self.vel = vec(0,0)
        self.vel.x = random.randint(2,8)
        
        self.lat = (self.a * width)/self.b
        
        
    def render(self):
        displaysurface.blit(self.image,self.pos)

    def move(self):
        self.lat -= self.vel.x + 4
        self.pos.x -= abs(self.vel.x)
       
        

    def update(self):
        global crossed_enemies
        hits = 0
        if 238< int(self.pos.x) <242 and Player.jumping == False:
            crossed_enemies+= 1
            
            hits = 1

        if hits == 1:
             
            self.kill()
            print("Player killed")
            alive = 0
            displaysurface.fill(black)
            pygame.time.delay(300)
            Player.health -= 1
            health_level1.image = health_ani[Player.health]


        if self.pos.x < -100 :
            self.kill()
            crossed_enemies +=1
            print(crossed_enemies, 'crossed enemies')


Player_Pro = player_level2()

class fireball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = Player_Pro.direction
        if self.direction == "Right" :
            self.image = pygame.image.load("fireball1_R.png")
        else :
            self.image = pygame.image.load("fireball1_L.png")
        self.rect = self.image.get_rect(center = Player_Pro.pos)
        self.rect.x = Player_Pro.pos.x
        self.rect.y = Player_Pro.pos.y - 40

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
            print("Fireball should be killed")
            self.kill()
           
    
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.rect  = self.image.get_rect(center = (350,350) )
    def render (self):
        displaysurface.blit(self.image,(self.rect.x,self.rect.y))



Player_Pro_group = pygame.sprite.Group()
Player_Pro_group.add(Player_Pro)
finale = level2()

Fireball = fireball()

Fireballs = pygame.sprite.Group()



start = level1()
ground = visible_ground()



floor = solid_ground()

Obstacles = pygame.sprite.Group()
handler = level_handler()

Player = player(240,237,25,49)

zameen = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(zameen)

health = Healthbar(5)
health_level1 = Healthbar(2)
level2_invoker = 1



floor_group = pygame.sprite.Group()
floor_group.add(floor)

index = Index()

level2_enemies = pygame.sprite.Group()




handler.level_1_handler()
while True:

    if index.poster_call == 1:
        

        
        index.prologue()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        

    else :
        

        if index.render_level_2 == 1 or master_control == 2 :
            Player_Pro.gravity_check()
            handler.level = 2
            finale.render()
            
            Player_Pro.move()
            if Player_Pro.attacking == True :
                Player_Pro.attack()
            if Player_Pro.health > 0:
                displaysurface.blit(Player_Pro.image,Player_Pro.rect)
                Player_Pro.update()
            health.render()



        if handler.level == 1 and alive == 1:
            
            start.render()
            start.update()
            ground.render()
            ground.update()
            
            health_level1.render()
            if Player.health > 0:
                Player.draw(displaysurface)
            if Player.health == 0:
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

            
            
        



        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if handler.level ==1 :
                    

                        Player.jumping = True
                        Player.draw(displaysurface)
                    if handler.level == 2 or master_control == 2:
                        Player_Pro.jump()

                if event.key == pygame.K_m:
                    if handler.level == 2 or master_control == 2:
                        Player_Pro.attacking = True
                        Fireball = fireball()
                        Fireballs.add(Fireball)
                    

                if event.key == pygame.K_RETURN:
                    if handler.level == 2 or master_control == 2:
                        if Player_Pro.attacking == False:
                            Player_Pro.attack()
                            Player_Pro.attacking = True


            if event.type == handler.enemy_generation:
                if multiple_enemies == 1:
                    while handler.level_1_obs > handler.obs_created:
                        
                        obs = obstacle()
                        Obstacles.add(obs)
                        handler.obs_created += 1

            if event.type == hit_cooldown:
                Player_Pro.cooldown = False
                pygame.time.set_timer(hit_cooldown,0)

            
            if event.type == handler.level2_enemy_generation:
                while handler.level2_generated < handler.level2_total_enemies:
                    enemy = melee_enemy()
                    level2_enemies.add(enemy)
                    handler.level2_generated += 1

        if handler.level == 2 or master_control == 2:
            for enemy in level2_enemies:
                enemy.render()
                enemy.move()
                enemy.update()




        if handler.level == 1:
            for entity in Obstacles:
                if alive == 1:
                    entity.render()
                    entity.move()
                    entity.update()
        if handler.level == 2 or master_control == 2:
            for ball in Fireballs:
                ball.fire()
        
        if handler.level == 2 or master_control == 2:
            if level2_invoker == 1:
                handler.level_2_handler()
                level2_invoker = 0


    

    if crossed_enemies >= 5:

        

        index.climax()
        master_control = 2

    if enemies_killed == 20:
        index.epilogue()

    pygame.display.update()
    fps_clock.tick(fps)



