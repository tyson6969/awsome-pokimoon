import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '-1400,0' # remove later, this just for me


from settings import *
from game_data import *
from pytmx.util_pygame import load_pygame 
from os.path import join

from sprites import Sprite, AnimatedSprite, MonsterPatchSprite, BorderSprite, CollidableSprite, TransitionSprite
from entites import Player, Character
from groups import ALLsprites
from dialog import DialogTree
from support import *
from monster import Monster
from monster_index import MonsterIndex


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("awsome pokimoon")
        self.clock = pygame.time.Clock()

        self.player_monsters = {
        0: Monster('Plumette', 30),
        1: Monster('Ivieron', 29),
        2: Monster('Pluma', 28),
        3: Monster('Sparchu', 27),
        4: Monster('Cindrill', 26),
        5: Monster('Charmadillo', 25),
        6: Monster('Finsta', 24),
        7: Monster('Gulfin', 23),
        8: Monster('Finiette', 22),
        9: Monster('Atrox', 21),
        10: Monster('Pouch', 20),
        11: Monster('Draem', 19),
        12: Monster('Larvea', 18),
        13: Monster('Cleaf', 17),
        14: Monster('Jacana', 16),
        15: Monster('Friolera', 15),
            }
        


        # shi groupsd
        self.all_sprites = ALLsprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()

        
        self.transition_target = None
        self.tint_Surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)) # use this later chud
        self.tint_mode = 'untint'
        self.tint_progress = 0 
        self.tint_direction = -1
        self.tint_speed = 600 


        self.import_assets()
        self.setup(self.tmx_maps['world'], 'house')
        self.dialog_tree = None

        self.monster_index = MonsterIndex(self.player_monsters, self.fonts, self.monster_frames)
        
        self.index_open = False


    def import_assets(self):
        self.tmx_maps = tmx_importer('data', 'maps')
        
        self.overworld_frames = { 'water': import_folder('graphics', 'tilesets', 'water'),
                                 'coast': coast_importer(24, 12 , 'graphics' , 'tilesets', 'coast'),
                                 'characters': all_character_import('graphics', 'characters') }
        

        self.monster_frames = {
            'icons': import_folder_dict('graphics', 'icons' ),
            'monsters': monster_importer(4,2,'graphics', 'monsters')
        }
        print(self.monster_frames['monsters'])
        



        self.fonts = {
            'dialog': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 30),
            'regular': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 18),
            'small': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 14),
            'bold': pygame.font.Font(join('graphics', 'fonts', 'dogicapixelbold.otf'), 20),
        }

        
    

    def setup(self, tmx_map, player_start_pos):

        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
            group.empty()

        for layer in ['Terrain', 'Terrain Top']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf , self.all_sprites, WORLD_LAYERS['bg'])


        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height ), TILE_SIZE):
                    AnimatedSprite((x,y), self.overworld_frames['water'] , self.all_sprites, WORLD_LAYERS['water'] )

        for obj in tmx_map.get_layer_by_name('Coast'):
            terrain = obj.properties['terrain']
            side = obj.properties['side']
            AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites, WORLD_LAYERS['bg'] )

        for obj in tmx_map.get_layer_by_name("Objects"): #line 67 6767 76767 77676 7 67777777777777777777777777777 676766767
            if obj.name == 'top':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'] )
            else:
                CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites) )

        #trans vro i am crine

        for obj in tmx_map.get_layer_by_name('Transition'):
            TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites )
            
        for obj in tmx_map.get_layer_by_name('Collisions'):
            BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in tmx_map.get_layer_by_name("Monsters"):
            MonsterPatchSprite((obj.x, obj.y), obj.image, self.all_sprites, obj.properties['biome'] )

        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == 'Player' :
                if obj.properties['pos'] == player_start_pos: 
                    self.player = Player(
                        pos = (obj.x, obj.y),
                        frames =  self.overworld_frames['characters']['player'], 
                        groups = self.all_sprites,
                        facing_direction=obj.properties['direction'],
                        collision_sprites = self.collision_sprites)
                    
            else:
                Character(
                        pos = (obj.x, obj.y),
                        frames =  self.overworld_frames['characters'][obj.properties['graphic']], 
                        groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
                        facing_direction= obj.properties['direction'],
                        character_data = TRAINER_DATA[obj.properties['character_id']],
                        player = self.player
                        , create_dialog= self.create_dialog , 
                        collision_sprites= self.collision_sprites
                        , radius = obj.properties['radius']) 
                        
                
    def input(self):
        if not self.dialog_tree:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_SPACE]:
                for character in self.character_sprites: # yo chud ur going to use this later
                    if check_connections(100, self.player, character):
                        self.player.block()
                        character.change_facing_direction(self.player.rect.center)
                        self.create_dialog(character)
                        character.can_rotate = False
            
            if keys[pygame.K_RETURN]:
                self.index_open = not self.index_open
                self.player.blocked = not  self.player.blocked
        
    def create_dialog(self,character):
        if not self.dialog_tree:
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)
    
    

    def end_dialog(self, character):
        self.dialog_tree = None 
        self.player.unblock()
        

    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.player.block()
            self.transition_target = sprites[0].target
            self.tint_mode = 'tint'


    def tint_screen(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt

        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if self.tint_progress >= 255:
                self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
                self.tint_mode = 'untint'
                self.transition_target = None

        self.tint_progress = max(0, min(self.tint_progress, 255))
        self.tint_Surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_Surf, (0,0))

    def run (self):
        while True:
            dt = self.clock.tick(180) / 1000 
            #merow event loop

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            # SHI GAME LOGIC
            self.input()
            self.all_sprites.update(dt)
            self.transition_check()
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player)

            if self.dialog_tree:
                self.dialog_tree.update()
            if self.index_open:
                self.monster_index.update(dt)


            self.tint_screen(dt)
            pygame.display.update()
            
if __name__ == '__main__':
    game = Game()
    game.run()




