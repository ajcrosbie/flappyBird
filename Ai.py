import pygame
import pickle
import numpy as np
import matplotlib.pyplot as plt
import time
import objects
import random


def Learning():
    size = 500 // 5
    HmEpisodes = 100
    epsilon = 0.4
    EPSDecay = 0.999
    showEvery = 100
    startQtable = 'qtableF-1606307731.pickle'  # or file name/ None
    learnRate = 0.1
    discount = 0.95
    qTable = qTables(startQtable, size)
    episodeRewards = []
    for episode in range(HmEpisodes):
        clock = pygame.time.Clock()
        reward = 0
        width = 1000
        height = 500
        pipes = []
        player = objects.bird(250)
        createObsticle(pipes, height, width, True)
        win = pygame.display.set_mode((width, height))
        if episode % showEvery == 0:
            print(f"on # {episode}, epsilon: {epsilon}")
            print(
                f"{showEvery} ep mean {np.mean(episodeRewards[-showEvery:])}")
            show = True
        else:
            show = False
        episodeReward = 0
        for i in range(1500):  # steps taken can be changed later
            obs = ((height-player.pos)//5,
                   (pipes[0].height - player.pos)//5, player.dir)
            if np.random.random() > epsilon:
                action = np.argmax(qTable[obs])
            else:
                action = np.random.randint(0, 2)
            player.jump(action)
            for i in pipes:
                i.move()
            createObsticle(pipes, height, width)
            point = 0
            pipes, t = removePipe(pipes)
            if collisions(player, pipes, show):
                reward -= 200
                point = -200
            elif not sides(player, height):
                reward -= 200
                point = -200
            else:
                reward = 10

            newObs = ((height-player.pos)//5,
                      (pipes[0].height - player.pos)//5, player.dir)
            maxFurureQ = np.max(qTable[newObs])
            currentQ = qTable[obs][action]

            if reward == -200:
                newQ = -200
            else:
                newQ = (1 - learnRate) * currentQ + learnRate * \
                    (reward+discount * maxFurureQ)
            qTable[obs][action] = newQ
            if show:
                pygame.time.delay(20)
                clock.tick(30)
                redrawWindow(win, player, pipes)
            episodeReward += reward
            if point == -200:
                break
        episodeRewards.append(episodeReward)
        epsilon *= EPSDecay
    pygame.display.quit()
    movingAvg = np.convolve(episodeRewards, np.ones(
        (showEvery,)) / showEvery, mode='valid')
    with open(f"qtableF-{int(time.time())}.pickle", "wb") as f:
        pickle.dump(qTable, f)
    plt.plot([i for i in range(len(movingAvg))], movingAvg)
    plt.ylabel(f"reward {showEvery}")
    plt.xlabel(f"episode #")
    plt.show()


def qTables(startQtable, size):
    if startQtable is None:
        qTable = {}
        for walls in range((-size+1), size):
            for pipeDif in range((-size+1), size):
                for c in range(-30, 30):
                    qTable[(walls, pipeDif, c)] = [np.random.uniform(-5, 0)
                                                   for i in range(2)]
    else:
        with open(startQtable, 'rb') as f:
            qTable = pickle.load(f)
    return qTable


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


def collisions(bird, pipes, show=-False):
    v = False
    for i in pipes:
        if i.pos[0] < 100 and i.pos[0] > -100:
            for b in range(i.height):
                for s in range(10):
                    s = s*20
                    if bird.pos + bird.size == i.pos[1] + b:
                        if 100 == i.pos[0] + s:
                            t = reset(bird)
                            v = True
                    elif bird.pos - bird.size == i.pos[1] + b:
                        if 100 == i.pos[0] + s:
                            t = reset(bird)
                            v = True

    return v


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
    t = False
    for i in pipes:
        if i.pos[0] == 0:
            c.remove(i)
            t = True
    return c, t


def main():
    width = 1000
    height = 500
    win = pygame.display.set_mode((width, height))
    bird = objects.bird(100)
    pipes = []
    createObsticle(pipes, height, width, True)
    clock = pygame.time.Clock()
    while True:
        pygame.time.delay(20)
        clock.tick(30)
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
    Learning()
