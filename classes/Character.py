import pygame
import random
from settings import Settings

settings = Settings()

class Character(pygame.sprite.Sprite):
    def __init__ (self, name, filename, block, block_index, color, initial_angle, on_width):
        pygame.sprite.Sprite.__init__ (self) 
        wh = settings.blocks["wh"]
        self.angle = initial_angle
        self.animate_status = False
        self.blocks = [block_index]
        self.current_block = block_index
        self.color = color
        self.filename = filename
        self.frame = 0
        self.images = self.load_images(7, wh) 
        self.image = pygame.transform.rotate(self.images[self.frame], self.angle)
        self.name = name
        self.next_x = 0
        self.next_y = 0
        self.rate = 0.05
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = block.x, block.y
        self.score = 0 
        self.time = 0
        self.on_width = on_width
   
    def move(self, block_index, blocks, game):
        if self.animate_status is False:
            if block_index >= 0 and block_index < len(blocks):
                if (blocks[block_index].y != blocks[self.current_block].y and blocks[block_index].x != blocks[self.current_block].x):
                    return

                block = blocks[block_index]
                if block.status != "wall":
                    game.to_render.append(self.current_block)
                    self.set_angle(block_index)
                    self.current_block = block_index
                    self.blocks.append(block_index)
                    self.animate_status = True
                    
                    if block.x > self.rect.left:
                        self.next_x = 40
                    elif block.x < self.rect.left:
                        self.next_x = -40
                    else:
                        self.next_x = 0

                    if block.y > self.rect.top:
                        self.next_y = 40
                    elif block.y < self.rect.top:
                        self.next_y = -40
                    else:
                        self.next_y = 0

                    if block.status != self.name and block.status != None and block.status != "wall":
                        if block.status == "placeholder":
                            self.score += len(self.blocks) * 3 + game.time
                            game.placeholder = False

                        for bl in self.blocks:
                            blocks[bl].status = None
                            game.to_render.append(bl)
                
                    block.status = self.name

                    for bl in self.blocks:
                        game.to_render.append(bl)
                    
                    game.to_render.append(self.current_block)

    def animate(self, dt = 0, game = None):

        if self.animate_status == True:
            self.time += dt 

            if self.time > self.rate:
                self.frame += 1
                
                if self.next_x != 0:
                    self.rect.left += self.next_x / 2
                if self.next_y != 0:
                    self.rect.top += self.next_y / 2
                
                self.image = pygame.transform.rotate(self.images[self.frame], self.angle)
                self.time = 0

                if self.frame == 2 or self.frame == 4 or self.frame == 6:
                    self.animate_status = False

                    if self.frame == 6:
                        self.frame = 0
        else:
            self.image = pygame.transform.rotate(self.images[self.frame], self.angle)
        
        game.to_render.append(self.current_block) 

    def load_images (self, n, wh):
        images = []

        for i in range(1, 8, 1):
            image = pygame.image.load(self.filename + str(i) + ".png").convert_alpha()
            image = pygame.transform.smoothscale(image, (wh, wh))
            images.append(image)

        return images
    
    def set_angle(self, block_index):
        if block_index == self.current_block + 1:
            self.angle = 0
        elif block_index == self.current_block - 1:
            self.angle = 180
        elif block_index == self.current_block + self.on_width:
            self.angle = -90
        elif block_index == self.current_block - self.on_width:
            self.angle = 90

    def setKeys (self, keys):
        pass
    
