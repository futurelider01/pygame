class Setting:
    def __init__(self) -> None:
        # Initialization settings
        # Params of display
        self.screen_width=1600
        self.screen_height=800
        self.bg_color=(170,170,170)
        self.ship_limit=3
        # Bullet settings
        self.bullet_height=25
        self.bullet_width=10
        self.bullet_color=(60,60,60)
        self.bullets_allowed=60
        self.fleet_drop_speed=10
        # Alien setting
        self.alien_speed=1.0
        self.ship_speed=1.5
        self.bullet_speed=3.0

        self.speedup_scale=1.1
        self.score_scale=1.5
        self.initialize_dynamic_setting()
    def initialize_dynamic_setting(self):
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.alien_speed=1.0
        self.fleet_direction=1
        self.alien_point=50
    def increase_speed(self):
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        self.alien_point=int(self.alien_point*self.score_scale)
        