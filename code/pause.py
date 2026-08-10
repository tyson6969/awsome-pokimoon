# meow meow meoww


from settings import *

class Pause:
    def __init__(self, fonts, resume_game, main_menu):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.resume_game = resume_game
        self.main_menu = main_menu

        self.selection_index = 0
        self.options = ['continue', 'main menu', 'quit']
        self.button_Rects = []


        self.tint_surf = pygame.Surface(self.display_surface.get_size())
        self.tint_surf.set_alpha(200)

    def choose_option(self):
        option = self.options[self.selection_index]

        if option == 'continue':
            self.resume_game()

        if option == 'main menu':
            self.main_menu()

        if option == 'quit':
            pygame.quit()
            exit()

    def input(self, events):
        keys = pygame.key.get_just_pressed()



        if keys[pygame.K_DOWN]:
            self.selection_index = (self.selection_index  + 1) % len(self.options)

        if keys[pygame.K_UP]:
            self.selection_index = (self.selection_index - 1) % len(self.options)


        if keys[pygame.K_s]:
            self.selection_index = (self.selection_index  + 1) % len(self.options)

        if keys[pygame.K_w]:
            self.selection_index = (self.selection_index - 1) % len(self.options)

            

        if keys[pygame.K_SPACE]:
            self.choose_option()


        mouse_pos = pygame.mouse.get_pos()
        for index, rect in enumerate(self.button_Rects):
            if rect.collidepoint(mouse_pos):
                self.selection_index = index

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, rect in enumerate(self.button_Rects):
                    if rect.collidepoint(event.pos):
                        self.selection_index = index
                        self.choose_option()


    def display_menu(self):
        title_surf = self.fonts['bold'].render('paused', False, COLORS['white'])
        title_rect = title_surf.get_frect(center = (WINDOW_WIDTH / 2, 200))
        self.display_surface.blit(title_surf, title_rect)
        self.button_Rects = []

        for index, option in enumerate(self.options):
            selected = index == self.selection_index
            font = self.fonts['bold'] if selected else self.fonts['regular']
            colors = COLORS['red'] if selected else COLORS['white']
            text_surf = font.render(option, False, colors)
            if selected:
                text_surf = pygame.transform.scale_by(text_surf, 1.25)

            text_rect = text_surf.get_frect(center = (WINDOW_WIDTH / 2 , 270+ index * 60))
            button_rect = text_rect.inflate(20, 16)

            if selected:
                pygame.draw.rect(self.display_surface, COLORS['dark white'], button_rect, 0, 5)
                pygame.draw.rect(self.display_surface, COLORS['white'], button_rect, 2, 5)

            self.display_surface.blit(text_surf, text_rect)
            self.button_Rects.append(button_rect)


        


    def update(self,dt, events):
        self.input(events)
        self.display_surface.blit(self.tint_surf, (0,0))
        self.display_menu()