import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    # managing with ship's setting
    def __init__(self,ai_game):
        super().__init__()
        # initialization of ship's display and
        # setting the initial position
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        # setting from alien
        self.setting=ai_game.setting
        
        # uploading image and setting a rectangular
        self.img=pygame.image.load('Images/Ship.bmp')
        self.image = pygame.transform.scale(self.img,(80,60))
        self.rect = self.image.get_rect()
        
        # self.x
        self.x=float(self.rect.x)
        
        # each new ship creates in bottom
        self.rect.midbottom = self.screen_rect.midbottom

        # flag moving
        self.moving_right=False
        self.moving_left=False
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x+=self.setting.ship_speed
        if  self.moving_left and self.rect.left > self.screen_rect.left: # self.screen_rect.lef=0
            self.rect.x-=self.setting.ship_speed
    
    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom

    def blit_me(self):
        # Bliting a ship in this position
                        # source    # position (x,y)
        self.screen.blit(self.image,self.rect) 