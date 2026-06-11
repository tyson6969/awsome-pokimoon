from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("awsome pokimoon")

    def run (self):
        while True:
            #merow event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            # SHI GAME LOGIC
            pygame.display.update() 
if __name__ == '__main__':
    game = Game()
    game.run()




