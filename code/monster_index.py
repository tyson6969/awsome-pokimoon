from settings import *


class MonsterIndex:
    def __init__(self, monsters, fonts):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts

        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)



    def update(self, dt):
        self.display_surface.blit(self.tint_surf, (0,0))
