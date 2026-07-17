from settings import *


class MonsterIndex:
    def __init__(self, monsters, fonts, monster_frames):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.monsters = monsters
        self.icon_frames = monster_frames['icons']

        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)


        self.main_rect = pygame.FRect(0,0, WINDOW_WIDTH * 0.6 , WINDOW_HEIGHT * 0.8).move_to(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.visible_items = 6
        self.list_width = self.main_rect.width * 0.3
        self.item_height = self.main_rect.height / self.visible_items

    def display_list(self):
        for index, monster in self.monsters.items():
            top = self.main_rect.top + index * self.item_height
            item_rect = pygame.FRect(self.main_rect.left, top ,self.list_width, self.item_height)

            text_surf = self.fonts['regular'].render(monster.name, False, COLORS['white'])
            text_rect = text_surf.get_frect(midleft = item_rect.midleft + vector(90, 0))

            icon_surf = self.icon_frames[monster.name]
            icon_rect = icon_surf.get_frect(center = item_rect.midleft + vector(45, 0))
            pygame.draw.rect(self.display_surface, COLORS['gray'], item_rect)
            self.display_surface.blit(icon_surf, icon_rect)
            self.display_surface.blit(text_surf, text_rect)

    def update(self, dt):
        self.display_surface.blit(self.tint_surf, (0,0))
        pygame.draw.rect(self.display_surface, 'black', self.main_rect)
        self.display_list()
