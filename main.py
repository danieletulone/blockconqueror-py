import random
import pygame
from pygame.locals import *
from classes.Character import Character
from classes.Block import Block
import settings

pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

wh = settings.blocks["wh"]

class Game:
    def __init__(self, name):
        pygame.mouse.set_visible(False)
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(settings.screen_tuple)
                           
        self.insalata = Character("insalata", "assets/insalata/camminata/Tavola disegno ", settings.screen_tuple[0] - wh, settings.screen_tuple[1] - wh, settings.colors["green"], 90, self)
        self.bistecca = Character("bistecca", "assets/bistecca/camminata/Tavola disegno ", 0, 0, settings.colors["red"], -90, self)
        self.bricks = self.load_bricks()
    
        self.tempo_attuale = 0
        self.durata_partita = 100
        self.blocks = self.generate_map()
        self.first_block(self.insalata)
        self.first_block(self.bistecca)
        self.dt = 0
        self.loop_status = True
        self.play_music()
        self.placeholder = False
        self.placeholder_image = pygame.transform.smoothscale(pygame.image.load("assets/placeholder.png").convert_alpha(), (wh, wh))
        self.rate_placeholder = settings.clock["rate_placeholder"]
        self.time_placeholder = 0
        self.random_block = False

    def first_block(self, character):
        for block in self.blocks:
            if block.x == character.rect.left and block.y == character.rect.top:
                block.status = character.name
                break

    def generate_map(self):
        color_prec_block = None
        
        grey, white = settings.grid["colors"]
        color = grey

        blocks = []

        for y in range(0, settings.screen["height"], wh):
            if color_prec_block is not None:
                if color_prec_block == grey:
                    color = grey
                else:
                    color = white

            for x in range(0, settings.screen["width"], wh):

                if (color == white):
                    color = grey
                else:
                    color = white
            
                r = random.randint(0, 100)
                if (r > random.randint(100 - settings.blocks["wall_probability"], 100)):
                    status = "wall"
                else:
                    status = None
                
                new_block = Block(x, y, status, color)
                if x == 0:
                    color_prec_block = new_block.color
                blocks.append(new_block)
    
        return blocks

    def loop(self):
        while self.loop_status:
            # Setto il delta time, clock tik 60 frame al secondo = 17, 
            self.dt = clock.tick(settings.clock["frame"]) / 1000

            # Incremento la variabile time usata per generate ogni tot il placeholder
            self.time_placeholder += self.dt
            
            # incremento il tempo attuale della partita in corso con il delta time
            self.tempo_attuale += self.dt

            if self.time_placeholder > self.rate_placeholder and self.placeholder == False:
                 cerca_blocco = True
                 
                 while cerca_blocco:

                    r_x = random.randrange(0, settings.screen["width"] - wh, wh)
                    r_y = random.randrange(0, settings.screen["height"] - wh, wh)

                    for block in self.blocks:
                        if block.x == r_x and block.y == r_y:
                            if block.status == None:
                                block.status = "placeholder"

                                cerca_blocco = False
                                self.time_placeholder = 0
                                self.placeholder = True
                                break

            elif self.time_placeholder > self.rate_placeholder and self.placeholder == True:

                for block in self.blocks:
                    if block.status == "placeholder":
                        block.status = None

                        self.placeholder = False
                        break
    
            self.cerco_eventi()
        
            self.draw_map()
            
            self.draw_and_animate()

            self.controlla_stato_partita()

            pygame.display.flip()
    
    
    def controlla_stato_partita(self):
        if self.tempo_attuale > self.durata_partita:
            self.loop_status = False
            print("Score insalata: " + str(self.insalata.score))
            print("Score bistecca: " + str(self.bistecca.score))

    def cerco_eventi(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_status = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.loop_status = False

        # In keys salvo una lista di tutti i pulsanti attualmente premuti
        keys = pygame.key.get_pressed()

        # Pulsantiera primo giocatore
        if keys[pygame.K_DOWN]:
            self.insalata.move(0, wh, self.blocks)
        if keys[pygame.K_UP]:
            self.insalata.move(0, -wh, self.blocks)
        if keys[pygame.K_RIGHT]:
            self.insalata.move(wh, 0, self.blocks)
        if keys[pygame.K_LEFT]:
            self.insalata.move(-wh, 0, self.blocks)
        
        # Pulsantiera secondo giocatore
        if keys[pygame.K_s]:
            self.bistecca.move(0, wh, self.blocks)
        if keys[pygame.K_w]:
            self.bistecca.move(0, -wh, self.blocks)
        if keys[pygame.K_d]:
            self.bistecca.move(wh, 0, self.blocks)
        if keys[pygame.K_a]:
            self.bistecca.move(-wh, 0, self.blocks)

    def draw_map(self):
        wh = settings.blocks["wh"]

        for i in self.blocks:
            if i.status == "wall":
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                self.screen.blit(self.bricks["wall"], pygame.Rect(i.x, i.y, wh, wh))
            elif i.status == "insalata":
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                pygame.draw.rect(self.screen, self.insalata.color, pygame.Rect(i.x + 16, i.y + 16, wh - 32, wh - 32))
            elif i.status == "bistecca":
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                pygame.draw.rect(self.screen, self.bistecca.color, pygame.Rect(i.x + 16, i.y + 16, wh - 32, wh - 32))
            elif i.status == "placeholder":
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                self.screen.blit(self.placeholder_image, pygame.Rect(i.x, i.y, wh, wh))
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                
                

    def draw_and_animate(self):
        self.screen.blit(self.insalata.image, self.insalata.rect)    
        self.screen.blit(self.bistecca.image, self.bistecca.rect)
        self.insalata.animate(self.dt)
        self.bistecca.animate(self.dt)

    def load_bricks (self):
        wh = settings.blocks["wh"]
        
        bricks = {
            "wall": pygame.transform.smoothscale(pygame.image.load("assets/bricks/mansory.png").convert_alpha(), (wh + 10, wh + 10)),
            "wall-bordered": pygame.transform.smoothscale(pygame.image.load("assets/bricks/brick-bordered.png").convert_alpha(), (wh, wh)),
        }
    
        return bricks

    def play_music(self):
        pygame.mixer.music.load('assets/bk.mp3')
        pygame.mixer.music.play(-1)

game = Game(settings.game_info["name"])
game.loop()