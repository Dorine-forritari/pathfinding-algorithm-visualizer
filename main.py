import pygame
import copy
import math
import random

from vertex import Vertex


# Initialize the pygame.
pygame.init()

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

# Chance that a vertex (node) will be a wall.
# The higher the number, the smaller the chance.
WALL_CHANCE = 4

# Title
pygame.display.set_caption("Pathfinder")


def generate_vertices(x_axis, y_axis):
    """Generates a list of vertices (nodes) that will be displayed in rows and columns"""
    vertices_list = []
    for x in range(int(x_axis * 0.1), int(x_axis * 0.9 + SQUARE_SIZE), SQUARE_SIZE):
        for y in range(int(y_axis * 0.1), int(y_axis * 0.9 + SQUARE_SIZE), SQUARE_SIZE):
            vertices_list.append(Vertex(x, y))
    return vertices_list


def generate_walls(v_list):
    """Randomly turns some of the vertices into walls, the path cannot go through walls."""
    for v in v_list:
        if v.return_coordinates() != src and v.return_coordinates() != dest:
            wall_decision = random.randrange(0, WALL_CHANCE)
            if wall_decision == 0:
                v.wall = True


def set_src_to_current(v_list):
    """Finds source and sets this vertex to current with a distance of 0"""
    for v in v_list:
        if v.return_coordinates() == src:
            v.current = True
            v.distance = 0


def create_shortest_path(v, path):
    """Creates list of vertices that form the shortest path"""
    if v.previous:
        path.append(v.previous.return_coordinates())
        create_shortest_path(v.previous, path)
    return path


def draw():
    """Draws the background, vertices, walls and shortest path. Display keeps updating while program runs"""
    SCREEN.fill(BLACK)
    for v in vertex_list:
        # Source and destination vertices are marked with different colours and size
        if v.return_coordinates() == src:
            v.colour = BLUE
            v.size = 6
        if v.return_coordinates() == dest:
            v.colour = RED
            v.size = 6
        # Some vertices are displayed as walls
        if v.wall:
            v.visited = True
            v.colour = GRAY
            v.shape = "rect"
        v.draw_vertex()
        # Draw the shortest path
        if v.path is not None:
            # reversed_path is path from source to destination
            reversed_path = v.path[::-1]
            for index, node in enumerate(reversed_path[:-1]):
                pygame.draw.line(SCREEN, GREEN, (node[0], node[1]), (reversed_path[index + 1][0], reversed_path[index + 1][1]), 3)
    pygame.display.update()


vertex_list = generate_vertices(W, H)
# Create copy of vertex_list for nested for-loops in game logic
copy_list = copy.deepcopy(vertex_list)
# Locator list is used to randomly locate source and destination
locator_list = copy.deepcopy(copy_list)

random_src_index = random.randrange(0, len(locator_list))
src_vertex = locator_list[random_src_index]
# remove source vertex, so it can´t be chosen as destination vertex
locator_list.pop(random_src_index)
random_dest_index = random.randrange(0, len(locator_list))
dest_vertex = locator_list[random_dest_index]

src = src_vertex.return_coordinates()
dest = dest_vertex.return_coordinates()

generate_walls(vertex_list)

set_src_to_current(vertex_list)


def main():
    run = True
    # Game loop ends when the destination is reached or all vertices have been visited (and destination is unreachable).
    dest_not_reached = True
    not_all_visited = True
    # implemented a countdown to make it easier to make screen video´s
    countdown = 0
    # FPS = frames per second
    FPS = 8
    clock = pygame.time.Clock()

    while run:
        # End game if user clicks cross.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        while dest_not_reached and not_all_visited:
            draw()
            clock.tick(FPS)
            # algorithm starts after 3 seconds, this was just to start up my screen recorder
            countdown += 1
            if countdown > FPS * 3:
                for index, v in enumerate(vertex_list):
                    if v.current:
                        # loop through copy of list to find neighbours of each vertex
                        for i, x in enumerate(copy_list):
                            # Check which vertices are neighbours of the current vertex
                            if 0 < v.calc_distance(x) < 1.5 * SQUARE_SIZE:
                                # Check if neighbour wasn´t visited yet
                                if not x.visited:
                                    # Calculate distance to the new vertex through current vertex
                                    new_distance = v.calc_distance(x) + v.distance
                                    # If calculated distance is smaller than current estimated distance, adjust distance
                                    if new_distance < x.distance:
                                        vertex_list[i].distance = new_distance
                                        x.distance = new_distance
                                        # Set the current vertex as 'previous' in the next one.
                                        # This information will be used to create the shortest path.
                                        vertex_list[i].previous = v
                        # Set vertex to 'visited' in both vertex list and copy of list
                        v.visited = True
                        copy_list[index].visited = True
                        # Vertex is no longer the current vertex
                        v.current = False
                        copy_list[index].current = False
                        # change the colour of the vertex to mark it as visited
                        if v.return_coordinates() != src:
                            v.colour = WHITE
                        # If the visited vertex was the destination, end the while loop
                        if v.return_coordinates() == dest:
                            print("Destination reached!")
                            print("Distance to source is:", v.distance)
                            v.path = create_shortest_path(v, [v.return_coordinates()])
                            dest_not_reached = False
                        else:
                            # If destination is not reached yet, find unvisited vertex with smallest estimated distance
                            smallest_dist = INFINITY
                            unvisited_count = 0
                            for vertex in vertex_list:
                                if not vertex.visited:
                                    unvisited_count += 1
                                    if vertex.distance < smallest_dist:
                                        smallest_dist = vertex.distance
                            # End loop if all vertices have been visited
                            if unvisited_count == 0:
                                not_all_visited = False
                                print("Destination unreachable")
                            else:
                                # There might be several vertices with the smallest estimated distance
                                # ... so only set the first one of those to 'current'
                                new_current_found = False
                                for vertex in vertex_list:
                                    if not vertex.visited:
                                        if vertex.distance == smallest_dist and not new_current_found:
                                            vertex.current = True
                                            new_current_found = True
        draw()
        clock.tick(FPS)


main()
