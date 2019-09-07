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
        self.insalata = Character("insalata", "assets/insalata/camminata/Tavola disegno ", settings.screen_tuple[0] - wh, settings.screen_tuple[1] - wh, settings.colors["green"], 90)
        self.bistecca = Character("bistecca", "assets/bistecca/camminata/Tavola disegno ", 0, 0, settings.colors["red"], -90)
        self.bricks = self.load_images()
        self.time = 0
        self.durata_partita = 100
        self.blocks = self.generate_map()
        self.dt = 0
        self.loop_status = True
        self.play_music()
        self.placeholder = False
        self.placeholder_block = None
        self.placeholder_image = pygame.transform.smoothscale(pygame.image.load("assets/placeholder.png").convert_alpha(), (wh, wh))
        self.rate_placeholder = settings.clock["rate_placeholder"]
        self.time_placeholder = 0
        self.random_block = False

    def animate (self):
        self.insalata.animate(self.dt)
        self.bistecca.animate(self.dt)

    def draw (self):
        self.screen.blit(self.insalata.image, self.insalata.rect)    
        self.screen.blit(self.bistecca.image, self.bistecca.rect)

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
    
    def end_game(self):
        if self.time > self.durata_partita:
            self.loop_status = False
            print("Score insalata: " + str(self.insalata.score))
            print("Score bistecca: " + str(self.bistecca.score))

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
    
    def load_images (self):
        wh = settings.blocks["wh"]
        
        bricks = {
            "wall": pygame.transform.smoothscale(pygame.image.load("assets/bricks/mansory.png").convert_alpha(), (wh + 10, wh + 10)),
            "lightning": pygame.transform.smoothscale(pygame.image.load("assets/weapons/lightning.png").convert_alpha(), (wh, wh)),
            "fist": pygame.transform.smoothscale(pygame.image.load("assets/weapons/fist.png").convert_alpha(), (wh, wh)),
        }

        return bricks

    def loop(self):
        while self.loop_status:
            self.dt = clock.tick(settings.clock["frame"]) / 1000
            self.time_placeholder += self.dt
            self.time += self.dt

            if self.time_placeholder > self.rate_placeholder and self.placeholder == False:
                seekEmptyBlock = True
                 
                while seekEmptyBlock:

                    random_index = random.randint(0, len(self.blocks))
                    random_block = self.blocks[random_index]

                    if random_block.status == None:
                        random_block.status = "placeholder"
                        self.placeholder_block = random_block.status
                        self.time_placeholder = 0
                        self.placeholder = True
                        seekEmptyBlock = False

            elif self.time_placeholder > self.rate_placeholder and self.placeholder == True:

                for block in self.blocks:
                    if block.status == "placeholder":
                        block.status = None

                        self.placeholder = False
                        break
    
            self.on_events()
            self.draw_map()
            self.draw()
            self.animate()
            self.end_game()
            pygame.display.flip()

    def on_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop_status = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.loop_status = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.insalata.move(0, wh, self.blocks, self)
        if keys[pygame.K_UP]:
            self.insalata.move(0, -wh, self.blocks, self)
        if keys[pygame.K_RIGHT]:
            self.insalata.move(wh, 0, self.blocks, self)
        if keys[pygame.K_LEFT]:
            self.insalata.move(-wh, 0, self.blocks, self)
        
        if keys[pygame.K_s]:
            self.bistecca.move(0, wh, self.blocks, self)
        if keys[pygame.K_w]:
            self.bistecca.move(0, -wh, self.blocks, self)
        if keys[pygame.K_d]:
            self.bistecca.move(wh, 0, self.blocks, self)
        if keys[pygame.K_a]:
            self.bistecca.move(-wh, 0, self.blocks, self)

    def play_music(self):
        pygame.mixer.music.load('assets/bk.mp3')
        pygame.mixer.music.play(-1)

game = Game(settings.game_info["name"])
game.loop()