
from pygame import *
from random import randint
from time import time as timer
font.init()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
background=transform.scale(image.load("galaxy.jpg"),(700,500))
window = display.set_mode((700, 500))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x = self.rect.x + self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15,20, -15)
        Bullets.add(bullet)

Bullets = sprite.Group()
class Anemi(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.x = randint( 50, 650)
            self.rect.y = 0
            lost = lost +1
ship = Player("rocket.png", 5, 420, 80, 100, 10)
Monsters = sprite.Group()
Asteroids = sprite.Group()
for i in range(1,5):
    monster = Anemi("ufo.png",randint(50,650), -40, 80, 50, randint(1,4))
    Monsters.add(monster)
for i in range(1,2):
    asteroid = Anemi("asteroid.png", randint(50,650), -40, 80, 50, randint(1,2))
    Asteroids.add(asteroid)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
font.init()
font1 = font.SysFont("Arial",80)
font2 = font.SysFont("Arial", 40)
win = font1.render("You win", True, (0,255,255))
lose = font1.render("Game Over", True, (255,255,0))

score = 0
goal = 10
lost = 0 
max_lost = 10
life = 3 



run = True
clock = time.Clock()
FPS = 60
finish  = False
rel_time = False
num_fire = 0


while run:
 
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()

    if not finish:
        window.blit(background,(0,0))
        ship.reset()
        ship.update()
        Monsters.update()
        Monsters.draw(window)
        Bullets.update()
        Bullets.draw(window)
        Asteroids.update()
        Asteroids.draw(window)
        
        if rel_time == True:
            now_time = timer()
            if  now_time - last_time < 3:
                reload = font2.render("Wait.....you don`t have ammont",1,(250,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(Monsters,Bullets,True,True)
        for c in collides:
            score = score + 1
            monster = Anemi("ufo.png",randint(50,650), -40, 80, 50, randint(1,3))
            Monsters.add(monster)

        if sprite.spritecollide(ship, Monsters, False) or sprite.spritecollide(ship, Asteroids,False):
            sprite.spritecollide(ship,Monsters, True)
            sprite.spritecollide(ship,Asteroids,True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            window.blit(win,(200,200))

      
        if life == 3:
            clife = (255,0,255)
        if life == 2:
            clife = (255,0,127)
        if life == 1:
            clife = (127,0,255)
        text_life = font2.render(str(life), True,clife)
        window.blit(text_life,(650,10))
        text_lost = font2.render(str(lost), True,(255,255,255))
        window.blit(text_lost,(50,10))
        score_text = font2.render(str(score), True,(150,105,50))
        window.blit(score_text,(650,40))
    
    
    
    else:
        finish = False
        score = 0 
        lost = 0
        num_fire = 0
        life = 3
        for monster in Monsters:
            monster.kill()
        for asteroid in Asteroids:
            asteroid.kill()
        time.delay(500)
        for i in range(1,5):
            monster = Anemi("ufo.png",randint(50,650), -40, 80, 50, randint(1,4))
            Monsters.add(monster)
        for i in range(1,2):
            asteroid = Anemi("asteroid.png", randint(50,650), -40, 80, 50, randint(1,2))
            Asteroids.add(asteroid)
    
    display.update()
    clock.tick(FPS)
    
