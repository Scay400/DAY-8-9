import pygame
import random
import pygine as pg

class Klient():
    def __init__(self):
        self.gender = None
        self.body = None
        self.clothing = None
        self.hair = None
        self.gender = random.choice(["male","female"])    

        if self.gender == "male":
            self.body = "male"
            self.clothing = random.choice(["suit","sportwear","casual"])
            self.hair = random.choice(["hair1","hair2","hair3"])
        else:
            self.body = "female"
            self.clothing = random.choice(["dress","casual","casual2"])
            self.hair = random.choice(["hair1","hair2","hair3"])

        self.wish_text = None
    
    def randomize(self):
        self.gender = random.choice(["male","female"])    

        if self.gender == "male":
            self.body = "male"
            self.clothing = random.choice(["suit","sportswear","casual"])
            self.hair = random.choice(["hear1","hear2","hear3"])
        else:
            self.body = "female"
            self.clothing = random.choice(["dress","casual","casual2"])
            self.hair = random.choice(["hear1","hear2","hear3"])

        self.wish_text = None

    def print_info(self):
        print(self.gender,"\n",self.body,"\n",self.clothing,"\n",self.hair)

# Наша собственная функция масштабирования
def set_scale(sprite, scale):
    if not hasattr(sprite, 'original_image'):
        sprite.original_image = sprite.image
    
    original_rect = sprite.original_image.get_rect()
    new_width = int(original_rect.width * scale)
    new_height = int(original_rect.height * scale)
    
    scaled_image = pygame.transform.scale(sprite.original_image, (new_width, new_height))
    sprite.image = scaled_image
    sprite.rect = scaled_image.get_rect(center=sprite.rect.center)

npc = Klient()
npc.print_info()
npc.randomize()

game = pg.Game(600, 600, "Walter's Bar", 60, (0,0,0))

# Создаем спрайты
k_body = pg.AnimatedSprite('./NPC/body.png', (38,65), (300,300))
k_clothing = pg.AnimatedSprite('./NPC/clothing/'+npc.gender+'/'+npc.clothing+'.png', (38,65), (300,300))
k_ear = pg.AnimatedSprite('./NPC/ears/standart/human.png', (38,65), (300,300))
k_eye = pg.AnimatedSprite('./NPC/eyes/human.png', (38,65), (300,300))
k_nose = pg.AnimatedSprite('./NPC/noses/standart/human.png', (38,65), (300,300))
k_hair = pg.AnimatedSprite('./NPC/hair/'+npc.gender+'/'+npc.hair+'.png', (38,65), (300,300))

# Применяем масштабирование
scale_factor = 3.0  # Масштаб (1.0 - оригинальный размер)
for sprite in [k_body, k_clothing, k_ear, k_eye, k_nose, k_hair]:
    set_scale(sprite, scale_factor)

def update():
    global k_body, k_clothing, k_ear, k_eye, k_nose, k_hair, scale_factor
    
    if pg.key_just_pressed(pygame.K_r):  
        npc.randomize()
        
        # Пересоздаем спрайты
        k_body = pg.AnimatedSprite('./NPC/body.png', (38,65), (300,300))
        k_clothing = pg.AnimatedSprite('./NPC/clothing/'+npc.gender+'/'+npc.clothing+'.png', (38,65), (300,300))
        k_ear = pg.AnimatedSprite('./NPC/ears/standart/human.png', (38,65), (300,300))
        k_eye = pg.AnimatedSprite('./NPC/eyes/human.png', (38,65), (300,300))
        k_nose = pg.AnimatedSprite('./NPC/noses/standart/human.png', (38,65), (300,300))
        k_hair = pg.AnimatedSprite('./NPC/hair/'+npc.gender+'/'+npc.hair+'.png', (38,65), (300,300))
        
        # Снова применяем масштабирование
        for sprite in [k_body, k_clothing, k_ear, k_eye, k_nose, k_hair]:
            set_scale(sprite, scale_factor)
    

def draw():
    game.screen.blit(k_body.image, k_body.rect)
    game.screen.blit(k_clothing.image, k_clothing.rect)
    game.screen.blit(k_ear.image, k_ear.rect)
    game.screen.blit(k_eye.image, k_eye.rect)
    game.screen.blit(k_nose.image, k_nose.rect)
    game.screen.blit(k_hair.image, k_hair.rect)

game.run(update, draw)