import pygame
import objects
import random


def sides(bird, height):
    if bird.pos - bird.size < 0:
        f = reset(bird)
    elif bird.pos + bird.size > height:
        f = reset(bird)
    else:
        f = True
    return f


def redrawWindow(win, bird, pipes):
    win.fill((100, 100, 255))
    bird.draw(win)
    for i in pipes:
        i.draw(win)
    pygame.display.update()


def collisions(bird, pipes):
    for i in pipes:
        if i.pos[0] < 100 and i.pos[0] > -100:
            for b in range(i.height):
                for v in range(50):
                    s = v*4
                    if bird.pos + bird.size == i.pos[1] + b:
                        if 100 == i.pos[0] + s:
                            t = reset(bird)
                            return t
                    elif bird.pos - bird.size == i.pos[1] + b:
                        if 100 == i.pos[0] + s:
                            t = reset(bird)
                            return t
    return True


def reset(bird):
    bird.pos = 100
    bird.dir = 0
    return False


def createObsticle(pipes, height, width, v=False):
    if v:
        Pheight = random.randrange(height - 150)
        pos = (width, -10)
        pipes.append(objects.pipe(Pheight, pos))

        NPheight = (height + 150) + Pheight
        Npos = (width, Pheight + 150)
        pipes.append(objects.pipe(NPheight, (Npos)))

    elif pipes[-1].pos[0] == 250:
        Pheight = random.randrange(height - 120)
        pos = (width, -10)
        pipes.append(objects.pipe(Pheight, pos))

        NPheight = height + 120 + Pheight
        Npos = (width, Pheight + 120)
        pipes.append(objects.pipe(NPheight, (Npos)))


def removePipe(pipes):
    c = pipes.copy()
    for i in pipes:
        if i.pos[0] == -190:
            c.remove(i)
    return c


def main():
    width = 1000
    height = 500
    win = pygame.display.set_mode((width, height))
    bird = objects.bird(100)
    pipes = []
    createObsticle(pipes, height, width, True)
    clock = pygame.time.Clock()
    while True:
        pygame.time.delay(30)
        clock.tick(20)
        keys = pygame.key.get_pressed()
        bird.jump(keys)
        for i in pipes:
            i.move()
        createObsticle(pipes, height, width)
        pipes = removePipe(pipes)
        h = collisions(bird, pipes)
        g = sides(bird, height)
        if h and g:
            pass
        else:
            pipes = []
            createObsticle(pipes, height, width, True)
        redrawWindow(win, bird, pipes)


if __name__ == '__main__':
    main()
