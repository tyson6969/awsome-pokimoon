from settings import *
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf , groups, z = WORLD_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z
        self.y_sort = self.rect.centery
        self.hitbox = self.rect.copy()


class BorderSprite(Sprite):
    def __init__(self, pos, surf, groups,):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()

class TransitionSprite(Sprite):
    def __init__(self, pos, size, target, groups):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.target = target


class CollidableSprite(Sprite):
    def __init__(self, pos, surf, groups,):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(0, -self.rect.height * 0.6)

class MonsterPatchSprite(Sprite):
    def __init__(self, pos, surf , groups, biome):
        self.biome = biome 
        super().__init__(pos, surf , groups, WORLD_LAYERS['main' if biome != 'sand' else 'bg'])
        self.y_sort -= 40




class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
        self.frame_index, self.frames = 0, frames 
        super().__init__(pos, frames[self.frame_index], groups, z)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)