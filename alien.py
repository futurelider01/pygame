import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.setting=ai_game.setting
        self.img=pygame.image.load('images/alien.png')
        self.image=pygame.transform.scale(self.img,(50,50))
        self.rect=self.image.get_rect()
    
        self.x=self.rect.width
        self.y=self.rect.height   
    def update(self):
        self.x+=self.setting.alien_speed*self.setting.fleet_direction
        self.rect.x=self.x
    def check_edge(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True