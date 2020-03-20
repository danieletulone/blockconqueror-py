import pygame

def load(path, filename, ext):
    return pygame.image.load(path + "/" + filename + "." + ext)

def loadPng(path, filename):
    return load(path, filename, "png").convert_alpha()

def resize(image, width, height):
    return pygame.transform.smoothscale(image, (width, height))
