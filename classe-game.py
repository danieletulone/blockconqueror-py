class Game:
    def __init__(self, nome_gioco):
        # Metodo predefinito di pygame per gestire la dimensione della fienstra manualmente
        self.screen = pygame.display.set_mode((1260, 840)) 

        # Restituisce le dimensioni necessarie per il rendering
        self.size = self.screen.get_size()

        # Inserisce il titolo del gioco alla finestra
        pygame.display.set_caption(nome_gioco) 
        
        # Setto le due istanze della classe Personaggio
        self.insalata = Personaggio("insalata", "assets/insalataveloce/Tavola disegno ", self.size[0] - wh, self.size[1] - wh, (193, 206, 99), 90, self)
        self.bistecca = Personaggio("bistecca", "assets/bistecca/camminata/Tavola disegno ", 0, 0, (203, 42, 46), -90, self)

        # Tempo Attuale e Durata Totale Partita
        self.tempo_attuale = 0
        self.durata_partita = 180

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

        # Bottino a False
        self.bottino = False

        # Variabile Time utile per il bottino
        self.time_bottino = 0 

        # Rate comparsa bottino: ogni 10 secondi compare un bottino
        self.rate_bottino = 10 

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

        for y in range(0, 840, 42):
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
                if (r > random.randint(75, 100)):
                    status = "wall"
                else:
                    status = None
                
                blocconuovo = Blocco(x, y, status, colore)
                if x == 0:
                    colore_del_blocco_precedente = blocconuovo.colore
                blocchi.append(blocconuovo)
