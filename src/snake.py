import sys
import pygame

class Game():
    def __init__(self):
        self.set_window()
    
    def set_window(self):
        pygame.init()
        pygame.display.set_caption('Snake')
        pygame.display.set_icon('../Include/icons/icon.png')

        self._width = 800
        self._height = 800
        self.screen = pygame.display.set_mode((self._width,self._height))

        self.clock = pygame.time.Clock()

    def run(self):
        quit = False
        game_state = False

        while quit == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True

                if event.type == pygame.KEYDOWN: 
                    keys = pygame.key.get_pressed()

                    # Estado del juego
                    if keys[pygame.K_SPACE]: game_state = not game_state
                    if keys[pygame.K_ESCAPE]: game_state = False

                    # Movimiento
                    if keys[pygame.K_UP]: pass
                    if keys[pygame.K_DOWN]: pass
                    if keys[pygame.K_RIGHT]: pass
                    if keys[pygame.K_LEFT]: pass
                
            if game_state == True:
                # Pantalla de juego
                pass

            if game_state == False: 
                # Pantalla de carga
                pass

            self.clock.tick(60)
            pygame.display.flip()
            

    def close(self):
        pygame.quit()
        sys.exit()
        