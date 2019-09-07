import pygame

class Settings:
    def __init__(self):
        self.blocks = {
            "wh": 40,
            "wall_probability": 15
        }

        self.colors = {
            "grey": (240, 240, 240),
            "white": (255, 255, 255),
            "red": (203, 42, 46),
            "green": (193, 206, 99)
        }

        self.clock = {
            "frame": 60,
            "rate_placeholder": 10
        }

        self.game_info = {
            "name": "BlockConqueror Py",
            "author": "Daniele Tulone",
            "graphic_design": "Mattia Guerriero"
        }

        self.grid = {
            "colors": (self.colors["grey"], self.colors["white"])
        }

        self.layout = {
            "header": 100,
            "body": 0
        }

        self.keys = [
            {
                "down": pygame.K_DOWN, 
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT,
                "up": pygame.K_UP,
            },
            {
                "down": pygame.K_s, 
                "left": pygame.K_a,
                "right": pygame.K_d,
                "up": pygame.K_w,
            },
        ]

        self.screen = {
            "width": 1260,
            "height": 546,
            "frame": 60
        }

        self.screen_tuple = (1260, 546)

    def setSize (self, size):
        self.screen_tuple = size
        self.screen["width"] = size[0]
        self.screen["height"] = size[1]
        self.calculateWh()

    def calculateWh (self):
        for i in range(40, 60):
            if self.screen["width"] % i == 0:
                self.blocks["wh"] = i 
                break

        self.layout["header"] = self.layout["header"] + (self.screen["height"] - self.layout["header"]) % self.blocks["wh"]
        self.layout["body"] = self.screen["height"] - self.layout["header"]
        self.layout["numbers_on_height"] = int(self.layout["body"] / self.blocks["wh"])
        
        print(self.layout)