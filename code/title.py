from settings import *

class Title:
    def __init__(self, fonts, start_game, audio):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.start_game = start_game
        self.audio = audio

        self.selection_index = 0
        self.menu = 'main'
        self.options = ['play', 'settings', 'instructions', 'quit']
        self.button_rects = []

        self.settings_index = 0
        self.settings_options = ["sound", 'purple???']
        self.settings_rects = []

        self.sound_on = True
        self.purple = False
        self.bg_colors = COLORS['water'] # maybe use later u chud duck





    def choose_option(self):
        option = self.options[self.selection_index]

        if option == 'play':
            self.start_game()

        if option == 'quit':
            pygame.quit()
            exit()
                

        if option == 'settings':
            self.menu = 'settings'

        if option == 'instructions':
            self.menu = 'instructions'



            



    

    def input(self, events):
        keys = pygame.key.get_just_pressed()

        if self.menu != 'main':
            if keys[pygame.K_ESCAPE]:
                self.menu = 'main'

            return

        if keys[pygame.K_DOWN]:
            self.selection_index = (self.selection_index + 1) % len(self.options)


        if keys[pygame.K_UP]:
            self.selection_index = (self.selection_index - 1) % len(self.options)

        if keys[pygame.K_s]:
            self.selection_index = (self.selection_index + 1) % len(self.options)
            

        if keys[pygame.K_w]:
            self.selection_index = (self.selection_index - 1) % len(self.options)

        if keys[pygame.K_SPACE]:
            self.choose_option()

        if keys[pygame.K_KP_ENTER]:
            self.choose_option()

        mouse_pos = pygame.mouse.get_pos()

        for index, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.selection_index = index

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for index, rect in enumerate(self.button_rects):
                        if rect.collidepoint(event.pos):
                            self.selection_index = index
                            self.choose_option()
                            


    def display_menu(self):
        title_surf = self.fonts['bold'].render('AWESOME POKIMOON', False, COLORS['white']) #ts temp will replace
        title_rect = title_surf.get_frect(center =  (WINDOW_WIDTH/ 2, 200))
        self.display_surface.blit(title_surf, title_rect)
        self.button_rects = []

        for index, option in enumerate(self.options):
            
            selected = index == self.selection_index

            font = self.fonts['bold'] if selected else self.fonts['regular']
            color = COLORS['red'] if selected else COLORS['white']
            text_surf = font.render(option, False, color)

            if selected:
                text_surf = pygame.transform.scale_by(text_surf, 1.25)

            text_rect = text_surf.get_frect(center = (WINDOW_WIDTH /2 , 270 + index * 60))
            button_rect = text_rect.inflate(30, 16)

            if selected:
                pygame.draw.rect(self.display_surface, COLORS['dark white'], button_rect, 0, 5)
                pygame.draw.rect(self.display_surface, COLORS['white'], button_rect, 2, 5)

            self.display_surface.blit(text_surf, text_rect)
            self.button_rects.append(button_rect)

    def display_instructions(self):
        text_surf = self.fonts['bold'].render('how to play', False, COLORS['white'])
        text_rect = text_surf.get_frect (center = (WINDOW_WIDTH /2 , 80))
        self.display_surface.blit(text_surf, text_rect)


        instructions = [
            'WASD or ARROW keys to move',
            'SPACE: interact and select options',
            'ENTER: open monster index',
            '',
            'fight monsters to gain XP and level up',
            'catch monsters to add them to your collection',
            'DEFEAT TRAINERS TO PROGRESS',
            'Visit the nurse to heal your monsters to restore their health and energy',
            '',
            'ESC OR SPACE:go back'
        ]


        for index, text in enumerate(instructions):
            text_surf = self.fonts['regular'].render(text, False, COLORS['white'])
            text_rect = text_surf.get_frect(center = (WINDOW_WIDTH / 2, 150 + index * 30))
            self.display_surface.blit(text_surf, text_rect)


        def display_settings(self):
            pass






    def update(self, dt, events):
        self.input(events)
        self.display_surface.fill(COLORS['water'])


        if self.menu == 'main':
            self.display_menu()

        if self.menu == 'instructions':
            self.display_instructions()



    