import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.setting=ai_game.setting
        self.color=self.setting.bullet_color

        self.rect = pygame.Rect(0,0,self.setting.bullet_width,self.setting.bullet_height)
        self.rect.midbottom=ai_game.ship.rect.midtop
        
    def update(self):
        self.rect.y-=self.setting.bullet_speed
        # self.rect_bullet.y = self.rect_bullet.y
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)