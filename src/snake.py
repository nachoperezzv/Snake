import enum
import sys
from pip import main
import pygame
import random

class Head(pygame.sprite.Sprite):
    def __init__(self,init_pos):
        super().__init__()
        img1 = pygame.image.load('../Include/icons/head.png')
        img2 = pygame.image.load('../Include/icons/head_r.png')
        img3 = pygame.image.load('../Include/icons/head_l.png')
        img4 = pygame.image.load('../Include/icons/head_d.png')
        self.images = {'up':img1,'right':img2,'left':img3,'down':img4}

        self.image = self.images['up']
        self.rect = self.image.get_rect(topleft=init_pos)

        self.pos = init_pos
        self.delta = 0
        self.movement = 'up'

        self.time = 0
    
    def move(self):
        if pygame.time.get_ticks() - self.time > 300:
            if self.movement == 'up':
                self.image = self.images['up']
                self.rect.y -= 30
            elif self.movement == 'down':
                self.image = self.images['down']
                self.rect.y += 30
            elif self.movement == 'right':
                self.image = self.images['right']
                self.rect.x += 30
            elif self.movement == 'left':
                self.image = self.images['left']
                self.rect.x -= 30
            self.time = pygame.time.get_ticks()
    
    def out_of_limits(self):
        if (self.rect.x < 0 or self.rect.x > 600 or 
            self.rect.y < 0 or self.rect.y > 600):
            return True
        else:
            return False

    def update(self):
        self.move()


class Body(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('../Include/icons/body.png')
        self.rect = self.image.get_rect(topleft=pos)

        self.pos = pos

        self.time = 0
    
    def move(self):
        if pygame.time.get_ticks() - self.time > 300:
            self.rect.topleft = self.pos
            self.time = pygame.time.get_ticks()
            print('move body')

    def update(self):
        self.move()


class Fruit(pygame.sprite.Sprite):
    def __init__(self,type,pos):
        super().__init__()
        self.image = pygame.image.load('../Include/icons/{}.png'.format(str(type)))
        self.rect = self.image.get_rect(topleft=pos)     

        self.pos = pos   
    
    def destroy(self):
        pass

    def update(self):
        pass

class Game():
    def __init__(self):
        # Ventana
        self.set_window()
        self.set_init_window()

        # Timer
        self.set_timers()

        # Jugador
        self.head = Head(init_pos=(300,300))
        self.player = pygame.sprite.Group()
        self.player.add(self.head)

        # Objetos - fruta
        self.rewards = pygame.sprite.Group()
        self.rewards.add(
            Fruit(
                type=random.choice(['naranja','sandia','pomelo','pera','cereza']), 
                pos=(random.randint(0,20)*30,random.randint(0,20)*30)
            )
        )

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

    def set_timers(self):
        self.create_fruit = pygame.USEREVENT + 1
        pygame.time.set_timer(self.create_fruit,5000)

    def run(self):
        quit = False
        game_state = False
        end_state = False

        while quit == False:
            # Eventos
            for event in pygame.event.get():

                # Fin de juego
                if event.type == pygame.QUIT:
                    quit = True

                # Teclado
                if event.type == pygame.KEYDOWN: 
                    keys = pygame.key.get_pressed()

                    # Estado del juego
                    if keys[pygame.K_SPACE]: game_state = not game_state
                    if keys[pygame.K_ESCAPE]: game_state = False

                    # Movimiento
                    if keys[pygame.K_RIGHT]: self.head.movement='right'
                    if keys[pygame.K_LEFT]: self.head.movement='left'
                    if keys[pygame.K_UP]: self.head.movement='up'
                    if keys[pygame.K_DOWN]: self.head.movement='down'
                
                # Creación de fruta
                if event.type == self.create_fruit and game_state:
                    self.rewards.add(
                        Fruit(
                            type=random.choice(['naranja','sandia','pomelo','pera','cereza']), 
                            pos=(random.randint(0,20)*30,random.randint(0,20)*30)
                        )
                    )
                
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

                self.rewards.draw(self.screen)
                self.rewards.update()

                player_list = self.player.sprites()
                last = this = player_list[0].pos
                for i,e in enumerate(player_list):
                    if i > 0:
                        this = e.pos
                        e.pos = last
                    last = this        

                self.player.draw(self.screen)        
                self.player.update()

                for fruit in self.rewards:
                    if bool(pygame.sprite.spritecollide(fruit,self.player,True)):
                        self.score += 1
                        self.player.add(Body(fruit.pos))
                        fruit.kill()
                
                if self.head.out_of_limits():
                    self.player.remove()
                    end_state = True
                
                self.display_score()

            if game_state == False: 
                self.display_init_window()

            if end_state == True:
                self.display_end_window()

            self.clock.tick(60)
            pygame.display.flip()
            
    def display_init_window(self):      
        self.screen.fill('black')
        self.screen.blit(self.init_text,self.init_rect)
    
    def display_score(self):
        score_text = pygame.font.Font(None,20).render(f'Score: {self.score}', True, 'white')
        score_rect = score_text.get_rect(topleft=(10,10))

        self.screen.blit(score_text,score_rect)
    
    def display_end_window(self):
        self.screen.fill('black')

        end_text = pygame.font.Font(None,40).render('Bien jugado!!', True, 'white')
        end_rect = end_text.get_rect(center=(self._width/2,200))

        score_text = pygame.font.Font(None,30).render(f'Score: {self.score}', True, 'white')
        score_rect = score_text.get_rect(center=(self._width/2,400))

        self.screen.blit(end_text,end_rect)
        self.screen.blit(score_text,score_rect)

    def close(self):
        pygame.quit()
        sys.exit()



            

