import pygame


class bird ():
    def __init__(self, pos):
        self.pos = pos
        self.dir = 0
        self.colour = (255, 255, 0)
        self.size = 20

    def jump(self, keys):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if keys[pygame.K_SPACE] and self.dir > -5:
            self.dir = -9

        self.pos = self.pos + self.dir
        self.dir = self.dir + 1

    def draw(self, win):
        pygame.draw.circle(win, self.colour, (100, self.pos), self.size)


class pipe():
    def __init__(self, height, pos):
        self.height = height
        self.pos = pos

    def move(self):
        t = self.pos[0]
        g = self.pos[1]
        t = t - 10
        self.pos = (t, g)

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), ((self.pos), (200, self.height)))
