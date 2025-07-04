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
scale_list = []

bignose = False
bigeye = False
bigear = False

npc.print_info()
npc.randomize()

game = pg.Game(600, 600, "Walter's Bar",60,(100,100,100))


k_body = pg.AnimatedSprite('NPC/body.png',(38,65),(300,300))
k_clothing = pg.AnimatedSprite('NPC/clothing/'+npc.gclothing+'/'+npc.clothing+'.png',(38,65),(k_body.x,k_body.y))
k_ear = pg.AnimatedSprite('NPC/ears/standart/'+npc.race+'.png',(38,65),(k_body.x,k_body.y))
k_eye = pg.AnimatedSprite('NPC/eyes/human.png',(38,65),(k_body.x,k_body.y))
k_nose = pg.AnimatedSprite('NPC/noses/standart/'+npc.race+'.png',(38,65),(k_body.x,k_body.y))
if not "pig" in debuff_list and not "ram" in debuff_list and not "cock" in debuff_list:
    k_hair = pg.AnimatedSprite('NPC/hair/'+npc.gender+'/'+npc.hair+'.png',(38,65),(k_body.x,k_body.y))
k_head = pg.AnimatedSprite('NPC/heads/'+npc.skin+'/'+npc.race+'.png',(38,65),(k_body.x,k_body.y))

 
scale_factor = 3.0  # Масштаб (1.0 - оригинальный размер)
for sprite in [k_body, k_clothing,k_hair,k_head]:
    set_scale(sprite, scale_factor)
if bignose == True:
    set_scale(k_nose,3.5)
else:
    set_scale(k_nose,3.0)
if bigear == True:
    set_scale(k_ear,3.5)
else:
    set_scale(k_ear,3.0)
if bigeye == True:
    set_scale(k_eye,3.5)
else:
    set_scale(k_eye,3.0)


def change():
    global k_body,k_clothing,k_ear,k_eye,k_nose,k_hair,k_head,bigeye,bigear,bignose

    if "pig" in debuff_list:
        npc.race = "pig"
        npc.head = True
    elif "ram" in debuff_list:
        npc.race = "ram" 
        npc.head = True
    elif "cock" in debuff_list:
        npc.race = "cock"   
        npc.head = True

    if "red" in debuff_list:
        npc.skin = "red"
        npc.head = True
    elif "green" in debuff_list:
        npc.skin = "green"
        npc.head = True
    elif "blue" in debuff_list:
        npc.skin = "blue"
        npc.head = True
    elif "black" in debuff_list:
        npc.skin = "black"
        npc.head = True
    elif "goblin" in debuff_list:
        npc.skin = "green"
        npc.head = True

    if "bignose" in debuff_list:
        bignose = True
    else:
        bignose = False
    if "bigeye" in debuff_list:
        bigeye = True
    else:
        bigeye = False
    if "bigear" in debuff_list:
        bigear = True
    else:
        bignose = False


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
    global k_body,k_clothing,k_ear,k_eye,k_nose,k_hair,k_head

    k_body = pg.AnimatedSprite('NPC/body.png',(38,65),(300,300))
    k_clothing = pg.AnimatedSprite('NPC/clothing/'+npc.gclothing+'/'+npc.clothing+'.png',(38,65),(k_body.x,k_body.y))
    if not "cock" in debuff_list and not "ram" in debuff_list:
        k_ear = pg.AnimatedSprite('NPC/ears/'+npc.skin+'/'+npc.race+'.png',(38,65),(k_body.x,k_body.y))
    elif "ram" in debuff_list:
        k_ear = pg.AnimatedSprite('NPC/ears/standart/'+npc.race+'.png',(38,65),(k_body.x,k_body.y))
    if "cock" in debuff_list:
        k_eye = pg.AnimatedSprite('NPC/eyes/'+npc.race+'.png',(38,65),(k_body.x,k_body.y))
    else:
        k_eye = pg.AnimatedSprite('NPC/eyes/human.png',(38,65),(k_body.x,k_body.y))
    if not "goblin" in debuff_list:
        k_nose = pg.AnimatedSprite('NPC/noses/'+npc.skin+'/'+npc.race+'.png',(38,65),(k_body.x,k_body.y))
    else:
        k_nose = pg.AnimatedSprite('NPC/noses/special/goblin.png',(38,65),(k_body.x,k_body.y))
    if not "pig" in debuff_list and not "ram" in debuff_list and not "cock" in debuff_list:
        k_hair = pg.AnimatedSprite('NPC/hair/'+npc.gender+'/'+npc.hair+'.png',(38,65),(k_body.x,k_body.y))
    k_head = pg.AnimatedSprite('NPC/heads/'+npc.skin+'/'+npc.race+'.png',(38,65),(k_body.x,k_body.y))

    scale_factor = 3.0  # Масштаб (1.0 - оригинальный размер)
    for sprite in [k_body, k_clothing,k_hair,k_head]:
        set_scale(sprite, scale_factor)

    
    if bignose == True:
        set_scale(k_nose,3.5)
    else:
        set_scale(k_nose,3.0)
    if bigear == True:
        set_scale(k_ear,3.5)
    else:
        set_scale(k_ear,3.0)
    if bigeye == True:
        set_scale(k_eye,3.5)
    else:
        set_scale(k_eye,3.0)




    if pg.key_just_pressed(pygame.K_z): 

        debuff_list.clear()

        npc.randomize()


        k_body = pg.AnimatedSprite('NPC/body.png',(38,65),(300,300))
        k_clothing = pg.AnimatedSprite('NPC/clothing/'+npc.gender+'/'+npc.clothing+'.png',(38,65),(k_body.x,k_body.y))
        k_ear = pg.AnimatedSprite('NPC/ears/standart/human.png',(38,65),(k_body.x,k_body.y))
        k_eye = pg.AnimatedSprite('NPC/eyes/human.png',(38,65),(k_body.x,k_body.y))
        k_nose = pg.AnimatedSprite('NPC/noses/standart/human.png',(38,65),(k_body.x,k_body.y))
        k_hair = pg.AnimatedSprite('NPC/hair/'+npc.gender+'/'+npc.hair+'.png',(38,65),(k_body.x,k_body.y))

      
        for sprite in [k_body, k_clothing, k_ear, k_eye, k_nose, k_hair]:
            set_scale(sprite, scale_factor)
 
    print(debuff_list)

    if pg.key_just_pressed(pygame.K_q):
        if not "cock" in debuff_list and not "ram" in debuff_list and not "pig" in debuff_list and not "goblin" in debuff_list:
            debuff_list.append('pig')
    elif pg.key_just_pressed(pygame.K_w):
        if not "cock" in debuff_list and not "ram" in debuff_list and not "pig" in debuff_list and not "goblin" in debuff_list:
            debuff_list.append('cock')
    elif pg.key_just_pressed(pygame.K_e):
        if not "cock" in debuff_list and not "ram" in debuff_list and not "pig" in debuff_list and not "goblin" in debuff_list:
            debuff_list.append('ram')
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


    game.screen.blit(k_head.image,k_head.rect)

    game.screen.blit(k_clothing.image,k_clothing.rect)

    if npc.race != "cock":
        game.screen.blit(k_ear.image,k_ear.rect)

    game.screen.blit(k_eye.image,k_eye.rect)
    game.screen.blit(k_nose.image,k_nose.rect)
    if npc.race != "cock" and npc.race != "pig" and npc.race != "ram":
        game.screen.blit(k_hair.image,k_hair.rect)

    


game.run(update,draw)