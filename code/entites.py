from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)

        self.frame_index, self.frames = 0, frames

        self.image = self.frames['down'][self.frame_index]
        self.rect = self.image.get_frect(center = pos)
    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED *dt
        self.image = self.frames['down'][int(self.frame_index % len(self.frames['down']))]

class Player(Entity):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups )

        self.direction = vector

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_w]:
            input_vector.y -=1 
        if keys[pygame.K_s]:
            input_vector.y +=1 
        if keys[pygame.K_d]:
            input_vector.x +=1 
        if keys[pygame.K_a]:
            input_vector.x -=1
        self.direction = input_vector
    
        

    def move(self, dt):
        self.rect.center += self.direction *  250 * dt # ur going to update this later chud maybe edit ur charcter sutff 

    def update(self, dt):
        self.input() 
        self.move(dt)
        self.animate(dt)