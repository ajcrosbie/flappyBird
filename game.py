import pygame
import objects


def redrawWindow(win, bird):
    win.fill((100, 100, 255))
    bird.draw(win)
    pygame.display.update()


def createObsticle(pipes):
    pass


def main():
    width = 1000
    height = 500
    win = pygame.display.set_mode((width, height))
    bird = objects.bird(100)
    pipes = []
    clock = pygame.time.Clock()
    while True:
        pygame.time.delay(60)
        clock.tick(10)
        keys = pygame.key.get_pressed()
        bird.jump(keys)
        redrawWindow(win, bird)


if __name__ == '__main__':
    main()
