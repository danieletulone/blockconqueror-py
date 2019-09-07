'''
                if self.name == "bistecca":
                    
                    if self.next_x != 0:
                        self.rect.left += self.next_x / 3

                    if self.next_y != 0:
                        self.rect.top += self.next_y / 3
                    
                    self.image = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load(self.filename + str(self.frame) + ".png"), (42, 42)), self.angle)
                    
                    self.time = 0

                    if self.frame == 7 or self.frame == 4:
                        if self.frame == 7:
                            self.frame = 1
                        self.animate_status = False
                        
                else:
                '''


                 '''       
    if intero_gioco > inizio_flip[flip] + 1 and intero_gioco < fine_flip[flip] + 1:
        if random_block == False:
            for i in blocchi:
                if i.status == "bottino":   
                    continue

                if i.status == "wall":
                    i.status = None

                r = random.randint(0, 100)
                if (r > 80):
                    i.status = "wall"
            random_block = True
            print("cambio muri")
        else:
            print("aspetto")
    '''
    