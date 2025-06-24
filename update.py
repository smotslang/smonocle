import pygame
def update(game):
    game.prgm = game.prgm.programFromSelf("tests/update.smots")
    game.prgm.interpret()
def render(game):
    pygame.draw.polygon(game.screen, pygame.Color(255, 0, 0), [(100, 100), (100, 150), (150, 150)])
    game.prgm = game.prgm.programFromSelf("tests/render.smots")
    game.prgm.interpret()