import pygame

import pygine as pg 

game = pg.Game(1280,720,'ХимЛаба',60,(100,100,100))

sprite = pg.AnimatedSprite('assets/platformer_sprites.png',(64,64),(1000,350))
sprite.add_animation('idle',[0,1,2,3])
sprite.set_scale(10)

def update():

    sprite.play_animation("idle")
    sprite.update()
    sprite.mirror(True)

def draw():

    game.screen.blit(sprite.image,sprite.rect)

game.run(update,draw)