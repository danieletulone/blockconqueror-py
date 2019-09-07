import pygame
import random
import settings
wh = settings.blocks["wh"]

class Character(pygame.sprite.Sprite):
    def __init__ (self, name, filename, x, y, color, initial_angle, game):
        pygame.sprite.Sprite. __init__ (self) 
        self.angle = initial_angle
        self.animate_status = False
        self.color = color
        self.filename = filename
        self.frame = 0
        self.game = game
        self.images = self.load_images(7) 
        self.image = pygame.transform.rotate(self.images[self.frame], self.angle)
        self.name = name
        self.next_x = 0
        self.next_y = 0
        self.rate = 0.05
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = x, y
        self.score = 0 
        self.time = 0
   
    def move(self, x, y, blocks):
        if self.animate_status is False:
            for block in blocks: 
                if block.x == self.rect.left + x and block.y == self.rect.top + y:
                    if block.status != "wall":
                        self.set_angle(x, y)
                        self.animate_status = True
                        self.next_x = x
                        self.next_y = y

                        if block.status != self.name and block.status != None and block.status != "wall":
                            
                            blocks_da_eliminare = []
                            for bl in blocks:
                                if bl.status == self.name:
                                    blocks_da_eliminare.append(bl)

                            if block.status == "placeholder":
                                self.score += len(blocks_da_eliminare) * 3 + self.game.tempo_attuale
                                self.game.placeholder = False
                                
                        
                            for bl in blocks_da_eliminare:
                                bl.status = None
                            
                            block.status = self.name
                    
                        else:
                            block.status = self.name

    def animate(self, dt):
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

    def load_images (self, n):
        images = []

        for i in range(1, 8, 1):
            image = pygame.image.load(self.filename + str(i) + ".png").convert_alpha()
            image = pygame.transform.smoothscale(image, (wh, wh))
            images.append(image)

        return images
    
    def set_angle(self, x, y):
        if x > 0:
            self.angle = 0
        elif x < 0:
            self.angle = 180
        elif y > 0:
            self.angle = -90
        elif y < 0:
            self.angle = 90
        
        


    

    