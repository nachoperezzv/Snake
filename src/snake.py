import pygame
import random
import sys

class Snake():
    def __init__(self,init_pos):
        self.x = init_pos[0]
        self.y = init_pos[1]
        
        self.tail = []
        self.tail.append([self.x,self.y])

        self.movement = 'up'
    
    def move(self):
        if self.movement == 'up':
            self.y -= 30
        elif self.movement == 'down':
            self.y += 30
        elif self.movement == 'right':
            self.x += 30
        elif self.movement == 'left':
            self.x -= 30
    
    def add(self,pos):
        self.tail.append(pos)

    def update(self):
        self.move()

        new_tail = self.tail.copy()
        new_tail[0] = [self.x,self.y]

        for i in range(1,len(self.tail)):
            new_tail[i] = self.tail[i-1]

        self.tail = new_tail
    
    def draw(self,screen):
        for seg in self.tail:
            pygame.draw.rect(
                surface=screen,
                color='white',
                rect=pygame.Rect(seg[0],seg[1],30,30)
            )

class Fruit():
    def __init__(self):
        self.x = random.randint(0,20)*30
        self.y = random.randint(0,20)*30
        
        type = random.choice(['sandia','pomelo','naranja','pera','cereza'])
        self.image = pygame.image.load('../Include/icons/{}.png'.format(type))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Game():
    def __init__(self):

        # Inicio de juego
        self.set_game()

        # Inicio timer para fruta
        self.set_timer()
        
        # Inicio del jugador
        self.set_player()

    def set_game(self):
        pygame.init()

        self._width, self._height = 630,630
        self.screen = pygame.display.set_mode((self._width,self._height))
        self.caption = pygame.display.set_caption("Snake game")
        self.icon = pygame.display.set_icon(pygame.image.load("../Include/icons/icon.png"))

        self.clock = pygame.time.Clock()

        self.score = 0

        self.update_time = 0

        self.add_seg = False

    def set_timer(self):
        self.create_fruit = pygame.USEREVENT + 1
        pygame.time.set_timer(self.create_fruit,4000)

    def set_player(self):
        self.snake = Snake(init_pos=[300,300])
        self.fruits = []

    def display_init_window(self):
        init_text = pygame.font.Font(None,25).render('Pulsa ESPACIO para jugar', True, 'white')
        init_rect = init_text.get_rect(center=(self._width/2,self._height/2))
        
        self.screen.fill('black')
        self.screen.blit(init_text,init_rect)

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

    def run(self):
        game_state = False  # Para pantalla principal o juego
        end_game = False    # Para cuando jugador muere
        exit = False        # Para cuando jugador cierra juego

        while exit == False:

            # Catch de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]: game_state = not game_state
                    if keys[pygame.K_ESCAPE]: game_state = False
                    
                    if keys[pygame.K_RIGHT]: self.snake.movement = 'right'
                    if keys[pygame.K_LEFT]: self.snake.movement = 'left'
                    if keys[pygame.K_UP]: self.snake.movement = 'up'
                    if keys[pygame.K_DOWN]: self.snake.movement = 'down'
                
                if event.type == self.create_fruit and game_state == True:
                    self.fruits.append(Fruit())

            if game_state == True:
                self.play() 

            elif game_state == False and end_game == False:
                self.display_init_window()
                self.update_time = pygame.time.get_ticks()
            
            elif game_state == False and end_game == True:
                self.display_end_window()
                self.update_time = pygame.time.get_ticks()

            self.clock.tick(60)
            pygame.display.flip()

    def play(self):
        # Imprime fondo
        self.screen.fill('black')

        # Imprime celdas
        self.cells()

        # Movimiento serpiente
        if pygame.time.get_ticks() - self.update_time > 200:
            
            for fruit in self.fruits:
                if self.snake.tail[len(self.snake.tail)-1] == [fruit.x,fruit.y]:
                    self.score += 1
                    self.fruits.remove(fruit)
                    new_pos = self.snake.tail[len(self.snake.tail)-1]
                    self.add_seg = True
            
            self.snake.update()
            self.update_time = pygame.time.get_ticks()
            
            if self.add_seg == True:
                self.snake.add(new_pos)   
                self.add_seg = False        

        # Imprime fruta
        for fruit in self.fruits:
            fruit.draw(self.screen)

        # Imprime snake
        self.snake.draw(self.screen)

        # Imprime puntuación
        self.display_score()

    def cells(self):
        for i in range(0,self._width,30):
            for j in range(0,self._height,30):
                pygame.draw.rect(
                    surface = self.screen,
                    color=[50,50,50],
                    rect = (i,j,30,30),
                    width=1
                )

    def exit(self):
        pygame.quit()
        sys.exit()
            

