import pygame
import random
import pygine as pg

# wish_dict = {
#     "текст1":["большой нос","сигма уй"],
#     "текст2":["маленький нос","свинья"],
#     "текст3":["ez","niga"],
# }

# if "большой нос" in wish_dict[1]["текст который говорят"]:
#     print("ez")

def set_scale(sprite, scale):
    if not hasattr(sprite, 'original_image'):
        sprite.original_image = sprite.image
    
    original_rect = sprite.original_image.get_rect()
    new_width = int(original_rect.width * scale)
    new_height = int(original_rect.height * scale)
    
    scaled_image = pygame.transform.scale(sprite.original_image, (new_width, new_height))
    sprite.image = scaled_image
    sprite.rect = scaled_image.get_rect(center=sprite.rect.center)

class Klient():
    def __init__(self):

        self.gender = None
        self.gclothing = None
        self.clothing = None
        self.hair = None
        self.race = "human"
        self.skin = "standart"



        self.gender = random.choice(["male","female"])    

        if self.gender == "male":
            self.gclothing = "male"
            self.clothing = random.choice(["suit","sportwear","casual"])
            self.hair = random.choice(["hair1","hair2","hair3"])

        else:
            self.gclothing = "female"
            self.clothing = random.choice(["dress","casual","casual2"])
            self.hair = random.choice(["hair1","hair2","hair3"])

        self.wish_text = None
    
    def randomize(self):

        self.gender = None
        self.gclothing = None
        self.clothing = None
        self.hair = None
        self.race = "human"
        self.skin = "standart"

        self.gender = random.choice(["male","female"])    

        if self.gender == "male":
            self.gclothing = "male"
            self.clothing = random.choice(["suit","sportswear","casual"])
            self.hair = random.choice(["hear1","hear2","hear3"])

        else:
            self.gclothing = "female"
            self.clothing = random.choice(["dress","casual","casual2"])
            self.hair = random.choice(["hear1","hear2","hear3"])

        self.wish_text = None

        # self.wish_text = random.choice(list(wish_dict.keys()))
        # self.wish = wish_dict[self.wish_text]

    def print_info(self):
        print(self.gender,"\n",self.clothing,"\n",self.hair)

npc = Klient()

debuff_list = []

npc.print_info()
npc.randomize()

game = pg.Game(600, 600, "Walter's Bar",60,(100,100,100))


k_body = pg.AnimatedSprite('NPC/body.png',(38,65),(300,300))
k_clothing = pg.AnimatedSprite('NPC/clothing/'+npc.gclothing+'/'+npc.clothing+'.png',(38,65),(300,300))
k_ear = pg.AnimatedSprite('NPC/ears/standart/'+npc.race+'.png',(38,65),(300,300))
k_eye = pg.AnimatedSprite('NPC/eyes/human.png',(38,65),(300,300))
k_nose = pg.AnimatedSprite('NPC/noses/standart/'+npc.race+'.png',(38,65),(300,300))
if not "pig" in debuff_list and not "raw" in debuff_list and not "cock" in debuff_list:
    k_hair = pg.AnimatedSprite('NPC/hair/'+npc.gender+'/'+npc.hair+'.png',(38,65),(300,300))

scale_factor = 3.0  # Масштаб (1.0 - оригинальный размер)
for sprite in [k_body, k_clothing, k_ear, k_eye, k_nose, k_hair]:
    set_scale(sprite, scale_factor)



def change():
    global k_body,k_clothing,k_ear,k_eye,k_nose,k_hair

    if "pig" in debuff_list:
        npc.race = "pig"
    elif "raw" in debuff_list:
        npc.race = "raw" 
    elif "cock" in debuff_list:
        npc.race = "cock"   

    if "red" in debuff_list:
        npc.skin = "red"
    elif "green" in debuff_list:
        npc.skin = "green"
    elif "blue" in debuff_list:
        npc.skin = "blue"
    elif "black" in debuff_list:
        npc.skin = "black"

    if "bignose" in debuff_list:
        for sprite in [k_nose]:
            set_scale(sprite, scale_factor+1)
    if "bigeye" in debuff_list:
        for sprite in [k_eye]:
            set_scale(sprite, scale_factor+1)
    if "bigear" in debuff_list:
        for sprite in [k_ear]:
            set_scale(sprite, scale_factor+1)

    if "vampire" in debuff_list:
        npc.gclothing = "special"
        npc.clothing = "vampire"
    elif "werewolf" in debuff_list:
        npc.gclothing = "special"
        npc.clothing = "werewolf"
    if "coconut" in debuff_list:
        npc.gclothing = "special"
        npc.clothing = "coconut"
    

def update():
    global k_body,k_clothing,k_ear,k_eye,k_nose,k_hair

    k_body = pg.AnimatedSprite('NPC/body.png',(38,65),(300,300))
    k_clothing = pg.AnimatedSprite('NPC/clothing/'+npc.gclothing+'/'+npc.clothing+'.png',(38,65),(300,300))
    if not "cock" in debuff_list and not "raw" in debuff_list:
        k_ear = pg.AnimatedSprite('NPC/ears/'+npc.skin+'/'+npc.race+'.png',(38,65),(300,300))
    elif "raw" in debuff_list:
        k_ear = pg.AnimatedSprite('NPC/ears/standart/'+npc.race+'.png',(38,65),(300,300))
    k_eye = pg.AnimatedSprite('NPC/eyes/'+npc.race+'.png',(38,65),(300,300))
    if not "goblin" in debuff_list:
        k_nose = pg.AnimatedSprite('NPC/noses/'+npc.skin+'/'+npc.race+'.png',(38,65),(300,300))
    else:
        k_nose = pg.AnimatedSprite('NPC/noses/special/goblin.png',(38,65),(300,300))
    if not "pig" in debuff_list and not "raw" in debuff_list and not "cock" in debuff_list:
        k_hair = pg.AnimatedSprite('NPC/hair/'+npc.gender+'/'+npc.hair+'.png',(38,65),(300,300))

    scale_factor = 3.0  # Масштаб (1.0 - оригинальный размер)
    for sprite in [k_body, k_clothing, k_ear, k_eye, k_nose, k_hair]:
        set_scale(sprite, scale_factor)



    if pg.key_just_pressed(pygame.K_z):  

        debuff_list.clear()

        npc.randomize()

        k_body = pg.AnimatedSprite('NPC/body.png',(38,65),(300,300))
        k_clothing = pg.AnimatedSprite('NPC/clothing/'+npc.gender+'/'+npc.clothing+'.png',(38,65),(300,300))
        k_ear = pg.AnimatedSprite('NPC/ears/standart/human.png',(38,65),(300,300))
        k_eye = pg.AnimatedSprite('NPC/eyes/human.png',(38,65),(300,300))
        k_nose = pg.AnimatedSprite('NPC/noses/standart/human.png',(38,65),(300,300))
        k_hair = pg.AnimatedSprite('NPC/hair/'+npc.gender+'/'+npc.hair+'.png',(38,65),(300,300))

        for sprite in [k_body, k_clothing, k_ear, k_eye, k_nose, k_hair]:
            set_scale(sprite, scale_factor)
    
    print(debuff_list)

    if pg.key_just_pressed(pygame.K_q):
        if not "cock" in debuff_list and not "raw" in debuff_list and not "pig" in debuff_list and not "goblin" in debuff_list:
            debuff_list.append('pig')
    elif pg.key_just_pressed(pygame.K_w):
        if not "cock" in debuff_list and not "raw" in debuff_list and not "pig" in debuff_list and not "goblin" in debuff_list:
            debuff_list.append('cock')
    elif pg.key_just_pressed(pygame.K_e):
        if not "cock" in debuff_list and not "raw" in debuff_list and not "pig" in debuff_list and not "goblin" in debuff_list:
            debuff_list.append('raw')
    elif pg.key_just_pressed(pygame.K_r):
        if not "bignose" in debuff_list:
            debuff_list.append('bignose')
    elif pg.key_just_pressed(pygame.K_t):
        if not "bigeye" in debuff_list:
            debuff_list.append('bigeye')
    elif pg.key_just_pressed(pygame.K_y):
        if not "bigear" in debuff_list:
            debuff_list.append('bigear')
    elif pg.key_just_pressed(pygame.K_u):
        if not "red" in debuff_list and not "green" in debuff_list and not "blue" in debuff_list and not "goblin" in debuff_list and not "black" in debuff_list:
            debuff_list.append('red')
    elif pg.key_just_pressed(pygame.K_i):
        if not "red" in debuff_list and not "green" in debuff_list and not "blue" in debuff_list and not "goblin" in debuff_list and not "black" in debuff_list:
            debuff_list.append('green')
    elif pg.key_just_pressed(pygame.K_o):
        if not "red" in debuff_list and not "green" in debuff_list and not "blue" in debuff_list and not "goblin" in debuff_list and not "black" in debuff_list:
            debuff_list.append('blue')
    elif pg.key_just_pressed(pygame.K_p):
        if not "red" in debuff_list and not "blue" in debuff_list and not "goblin" in debuff_list and not "black" in debuff_list:
            debuff_list.append('goblin')
    elif pg.key_just_pressed(pygame.K_a):
        if not "coconut" in debuff_list and not "werewolf" in debuff_list and not "vampire" in debuff_list:
            debuff_list.append('vampire')
    elif pg.key_just_pressed(pygame.K_s):
        if not "coconut" in debuff_list and not "werewolf" in debuff_list and not "vampire" in debuff_list:
            debuff_list.append('werewolf')
    elif pg.key_just_pressed(pygame.K_d):
        if not "red" in debuff_list and not "green" in debuff_list and not "blue" in debuff_list and not "goblin" in debuff_list and not "black" in debuff_list:
            debuff_list.append('black')
    elif pg.key_just_pressed(pygame.K_f):
        if not "coconut" in debuff_list and not "werewolf" in debuff_list and not "vampire" in debuff_list:
            debuff_list.append('coconut')
    elif pg.key_just_pressed(pygame.K_g):
        if not "poop" in debuff_list:
            debuff_list.append('poop')
    elif pg.key_just_pressed(pygame.K_l): #сброс
        debuff_list.clear()
    elif pg.key_just_pressed(pygame.K_k):  #смена
        change()                 



def draw():

    game.screen.blit(k_body.image,k_body.rect)

    game.screen.blit(k_clothing.image,k_clothing.rect)
    if not "cock" in debuff_list:
        game.screen.blit(k_ear.image,k_ear.rect)

    game.screen.blit(k_eye.image,k_eye.rect)
    game.screen.blit(k_nose.image,k_nose.rect)

    game.screen.blit(k_hair.image,k_hair.rect)


game.run(update,draw)