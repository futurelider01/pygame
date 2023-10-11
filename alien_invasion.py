import sys
import pygame
from time import sleep
from setting import Setting
from ship import Ship
from bullet import Bullet
from button import Button
from alien import Alien
from GameStats import GameStats
from scoreboard import Scoreboard

class AlienInvasion:
    def __init__(self):
        # initialization pygame setting
        pygame.init()
        self.setting=Setting()
        # setting a screen with size 1200x800
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_height))
        # self.setting.screen_width=self.screen.get_rect().width
        # self.setting.screen_height=self.screen.get_rect().height
        # setting a caption
        pygame.display.set_caption('Alien Invasion')
        # statistics
        self.stats=GameStats(self)
        self.sb=Scoreboard(self)
        # setting ship 
        self.ship = Ship(self)
        # setting bullets
        self.bullets=pygame.sprite.Group()
        # setting aliens
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        self.play_btn=Button(self,'Play')


    def run_game(self):
        while True:
            # isolating a event-check function
            self._check_events()
            # isolating a updating new screen
            self._update_screen()
            if self.stats.game_active:
                # moving of ship
                self.ship.update()
                # moving of bullet
                self._update_bullets()
                # updating aliens
                self._update_aliens()
    def _check_events(self):
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    self._check_keydown_events(event)               
                elif event.type==pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    self._check_play_btn(mouse_pos)
    def _check_keydown_events(self,event): 
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True 
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_p:
            self._check_play_btn(event.key)
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
        elif event.key==pygame.K_q:
            sys.exit()
    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
    def _check_play_btn(self,mouse_pos):    
        if isinstance(mouse_pos,tuple):
            mouse_clicked=self.play_btn.rect.collidepoint(mouse_pos)        
            if mouse_clicked and not self.stats.game_active:
                self.start()
        elif mouse_pos==pygame.K_p:
            self.start()
    def start(self):
        self.setting.initialize_dynamic_setting()
        self.stats.reset_stat()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ship()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)
    def _create_fleet(self):
        alien=Alien(self)
        alien_width, alien_height = alien.rect.size
        availabe_space_x = self.setting.screen_width-2*alien_width
        number_alien_x = availabe_space_x//(2*alien_width)
        
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height -(3* alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x+1):
                self._creat_alien(alien_number,row_number)
            
    def _creat_alien(self,alien_number,row_number):
        alien=Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x=alien_width+2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.setting.fleet_drop_speed
        self.setting.fleet_direction*=-1

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _fire_bullet(self):
        if len(self.bullets)<self.setting.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom<=0:
                    self.bullets.remove(bullet)
        self._check_collision()
    def _check_collision(self):
        collisions = pygame.sprite.groupcollide(self.aliens,self.bullets,True,True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()    
            self.setting.increase_speed()
            self.stats.level+=1
            self.sb.prep_level()
        if collisions:
            for alien in collisions.values():
                self.stats.score+=self.setting.alien_point*len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _ship_hit(self):
        if self.stats.ship_left>0:
            self.stats.ship_left-=1
            self.sb.prep_ship()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active=False
    def _update_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.ship.blit_me()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_btn.draw_btn()
        pygame.display.flip()

if __name__=="__main__":
    ai=AlienInvasion()
    ai.run_game()
