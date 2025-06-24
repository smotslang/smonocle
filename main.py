import pygame

# smonocle files
from render import *
from smotslang import *

class Game:
    screen = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()
    running = True

pygame.init()
game = Game()

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    game.screen.fill("purple")

    # render
    render(game)

    pygame.display.flip()

    game.clock.tick(60)

pygame.quit()