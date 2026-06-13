from settings import *
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf , groups, z = WORLD_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
        self.frame_index, self.frames = 0, frames 
        super().__init__(pos, frames[self.frame_index], groups, z)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, dt):
        self.animate(dt)