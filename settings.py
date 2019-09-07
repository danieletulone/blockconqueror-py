import pygame

blocks = {
    "wh": 42,
    "wall_probability": 15
}

colors = {
    "grey": (240, 240, 240),
    "white": (255, 255, 255),
    "red": (203, 42, 46),
    "green": (193, 206, 99)
}

clock = {
    "frame": 60,
    "rate_placeholder": 10
}

game_info = {
    "name": "BlockConqueror Py",
    "author": "Daniele Tulone",
    "graphic_design": "Mattia Guerriero"
}

grid = {
    "colors": (colors["grey"], colors["white"])
}

keys = [
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

screen = {
    "width": 1260,
    "height": 546,
    "frame": 60
}

screen_tuple = (1260, 546)