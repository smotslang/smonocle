import pygame

def render(game):
    pygame.draw.polygon(game.screen, pygame.Color(255, 0, 0), [(100, 100), (100, 150), (150, 150)])