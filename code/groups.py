from settings import * 
from support import import_image
from entites import Entity

class ALLsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset= vector()
        self.shadow_surface = import_image('graphics', 'other', 'shadow')
        self.notice_surf = import_image('graphics', 'ui', 'notice')

    def draw(self, player):
        self.offset.x = -(player.rect.centerx - WINDOW_WIDTH / 2)
        self.offset.y = -(player.rect.centery - WINDOW_HEIGHT / 2)

        bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['main'] ]
        main_sprites = sorted([sprite for sprite in self if sprite.z == WORLD_LAYERS['main'] ], key = lambda sprite: sprite.y_sort)
        fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['main'] ]

        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                if isinstance(sprite, Entity):
                    self.display_surface.blit(self.shadow_surface, sprite.rect.topleft + self.offset + vector(40,110))
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
                if sprite == player and player.noticed:
                    rect = self.notice_surf.get_frect(midbottom = sprite.rect.midtop )
                    self.display_surface.blit(self.notice_surf, rect.topleft + self.offset)
