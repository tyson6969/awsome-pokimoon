from settings import *
from timer import Timer

class Evoloution:
    def __init__(self, frames, start_monster, end_monster, font, end_evolution):
        self.display_surface = pygame.display.get_surface()
        self.start_monster_surf = pygame.transform.scale2x(frames[start_monster]['idle'][0])
        self.end_monster_surf = pygame.transform.scale2x(frames[end_monster]['idle'][0])
        self.timers= {
            'start': Timer(800, autostart = True),
            'end': Timer(1800, func = end_evolution)

        }
        self.tint_surf = pygame.Surface(self.display_surface.get_size())
        self.tint_surf.set_alpha(200)

        self.start_monster_surf_white = pygame.mask.from_surface(self.start_monster_surf).to_surface()
        self.start_monster_surf_white.set_colorkey('black')
        self.tint_amount, self.tint_speed = 0, 120
        self.start_monster_surf_white.set_alpha(self.tint_amount)

    def update(self,dt):
        for timer in self.timers.values():
            timer.update()

        if not self.timers['start'].active:
            self.display_surface.blit(self.tint_surf, (0,0))
            if self.tint_amount < 255:
                rect = self.start_monster_surf.get_frect(center = (WINDOW_WIDTH / 2 ,WINDOW_HEIGHT /2))
                self.display_surface.blit(self.start_monster_surf, rect)

                self.tint_amount += self.tint_speed * dt
                self.start_monster_surf_white.set_alpha(self.tint_amount)
                self.display_surface.blit(self.start_monster_surf_white, rect)
            else:
                rect = self.end_monster_surf.get_frect(center = (WINDOW_WIDTH /2 , WINDOW_HEIGHT /2) )
                self.display_surface.blit(self.end_monster_surf, rect)

                if not self.timers['end'].active: self.timers['end'].activate()

            