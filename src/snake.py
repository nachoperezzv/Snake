from cgitb import text
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

        self.up = pygame.image.load('../Include/icons/head.png')
        self.down = pygame.image.load('../Include/icons/head_d.png')
        self.right = pygame.image.load('../Include/icons/head_r.png')
        self.left = pygame.image.load('../Include/icons/head_l.png')

        self.images = {
            'up': self.up,
            'down': self.down,
            'right': self.right,
            'left': self.left
        }

        self.image = self.images[self.movement]

        self.dead_sound = pygame.mixer.Sound('../Include/sounds/dead.wav')
    
    def move(self):
        if self.movement == 'up':
            self.y -= 30
        elif self.movement == 'down':
            self.y += 30
        elif self.movement == 'right':
            self.x += 30
        elif self.movement == 'left':
            self.x -= 30
        
        self.image = self.images[self.movement]
    
    def add(self,pos):
        self.tail.append(pos)

    def update(self):
        self.move()

        new_tail = self.tail.copy()
        new_tail[0] = [self.x,self.y]

        for i in range(1,len(self.tail)):
            new_tail[i] = self.tail[i-1]

        self.tail = new_tail
    
    def limits(self):
        if (self.x < 0 or self.x > 630 or 
            self.y < 0 or self.y > 630):
            self.dead_sound.play()
            return True
        else:
            return False

    def itself(self):
        for i in range(1,len(self.tail)):
            if [self.x,self.y] == self.tail[i]:
                self.dead_sound.play()
                return True
        return False

    def draw(self,screen):
        for i,seg in enumerate(self.tail):
            if i == 0:
                rect = self.image.get_rect(topleft=(seg[0],seg[1]))
                screen.blit(self.image,rect)
            else:
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

        # Inicio sonidos
        self.set_sounds()

        # Inicio botón
        self.set_buttons()

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

    def set_sounds(self):
        self.eat_sound = pygame.mixer.Sound('../Include/sounds/eat.wav')

    def set_buttons(self):
        self.restart_button = Button(
            text='<-',
            left=560,top=60,width=30,height=30,
            font=pygame.font.Font(None,20)
        )

    def restart_game(self):
        del self.snake
        del self.fruits

        self.score = 0
        self.update_time = 0
        self.add_seg = 0

        self.set_player()

        self.game_state = True
        self.end_game = False

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

        self.display_button()
    
    def display_button(self):
        if self.restart_button.draw(self.screen):
            self.restart_button.pressed = False
            self.restart_game()

    def run(self):
        self.game_state = False  # Para pantalla principal o juego
        self.end_game = False    # Para cuando jugador muere
        exit = False        # Para cuando jugador cierra juego

        while exit == False:

            # Catch de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]: self.game_state = not self.game_state
                    if keys[pygame.K_ESCAPE]: self.game_state = False
                    
                    if keys[pygame.K_RIGHT]: self.snake.movement = 'right'
                    if keys[pygame.K_LEFT]: self.snake.movement = 'left'
                    if keys[pygame.K_UP]: self.snake.movement = 'up'
                    if keys[pygame.K_DOWN]: self.snake.movement = 'down'
                
                if event.type == self.create_fruit and self.game_state == True:
                    self.fruits.append(Fruit())

            if self.game_state == True:
                self.play() 

            elif self.game_state == False and self.end_game == False:
                self.display_init_window()
                self.update_time = pygame.time.get_ticks()
            
            elif self.game_state == False and self.end_game == True:
                self.display_end_window()
                self.update_time = pygame.time.get_ticks()

            self.clock.tick(60)
            pygame.display.flip()

    def play(self):
        # Imprime fondo
        self.screen.fill('black')

        # Imprime celdas
        self.cells()

        # Movimiento serpiente y check come fruta
        if pygame.time.get_ticks() - self.update_time > 200:
            
            for fruit in self.fruits:
                if [self.snake.x,self.snake.y] == [fruit.x,fruit.y]:
                    self.score += 1
                    self.eat_sound.play()

            for fruit in self.fruits:
                if self.snake.tail[len(self.snake.tail)-1] == [fruit.x,fruit.y]:
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
        
        # Check limites
        if self.snake.limits() or self.snake.itself():
            self.end_game = True
            self.game_state = False

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


class Button:
    def __init__(
                    self,text,left,top,width,height,
                    font, elevation=3, 
                    text_color=[255,255,255],
                    btn_color_on=[195,195,195], btn_color_off=[175,175,175],
                    btn_color_bg=[25,25,25],
                    border_radius = 6
                ):

        #Core attributes 
        self.pressed            = False
        self.elevation          = elevation
        self.dynamic_elecation  = elevation
        self.pos                = (left,top)
        self.width              = width
        self.height             = height
        self.color_on           = btn_color_on
        self.color_off          = btn_color_off
        self.color_bg           = btn_color_bg
        self.border_radius      = border_radius
        # top rectangle 
        self.top_rect = pygame.Rect(self.pos,(self.width,self.height))
        self.top_color = self.color_off

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(self.pos,(self.width,self.height))
        self.bottom_color = self.color_bg
        #text
        self.text_surf = font.render(text,True,text_color)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self, screen):
    # elevation logic 
        self.top_rect.y = self.pos[1] - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = self.border_radius)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = self.border_radius)
        screen.blit(self.text_surf, self.text_rect)
        return self.check_click()

    def check_click(self,kwargs=None):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.color_on
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    return True
                    # if kwargs == None:
                    #     function()
                    # else:
                    #     function(**kwargs)
                    # self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.color_off
            return False
        
    def get_Rect(self):
        return self.top_rect

