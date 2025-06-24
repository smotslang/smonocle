import pygame
def update(game):
    game.prgm = game.prgm.programFromSelf("tests/update.smots", game)
    game.prgm.interpret()
def render(game):
    game.prgm = game.prgm.programFromSelf("tests/render.smots", game)
    game.prgm.interpret()