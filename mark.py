import pygame

import pygine as pg 
size_klient = (width,height)
pouse_klient = (x, y)
game = pg.Game(1280,720,'ХимЛаба',60,(100,100,100))

bottle_pig = pg.Button(0,0,100,50,"pig",pig_callback)
bottle_rooster = pg.Button(0,0,100,50,"rooster",rooster_callback)
bottle_ram = pg.Button(0,0,100,50,"ram",ram_callback)

bottle_nouse = pg.Button(0,0,100,50,"nouse",nouse_callback)
bottle_eye = pg.Button(0,0,100,50,"eye",eye_callback)
bottle_ears = pg.Button(0,0,100,50,"ears",ears_callback)

bottle_green = pg.Button(0,0,100,50,"green",green_callback)
bottle_red = pg.Button(0,0,100,50,"red",red_callback)
bottle_blue = pg.Button(0,0,100,50,"blue",blue_callback)

bottle_goblin = pg.Button(0,0,100,50,"goblin",goblin_callback)
bottle_vampire = pg.Button(0,0,100,50,"vampire",vampire_callback)
bottle_werewolf = pg.Button(0,0,100,50,"werewolf",werewolf_callback)

bottle_coconut_milk = pg.Button(0,0,100,50,"coconut milk",coconut_milk_callback)
bottle_laxative = pg.Button(0,0,100,50,"laxative",laxative_callback)
bottle_negr = pg.Button(0,0,100,50,"negr",negr_callback)

pig = False
rooster = False
ram = False

nouse = False
eye = False
ears = False

green = False
red = False
blue = False

goblin = False
vampire = False
werewolf = False

coconut_milk = False
Laxative = False
negr = False

def pig_callback():
    pig = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)

def rooster_callback():
    rooster = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    
def ram_callback():
    ram = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    
def nouse_callback():
    nouse = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)

def eye_callback():
    eye = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    
def ears_callback():
    ears = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    
def green_callback():
    green = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    
def red_callback():
    red = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    
def blue_callback():
    blue = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    
def goblin_callback():
    goblin = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    
def vampire_callback():
    vampire = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)

def werewolf_callback():
    werewolf = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)

def coconut_milk_callback():
    coconut_milk = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)

def laxative_callback():
    Laxative = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)

def negr_callback():
    negr = True
    animation_filling = pg.AnimatedSprite("",Wolter_size, Wolter_)
    animation_filling.add_animation("probirka",[1,2,3,4,5,6],fps = 60,loop = False)
    

def change_human():
    ifects = pg.AnimatedSprite("",size_klient,pouse_klient)
    if pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif _callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
    elif pig_callback == True:
        pig_face = pg.AnimatedSprite("",size_klient,pouse_klient)
        
    

def update():
    pass

def draw():
    bottle_pig.draw()

game.run(update,draw)
