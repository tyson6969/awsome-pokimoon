from settings import  *

class CharacterSelect:
    def __init__(self, character_frames , fonts, confirm_character):
        self.display_surface = pygame.display.get_surface()
        self.character_frames = character_frames
        self.fonts = fonts
        self.confirm_character = confirm_character

        self.characters = ['player', 'blond', 'hat_girl', 'purple_girl', 'straw', 'young_girl', 'young_guy']
        self.characters_name = ['Tyson', 'blondie', 'stacy', 'meower', 'straw head', 'alex', 'i10(fly high🕊️ )'] #ts IS not ai twin i added the emoji myself fly high i tinnie
        self.index = 0
        self.frame_index = 0

        self.confirm_rect = pygame.FRect(0,0, 160, 50).move_to(center = (WINDOW_WIDTH /2 , WINDOW_HEIGHT  - 100))
        self.arrow_rects = {}

    def input(self,events):
        keys = pygame.key.get_just_pressed()

        if keys[pygame.K_RIGHT]:
            self.index = (self.index + 1) % len(self.characters)
        if keys[pygame.K_LEFT]:
            self.index = (self.index - 1) % len(self.characters)

        if keys[pygame.K_a]:
            self.index = (self.index + 1) % len(self.characters)
        if keys[pygame.K_d]:
            self.index = (self.index - 1) % len(self.characters)

        if keys[pygame.K_SPACE]:
            self.confirm_character(self.characters[self.index]) 


        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.arrow_rects.get('left') and self.arrow_rects['left'].collidepoint(event.pos):
                    self.index = (self.index -1 ) % len(self.characters)

                if self.arrow_rects.get('right') and self.arrow_rects['right'].collidepoint(event.pos):
                    self.index = (self.index  + 1) % len(self.characters)

                if self.confirm_rect.collidepoint(event.pos):
                    self.confirm_character(self.characters[self.index])


    def title(self):
        title_surf = self.fonts['bold'].render('choose your character', False, COLORS['white'])
        title_rect = title_surf.get_frect(center = (WINDOW_WIDTH / 2, 100))
        self.display_surface.blit(title_surf, title_rect)


    def display_character(self,dt):
        name = self.characters[self.index]
        frames = self.character_frames[name]['down_idle']

        self.frame_index += ANIMATION_SPEED * dt 
        surf = frames[int(self.frame_index) % len(frames)]
        surf = pygame.transform.scale2x(surf)
        rect = surf.get_frect(center = (WINDOW_WIDTH / 2 , WINDOW_HEIGHT / 2))
        self.display_surface.blit(surf, rect)

        name_surf = self.fonts['regular'].render(self.characters_name[self.index], False, COLORS['white'])
        name_rect = name_surf.get_frect(midtop = rect.midbottom + vector(0, 20))
        self.display_surface.blit(name_surf, name_rect)

    def arrows(self):
        left_surf = self.fonts['bold'].render('<', False, COLORS['white'])
        left_rect = left_surf.get_frect(midright = (WINDOW_WIDTH / 2 - 160, WINDOW_HEIGHT / 2))
        self.display_surface.blit(left_surf, left_rect)
        self.arrow_rects['left'] = left_rect.inflate(30, 30)

        right_surf = self.fonts['bold'].render('>', False, COLORS['white'])
        right_rect = right_surf.get_frect(midleft = (WINDOW_WIDTH / 2 + 160, WINDOW_HEIGHT / 2))
        self.display_surface.blit(right_surf, right_rect)
        self.arrow_rects['right'] = right_rect.inflate(30, 30)

    def confirm(self):
        pygame.draw.rect(self.display_surface, COLORS['dark white'], self.confirm_rect, 0, 5)
        pygame.draw.rect(self.display_surface, COLORS['white'], self.confirm_rect, 2, 5)

        text_surf = self.fonts['regular'].render('confirm', False, COLORS['red'])
        text_rect = text_surf.get_frect(center = self.confirm_rect.center)
        self.display_surface.blit(text_surf, text_rect)





    def update(self, dt , events):
        self.input(events)
        self.display_surface.fill(COLORS['dark'])
        self.title()
        self.display_character(dt)
        self.arrows()
        self.confirm()
        
