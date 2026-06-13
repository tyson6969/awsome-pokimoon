from settings import * 


class ALLsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset= vector()

    def draw(self, player_center):
        self.offset.x = -(player_center[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_center[1] - WINDOW_HEIGHT / 2)

        bg_sprites = [sprite for sprite in self if sprite.z < WORLD_LAYERS['main'] ]
        main_sprites = [sprite for sprite in self if sprite.z == WORLD_LAYERS['main'] ]
        fg_sprites = [sprite for sprite in self if sprite.z > WORLD_LAYERS['main'] ]

        for layer in (bg_sprites, main_sprites, fg_sprites):
            for sprite in layer:
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
