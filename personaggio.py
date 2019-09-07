import pygame
import random

class Personaggio(pygame.sprite.Sprite):
    def __init__ (self, name, filename, x, y, colore, initial_angle, game):
        #semplice classe base di Pygame per oggetti di gioco visibile  
        pygame.sprite.Sprite. __init__ (self) 
        
        #l'attributo frame self.frame viene assegnato al valore 1
        self.frame = 1

        #l'attributo self.angle viene assegnato al valore literal initial_angle inserito nei parametri di classe
        #in attesa di un valore numerico di posizione, partendo dalal posizione di riferimento in cui sono stati disegnati i frame, quindi
        #per mostrare i piedi dell'insalata verso l'alto bisognerà posizionarla a -90°
        self.angle = initial_angle 
        
        #l'attributo self.filename viene assegnato al valore literal filename inserito nei parametri della classe per ricevere un valore 
        #literal in ingresso, ovvero il percorso che il computer eseguirà per recuperare i frame dell'animazione.
        self.filename = filename
        
        #All'attrinbuto self.image viene assegnato dal modulo transform: modulo che opera nel contesto superficie attraverso operazioni che 
        #spostano o ridimensionano i pixel, le funzioni all'interno di questo modulo ad esempio rotate hanno bisogno di una superficie per modificare
        #e restituire una nuova superficie con nuovi risultati.Inseriamo il metodo smothscale per scalare il vettoriale senza dispersione di dati, in questo modo
        #le immagini saranno ben evidenti, attraverso Pygame, attraverso l'attributo load avviene il caricamento, allinterno delle parentesi troviamo self.filename
        #ovvero il percorso, str perchè converte in stringa  il titolo del frame 1 + il suo formato, larghezza ed altezza e l'angolo.
        self.image = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load(self.filename + str(self.frame) + ".png"), (42, 42)), self.angle)
        
        #attributo self.rect assegnato a self.image.get_rect(), la funzione get_rect() restituisce un rettagolo della stessa larghezza e altezza dell'img/
        #caricata.
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y 
        self.colore = colore
        
        
        self.time = 0
        
        self.rate = 0.0
        
        self.animate_status = False
        
        self.next_x = 0
        
        self.next_y = 0
        
        self.name = name
        
        
        self.score = 0 

        self.game = game
   
    def move(self, x, y, blocchi):
        if self.animate_status is False: #se animate status is false il metodo può essere eseguito
            for blocco in blocchi: 
                if blocco.x == self.rect.left + x and blocco.y == self.rect.top + y: #la posizione del blocco nell'asse delle x
                    #è uguale alla posizione del personaggio + il blocco in cui si sposterà stessa cosa per y, se  è diverso dall
                    if blocco.status != "wall":
                        self.scegli_angolo(x, y)
                        self.animate_status = True
                        self.next_x = x
                        self.next_y = y

                        #se blocco diverso da self name da none e dal muro sarà la scia del giocatore avversario o il bottino
                        if blocco.status != self.name and blocco.status != None and blocco.status != "wall":
                            
                            #lista nella quale vanno i blocchi eliminati a causa della presa del bottino o dal passaggio sopra la scia dell'avversario 
                            blocchi_da_eliminare = []
                            for bl in blocchi:
                                if bl.status == self.name:
                                    blocchi_da_eliminare.append(bl)

                            if blocco.status == "bottino":
                                self.score += len(blocchi_da_eliminare) * 3 + self.game.tempo_attuale
                                self.game.bottino = False
                                
                        
                            for bl in blocchi_da_eliminare:
                                bl.status = None
                            
                            blocco.status = self.name
                        
                            
                            
                        else:
                            blocco.status = self.name

                    
    def scegli_angolo(self, x, y):
        if x > 0:
            self.angle = 0
        elif x < 0:
            self.angle = 180
        elif y > 0:
            self.angle = -90
        elif y < 0:
            self.angle = 90

    def animate(self, dt):
        if self.animate_status == True: #self.animate_status è settata a False poi nella funzione move viene messa a True, l'animazione parte
            #incremento di 16/17 il self.time
            self.time += dt 

            if self.time > self.rate:
                self.frame += 1
                
                if self.next_x != 0:
                    self.rect.left += self.next_x / 2 # - 42 o + 42, direzione x , verso la quale vado, next_x viene diviso, compierà 21 pixel e un cambio immagine

                if self.next_y != 0:
                    self.rect.top += self.next_y / 2
                
                self.image = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load(self.filename + str(self.frame) + ".png"), (42, 42)), self.angle) #carico immagine
                self.time = 0 #resetto il tempo 

                if self.frame == 3 or self.frame == 5 or self.frame == 7:
                    
                    if self.frame == 7:
                        self.frame = 1
                    self.animate_status = False
        else:
            self.image = pygame.transform.rotate(pygame.transform.smoothscale(pygame.image.load(self.filename + str(self.frame) + ".png"), (42, 42)), self.angle)     

        
 
    
        
        


    

    