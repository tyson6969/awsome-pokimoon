from settings import *
from support import draw_bar
from random import uniform
from monster import Monster


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

class MonsterSprite(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, monster, index, pos_index, entity):

        self.index = index
        self.pos_index = pos_index
        self.entity = entity
        self.monster = monster 
        self.frame_index = 0
        self.frames = frames
        self.state = 'idle'
        self.animation_speed = ANIMATION_SPEED + uniform(-1, 1)

        super().__init__(groups)
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]



    def update(self, dt): 
        self.animate(dt)

class MonsterNameSprite(pygame.sprite.Sprite):
    def __init__(self, pos, monster_sprite, groups, font):
        super().__init__(groups)
        self.monster_sprite = monster_sprite
        text_surf = font.render(monster_sprite.monster.name, False, COLORS['black'])
        padding = 10


        self.image = pygame.Surface((text_surf.get_width() + 2 * padding, text_surf.get_height() + 2 * padding))
        self.image.fill(COLORS['white'])
        self.image.blit(text_surf, (padding , padding))
        self.rect = self.image.get_frect(midtop = pos)
        
class MonsterLevelSprite(pygame.sprite.Sprite):
    def __init__(self, entity, anchor, monster_sprite, groups , font):
        super().__init__(groups)
        self.monster_sprite = monster_sprite
        self.font = font

        self.image = pygame.Surface((60,26))
        self.rect = self.image.get_frect(topleft = anchor) if entity == 'player' else self.image.get_frect(topright = anchor)
        self.xp_rect = pygame.FRect(0, self.rect.height -2 ,self.rect.width, 2)





    def update(self,_):
        self.image.fill(COLORS['white'])

        text_surf = self.font.render(f'lvl {self.monster_sprite.monster.level}', False, COLORS['black'])
        text_rect = text_surf.get_frect(center = (self.rect.width /2 , self.rect.height /2))
        self.image.blit(text_surf, text_rect)

        xp_rect = pygame.FRect(0, self.rect.height -2 ,self.rect.width, 2)
        draw_bar(self.image, self.xp_rect , self.monster_sprite.monster.xp, self.monster_sprite.monster.level_up, COLORS['black'], COLORS['white'], 0)

class MonsterStatsSprite(pygame.sprite.Sprite):
    def __init__(self,pos, monster_sprite, size, groups, fonts):
        super().__init__(groups)

        self.monster_sprite = monster_sprite
        self.image = pygame.Surface(size)
        self.rect = self.image.get_frect(midbottom = pos)
        self.font = fonts

    def update(self, _):
        self.image.fill(COLORS['white'])

        for index, (value , max_value) in enumerate(self.monster_sprite.monster.get_info()):
            color = (COLORS['red'],  COLORS['blue'], COLORS['gray'])[index]
            if index < 2:
                text_surf = self.font.render(f'{int(value)}/ {max_value}', False, COLORS['black'])
                text_rect = text_surf.get_frect(topleft = (self.rect.width * 0.05, index * self.rect.height / 2))
                bar_rect = pygame.FRect(text_rect.bottomleft + vector(0, -2), (self.rect.width * 0.9 , 4))

                self.image.blit(text_surf, text_rect)
                draw_bar(self.image , bar_rect, value, max_value, color, COLORS['black'], 2)
            else:
                pass