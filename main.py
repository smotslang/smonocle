import pygame

# smonocle files
from update import *
from smotslang import *

class Game:
    screen = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()
    running = True

    def __init__(self):
        self.prgm = Program("tests/init.smots", self)
        self.prgm.interpret()

pygame.init()
game = Game()

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    # update
    update(game)

    game.screen.fill(pygame.Color(138, 204, 237))

    # render
    render(game)

    pygame.display.flip()

    game.clock.tick(60)

game.prgm = game.prgm.programFromSelf("tests/exit.smots", game)
game.prgm.interpret()
pygame.quit()