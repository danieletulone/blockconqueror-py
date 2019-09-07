# Importo i moduli necessari
import pygame
from pygame.locals import *
import random
from personaggio import Personaggio
from classes.blocco import Blocco

#inizializzo Pygame
pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# Altezza e larghezza di ogni singolo blocco che compongae lo screen
wh = 42

class Game:
    def __init__(self, name):
        self.screen = pygame.display.set_mode((1260, 546))
        pygame.mouse.set_visible(False)
        self.size = self.screen.get_size()

        # Inserisce il titolo del gioco alla finestra
        pygame.display.set_caption(name) 
        
        # Setto le due istanze della classe Personaggio                                         
        self.insalata = Personaggio("insalata", "assets/insalata/camminata/Tavola disegno ", self.size[0] - wh, self.size[1] - wh, (193, 206, 99), 90, self)
        self.bistecca = Personaggio("bistecca", "assets/bistecca/camminata/Tavola disegno ", 0, 0, (203, 42, 46), -90, self)
        
        # Tempo Attuale e Durata Totale Partita
        self.tempo_attuale = 0
        self.durata_partita = 100

        # Lista Blocchi
        self.blocchi = self.genera_mappa()

        # Cerco e coloro il primo blocco dei personaggi
        self.primo_blocco(self.insalata)
        self.primo_blocco(self.bistecca)

        # Delta Time: tempo che passa tra un esecuzione e l'altra del loop
        self.dt = 0

        # variabile per il loop
        self.loop_status = True

        # Avvio Musica
        self.avvia_musica()

        # Variabile Time utile per il bottino
        self.time_bottino = 0 

        # Rate comparsa bottino: ogni 10 secondi compare un bottino
        self.rate_bottino = 2 

        # Imposto che per il momento non c'è il bottino
        self.bottino = False

        self.random_block = False

    def primo_blocco(self, personaggio):
        # Metodo first_block, attraverso la ricerca nella lista blocchi, la funzione troverà la posizione del blocco corrispondente alla posizione del 
        # personaggio di riferimento, se la trova allora colora il quadrato iniziale del colore assegnato in self.name al personaggio 
        for blocco in self.blocchi:
            if blocco.x == personaggio.rect.left and blocco.y == personaggio.rect.top:
                blocco.status = personaggio.name
                break

    def genera_mappa(self):
        # Terrà a memoria il colore del blocco precendente per quando deve creare la mappa
        colore_del_blocco_precedente = None
        
        # Variabili Colori
        grey = 240, 240, 240
        white = 255, 255, 255
        colore = grey

        blocchi = []

        for y in range(0, 546, 42):
            if colore_del_blocco_precedente is not None:
                if colore_del_blocco_precedente == grey:
                    colore = grey
                else:
                    colore = white

            for x in range(0, 1260, 42):

                if (colore == white):
                    colore = grey
                else:
                    colore = white
            
                r = random.randint(0, 100)
                if (r > random.randint(90, 100)):
                    status = "wall"
                else:
                    status = None
                
                blocconuovo = Blocco(x, y, status, colore)
                if x == 0:
                    colore_del_blocco_precedente = blocconuovo.colore
                blocchi.append(blocconuovo)
    
        return blocchi

    def loop(self):
        while self.loop_status:
            # Setto il delta time, clock tik 60 frame al secondo = 17, 
            self.dt = clock.tick(120) / 1000

            # Incremento la variabile time usata per generate ogni tot il bottino
            self.time_bottino += self.dt
            
            # incremento il tempo attuale della partita in corso con il delta time
            self.tempo_attuale += self.dt

            if self.time_bottino > self.rate_bottino and self.bottino == False:
                 cerca_blocco = True
                 
                 while cerca_blocco:

                     r_x = random.randrange(0, 1260 - 42, 42)
                     r_y = random.randrange(0, 546 - 42, 42)

                     for blocco in self.blocchi:
                         if blocco.x == r_x and blocco.y == r_y:
                             if blocco.status == None:
                                 blocco.status = "bottino"

                                 cerca_blocco = False
                                 self.time_bottino = 0
                                 self.bottino = True
                                 break

            elif self.time_bottino > self.rate_bottino and self.bottino == True:

                for blocco in self.blocchi:
                    if blocco.status == "bottino":
                        blocco.status = None

                        self.bottino = False
                        break

            # Cerco gli eventi: pulsante esc, pulsantiere giocatori o click sulla x della finestra
            self.cerco_eventi()
            
            # Metodo per disegnare la mappa
            self.disegna_mappa()
            
            # Metodo per disegnare i personaggi e animarli
            self.disegna_e_anima_personaggi()

            # Controllo se la partita può continuare o terminare
            self.controlla_stato_partita()

            # Metodo di pygame per aggiornare l'intera superficie della finistra/schermo
            pygame.display.flip()
    
    def avvia_musica(self):
        # Carico and Eseguo la musica: -1 sta per loop infinito
        pygame.mixer.music.load('bk.mp3')
        pygame.mixer.music.play(-1)
    
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
            self.insalata.move(0, wh, self.blocchi)
        if keys[pygame.K_UP]:
            self.insalata.move(0, -wh, self.blocchi)
        if keys[pygame.K_RIGHT]:
            self.insalata.move(wh, 0, self.blocchi)
        if keys[pygame.K_LEFT]:
            self.insalata.move(-wh, 0, self.blocchi)
        
        # Pulsantiera secondo giocatore
        if keys[pygame.K_s]:
            self.bistecca.move(0, wh, self.blocchi)
        if keys[pygame.K_w]:
            self.bistecca.move(0, -wh, self.blocchi)
        if keys[pygame.K_d]:
            self.bistecca.move(wh, 0, self.blocchi)
        if keys[pygame.K_a]:
            self.bistecca.move(-wh, 0, self.blocchi)

    def disegna_mappa(self):
        global wh
        for i in self.blocchi:
            if i.status == "wall":
                pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(i.x, i.y, wh, wh))
            elif i.status == "insalata":
                pygame.draw.rect(self.screen, self.insalata.colore, pygame.Rect(i.x, i.y, wh, wh))
            elif i.status == "bistecca":
                pygame.draw.rect(self.screen, self.bistecca.colore, pygame.Rect(i.x, i.y, wh, wh))
            elif i.status == "bottino":
                pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(i.x, i.y, wh, wh))
            else:
                pygame.draw.rect(self.screen, (i.colore), pygame.Rect(i.x, i.y, wh, wh))

    def disegna_e_anima_personaggi(self):
        self.screen.blit(self.insalata.image, self.insalata.rect)    
        self.screen.blit(self.bistecca.image, self.bistecca.rect)
        self.insalata.animate(self.dt)
        self.bistecca.animate(self.dt)

game = Game("Is Not A Food War")
game.loop()