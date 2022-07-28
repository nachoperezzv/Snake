import sys
import pygame
import random

class Head(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        super().__init__()
        self.image = pygame.image.load('../Include/icons/head.png')
        self.rect = self.image.get_rect(topleft=init_pos)
    
    def move(self):
        pass

    def update(self):
        self.move()

class Body(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('../Include/icons/body.png')
        self.rect = self.image.get_rect(topleft=pos)
    
    def move(self):
        pass

    def update(self):
        pass

class Fruit(pygame.sprite.Sprite):
    def __init__(self,type,pos):
        super().__init__()
        self.image = pygame.image.load('../Include/icons/{}.png'.format(str(type)))
        self.rect = self.image.get_rect(topleft=pos)        
    
    def destroy(self):
        pass

    def update(self):
        pass

class Game():
    def __init__(self):
        # Ventana
        self.set_window()
        self.set_init_window()

        # Jugador
        self.head = Head(init_pos=(300,300))
        self.player = pygame.sprite.Group()
        self.player.add(self.head)

        # Objetos - fruta
        # self.fruit = Fruit(
        #     type=random.choice(['naranja','sandia','pomelo','pera','cereza']), 
        #     pos=(random.randint(0,30)*10,random.randint(0,30)*10)
        #     )
        self.fruit = pygame.sprite.GroupSingle()

        # Score
        self.score = 0

    def set_window(self):
        pygame.init()
    
        self._width = 630
        self._height = 630
        self.screen = pygame.display.set_mode((self._width,self._height))

        pygame.display.set_caption('Snake')
        pygame.display.set_icon(pygame.image.load('../Include/icons/icon.png'))

        self.clock = pygame.time.Clock()
    
    def set_init_window(self):
        self.init_text = pygame.font.Font(None,25).render('Pulsa ESPACIO para jugar', True, 'white')
        self.init_rect = self.init_text.get_rect(center=(self._width/2,self._height/2))

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
                    if keys[pygame.K_RIGHT]: pass
                    if keys[pygame.K_LEFT]: pass
                
            if game_state == True:
                self.screen.fill('black')

                for i in range(0,self._width,30):
                    for j in range(0,self._height,30):
                        pygame.draw.rect(
                            surface = self.screen,
                            color=[50,50,50],
                            rect = (i,j,30,30),
                            width=1
                        )

                self.player.draw(self.screen)
                self.player.update()
                
                self.display_score()

            if game_state == False: 
                self.display_init_window()

            self.clock.tick(60)
            pygame.display.flip()
            
    def display_init_window(self):      
        self.screen.fill('black')
        self.screen.blit(self.init_text,self.init_rect)
    
    def display_score(self):
        score_text = pygame.font.Font(None,20).render(f'Score: {self.score}', True, 'white')
        score_rect = score_text.get_rect(topleft=(10,10))

        self.screen.blit(score_text,score_rect)

    def close(self):
        pygame.quit()
        sys.exit()
        