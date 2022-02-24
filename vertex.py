import pygame
import math

# Constants
W = 800
H = 600
SCREEN = pygame.display.set_mode((W, H))

SQUARE_SIZE = 20
INFINITY = math.inf

BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (178, 190, 181)
GREEN = (121, 254, 12)


class Vertex:
    def __init__(self, x, y, current=False, distance=INFINITY, visited=False, previous=None,
                 path=None, wall=False, colour=PURPLE, shape="circle", size=4) -> None:
        self.x = x
        self.y = y
        self.current = current
        self.distance = distance
        self.visited = visited
        self.previous = previous
        self.path = path
        self.wall = wall
        self.colour = colour
        self.shape = shape
        self.size = size

    def return_coordinates(self):
        return self.x, self.y

    def __str__(self):
        return f"|{self.x}|\n|{self.y}|\n"

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self.x, self.y

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self.x, self.y

    def calc_distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def draw_vertex(self):
        if self.shape == "circle":
            pygame.draw.circle(SCREEN, self.colour, (self.x, self.y), self.size)
        elif self.shape == "rect":
            pygame.draw.rect(SCREEN, self.colour, (self.x - SQUARE_SIZE/2, self.y - SQUARE_SIZE/2, SQUARE_SIZE, SQUARE_SIZE))
