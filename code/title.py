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
        self.settings_options = ["music", 'purple???']
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



    def change_Setting(self):
        option = self.settings_options[self.settings_index]

        if option == 'music':
            self.sound_on = not self.sound_on

            for sound in self.audio.values():
                sound.set_volume(1 if self.sound_on else 0)

        if option == 'purple???':
            self.purple = not self.purple

            if self.purple:
                self.bg_colors = COLORS['purple']

            else:
                self.bg_colors = COLORS['water']





    def input(self, events):
        keys = pygame.key.get_just_pressed()

        if self.menu == 'settings':
            if keys[pygame.K_ESCAPE]:
                self.menu = 'main'
                return


            if keys[pygame.K_DOWN]:
                self.settings_index = (self.settings_index + 1) % len(self.settings_options)

            if keys[pygame.K_UP]:
                self.settings_index = (self.settings_index - 1)%len(self.settings_options)

            if keys[pygame.K_s]:
                self.settings_index = (self.settings_index + 1) % len(self.settings_options)

            if keys[pygame.K_w]:
                self.settings_index = (self.settings_index - 1)%len(self.settings_options)

            if keys[pygame.K_SPACE]:
                self.change_Setting()

            mouse_pos = pygame.mouse.get_pos()

            for index, rect in enumerate(self.settings_rects):
                if rect.collidepoint(mouse_pos):
                    self.settings_index = index

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for index, rect in enumerate(self.settings_rects):
                            if rect.collidepoint(event.pos):
                                self.settings_index = index
                                self.change_Setting()
            return


        if self.menu == 'instructions':
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
        title_surf = self.fonts['bold'].render('settings', False, COLORS['white'])
        title_rect = title_surf.get_frect(center = (WINDOW_WIDTH / 2 ,100))
        self.display_surface.blit(title_surf, title_rect)


        self.settings_rects = []

        for index, option in enumerate(self.settings_options):
            selected = index == self.settings_index
            checked = self.sound_on if option == 'msuic' else self.purple
            label = 'msuic' if option == 'music' else 'purple?????'

            row_rect = pygame.FRect(0, 0, 310, 50).move_to(center = (WINDOW_WIDTH / 2, 250 + index * 70))

            if selected:
                pygame.draw.rect(self.display_surface, COLORS['dark white'], row_rect, 0, 5)
                pygame.draw.rect(self.display_surface, COLORS['white'], row_rect, 2, 5) # check ts chud

            font = self.fonts['bold'] if selected else self.fonts['regular']
            color = COLORS['red'] if selected else COLORS['white']
            text_surf = font.render(label, False, color)
            # text_surf = font.render(label, True, color) #hmmm i wonder how it looks if i made it true will see tho
            text_rect = text_surf.get_frect(midleft = row_rect.midleft + vector(20, 0))
            self.display_surface.blit(text_surf, text_rect)

            box_rect = pygame.FRect(0,0, 26,26).move_to(midright = row_rect.midright + vector(-20,0))
            pygame.draw.rect(self.display_surface, COLORS['white'], box_rect, 2,4)

            if checked:
                pygame.draw.rect(self.display_surface, COLORS['gold'], box_rect.inflate(-10, -10), 0, 2)
                self.settings_rects.append(row_rect)











    def update(self, dt, events):
        self.input(events)

        self.display_surface.fill(self.bg_colors)
        


        if self.menu == 'main':
            self.display_menu()

        if self.menu == 'instructions':
            self.display_instructions()

        if self.menu == 'settings':          
            self.display_settings()



    