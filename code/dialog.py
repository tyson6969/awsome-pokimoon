from settings import *


class DialogTree:
    def __init__(self, character, player, all_sprites, font):
        self.player = player
        self.character = character
        self.font = font
        self.all_sprites = all_sprites
        print(character.get_dialog())