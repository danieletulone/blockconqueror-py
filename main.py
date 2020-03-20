import random
import pygame
from pygame.locals import *
from classes.Character import Character
from classes.Block import Block
from settings import Settings 
from helpers.image import loadPng, resize

settings = Settings()
pygame.init()
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.display.set_caption(settings.game_info["name"])
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        settings.setSize(self.screen.get_size())      
        pygame.mouse.set_visible(False)
        self.bricks = self.load_images()
        self.time = 0
        self.blocks = self.generate_map()
        self.characters = self.setCharacters()
        self.dt = 0
        self.loop_status = True
        self.play_music()
        self.placeholder = False
        self.placeholder_block = None
        self.placeholder_image = resize(loadPng("assets", "placeholder"), settings.blocks["wh"], settings.blocks["wh"])
        self.rate_placeholder = settings.clock["rate_placeholder"]
        self.time_placeholder = 0
        self.random_block = False
        self.to_render = []
        self.loop()

    def animate (self):
        for c in self.characters:
            c.animate(self.dt, self)

    def draw (self):
        for c in self.characters:
            pygame.draw.rect(self.screen, (255, 255, 255), c.rect)
            self.screen.blit(c.image, c.rect)    

    def draw_map(self):
        wh = settings.blocks["wh"]

        for i in self.blocks:
            if i.status == "wall":
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                self.screen.blit(self.bricks["wall"], pygame.Rect(i.x, i.y, wh, wh))
            elif i.status == "insalata":
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                pygame.draw.rect(self.screen, self.characters[1].color, pygame.Rect(i.x + 16, i.y + 16, wh - 32, wh - 32))
            elif i.status == "bistecca":
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                pygame.draw.rect(self.screen, self.characters[0].color, pygame.Rect(i.x + 16, i.y + 16, wh - 32, wh - 32))
            elif i.status == "placeholder":
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                self.screen.blit(self.placeholder_image, pygame.Rect(i.x, i.y, wh, wh))
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
    
    def end_game(self):
        if self.time > settings.clock["game_duration"]:
            self.loop_status = False

    def generate_map(self):
        color_prec_block = None
        
        grey, white = settings.grid["colors"]
        color = grey

        blocks = []

        for y in range(0, settings.layout["numbers_on_height"]):
            for x in range(0, settings.screen["width"], settings.blocks["wh"]):
                r = random.randint(0, 100)

                if (r > random.randint(100 - settings.blocks["wall_probability"], 100)):
                    status = "wall"
                else:
                    status = None

                new_block = Block(x, y * settings.blocks["wh"] + settings.layout["header"], status)

                blocks.append(new_block)
    
        return blocks
    
    def load_images (self):
        wh = settings.blocks["wh"]
        
        bricks = {
            "wall": resize(loadPng("assets/bricks", "mansory"), wh + 10, wh + 10),
            "lightning": resize(loadPng("assets/weapons", "lightning"), wh, wh),
            "fist": resize(loadPng("assets/weapons", "fist"), wh, wh),
        }

        return bricks

    def loop(self):
        self.draw_map()

        while self.loop_status:
            self.to_render = []
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
                        self.placeholder_block = random_index
                        self.time_placeholder = 0
                        self.placeholder = True
                        seekEmptyBlock = False
                        self.to_render.append(self.placeholder_block)

            elif self.time_placeholder > self.rate_placeholder and self.placeholder == True:

                for block in self.blocks:
                    if block.status == "placeholder":
                        block.status = None

                        self.placeholder = False
                        break
    
            self.on_events()
            wh = settings.blocks["wh"]
            
            self.animate()

            for i in self.to_render:
                w = i
                i = self.blocks[i]
                if i.status == "wall":
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                    self.screen.blit(self.bricks["wall"], pygame.Rect(i.x, i.y, wh, wh))
                elif i.status == "insalata":
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                    pygame.draw.rect(self.screen, self.characters[1].color, pygame.Rect(i.x + 16, i.y + 16, wh - 32, wh - 32))
                elif i.status == "bistecca":
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                    pygame.draw.rect(self.screen, self.characters[0].color, pygame.Rect(i.x + 16, i.y + 16, wh - 32, wh - 32))
                elif i.status == "placeholder":
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
                    self.screen.blit(self.placeholder_image, pygame.Rect(i.x, i.y, wh, wh))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(i.x, i.y, wh, wh))
            self.draw()
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
        
        for i in range(2):
            if keys[settings.keys[i]["down"]]:
                self.characters[i].move(self.characters[i].current_block + settings.layout["numbers_on_width"], self.blocks, self)
            if keys[settings.keys[i]["up"]]:
                self.characters[i].move(self.characters[i].current_block - settings.layout["numbers_on_width"], self.blocks, self)
            if keys[settings.keys[i]["right"]]:
                self.characters[i].move(self.characters[i].current_block + 1, self.blocks, self)
            if keys[settings.keys[i]["left"]]:
                self.characters[i].move(self.characters[i].current_block - 1, self.blocks, self)

    def play_music(self):
        pygame.mixer.music.load('assets/bk.mp3')
        pygame.mixer.music.play(-1)

    def setCharacters(self):
        bistecca = Character("bistecca", self.blocks[0], 0, settings.colors["red"], -90, settings.layout["numbers_on_width"])
        insalata = Character("insalata", self.blocks[len(self.blocks) - 1], len(self.blocks) - 1, settings.colors["green"], 90, settings.layout["numbers_on_width"])
        return [bistecca, insalata]

game = Game()