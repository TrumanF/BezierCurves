import random

import pygame
import bezier
import numpy as np

pygame.init()

SIZE = WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode(SIZE)
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BABY_BLUE = (173, 216, 230)


class Circle:
    def __init__(self, x, y, radius):
        self.pos = (x, y)
        self.x_boundary = (x - radius, x + radius)
        self.y_boundary = (y - radius, y + radius)
        self.radius = radius

    def draw(self):
        pygame.draw.circle(WIN, BLACK, to_cartesian(self.pos), self.radius, 0)

    def recalc_boundary(self):
        self.x_boundary = (self.pos[0] - self.radius, self.pos[0] + self.radius)
        self.y_boundary = (self.pos[1] - self.radius, self.pos[1] + self.radius)

    def update(self):
        # for updates
        pass


def to_cartesian(coord):
    x, y = coord
    return x, HEIGHT - y


def to_int(coord):
    return int(coord[0]), int(coord[1])


def within(x, low, high):
    return low <= x <= high


def main():
    run = True
    clock = pygame.time.Clock()
    c_points = [Circle(random.randint(10, 240), random.randint(10, 240), 5) for _ in range(4)]
    selected = False
    active_c_point = None
    while run:
        points = bezier.generate_points(np.array([x.pos for x in c_points]), 1000)
        all_p = bezier.draw_line_percent(.5, np.array([x.pos for x in c_points]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left mouse button
                if event.button == 1:
                    pos = to_cartesian(pygame.mouse.get_pos())
                    for c_point in c_points:
                        c_point.draw()
                        if within(pos[0], *c_point.x_boundary) and within(pos[1], *c_point.y_boundary):
                            selected = True
                            active_c_point = c_point
            elif event.type == pygame.MOUSEBUTTONUP:
                # User released mouse buttons
                selected = False
        if selected:
            # Move to mouse position when selected,
            # the circle 'follows' the mouse
            active_c_point.pos = to_cartesian(pygame.mouse.get_pos())
            active_c_point.recalc_boundary()

        clock.tick(FPS)
        WIN.fill(WHITE)

        for c_point in c_points:
            c_point.draw()

        for point in points:
            WIN.set_at(to_int(to_cartesian(point)), BLACK)
        for i in range(len(c_points) - 1):
            for pair in [all_p[i][a:a + 2] for a in range(len(all_p[i]) - 1)]:
                pygame.draw.line(WIN, BABY_BLUE, to_int(to_cartesian(pair[0])), to_int(to_cartesian(pair[1])))

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
