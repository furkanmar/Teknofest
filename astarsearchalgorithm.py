import pygame
import sys
import random
import heapq
import math

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ROV Simulation")

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# ROV parameters
rov_size = 50
rov_speed = 5
rov_x = width // 2
rov_y = height // 2

# Object parameters
object_size = 30
object_x = random.randint(0, width - object_size)
object_y = random.randint(0, height - object_size)

# Barriers
barrier_count = 5
barriers = [pygame.Rect(random.randint(0, width - object_size), random.randint(0, height - object_size), object_size, object_size) for _ in range(barrier_count)]

# Load TalAI image with orientation arrow
talai_image = pygame.Surface((rov_size, rov_size), pygame.SRCALPHA)
pygame.draw.polygon(talai_image, blue, [(0, rov_size), (rov_size // 2, 0), (rov_size, rov_size)])
pygame.draw.line(talai_image, (255, 255, 255), (rov_size // 2, rov_size // 2), (rov_size // 2, 0), 2)

# Load target object image
object_image = pygame.Surface((object_size, object_size), pygame.SRCALPHA)
pygame.draw.circle(object_image, blue, (object_size // 2, object_size // 2), object_size // 2)

# A* pathfinding
def astar(graph, start, goal):
    heap = [(0, start)]
    visited = set()
    while heap:
        (cost, current) = heapq.heappop(heap)
        if current in visited:
            continue
        if current == goal:
            return reconstruct_path(graph, start, goal)
        visited.add(current)
        for next_node in graph.neighbors(current):
            if next_node not in visited:
                new_cost = cost + graph.cost(current, next_node)
                heapq.heappush(heap, (new_cost + heuristic(goal, next_node), next_node))
                graph.came_from[next_node] = current  # Update came_from

def reconstruct_path(graph, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = graph.came_from[current]
        path.append(current)
    return path[::-1]  # Reverse the path to get it from start to goal

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Graph:
    def __init__(self):
        self.barriers = [(b.x // object_size, b.y // object_size) for b in barriers]
        self.came_from = {}

    def neighbors(self, node):
        neighbors = [(node[0] + i, node[1] + j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
        return [n for n in neighbors if 0 <= n[0] < width // object_size and 0 <= n[1] < height // object_size and n not in self.barriers]

    def cost(self, current, next_node):
        return 1

graph = Graph()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Object detection using simple bounding box intersection
    if (
        rov_x < object_x + object_size
        and rov_x + rov_size > object_x
        and rov_y < object_y + object_size
        and rov_y + rov_size > object_y
    ):
        print("Object found!")

        # Respawn the object at a new location
        object_x = random.randint(0, width - object_size)
        object_y = random.randint(0, height - object_size)

    # Draw background
    screen.fill(white)

    # Calculate angle between ROV and target object
    angle = math.atan2(object_y - rov_y, object_x - rov_x)
    angle_deg = math.degrees(angle)

    # Draw TalAI with orientation based on the calculated angle
    rotated_talai = pygame.transform.rotate(talai_image, angle_deg)
    screen.blit(rotated_talai, (rov_x, rov_y))

    # Draw TalAI name
    font = pygame.font.SysFont(None, 30)
    text = font.render("TalAI", True, blue)
    screen.blit(text, (rov_x - 10, rov_y - 30))

    # Draw object using image
    screen.blit(object_image, (object_x, object_y))

    # Draw barriers
    for barrier in barriers:
        pygame.draw.rect(screen, red, barrier)

    # Perform A* pathfinding
    start = (rov_x // object_size, rov_y // object_size)
    goal = (object_x // object_size, object_y // object_size)
    path = astar(graph, start, goal)

    # Move TalAI along the path with a delay
    if path and len(path) > 1:
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]

            # Draw line between nodes
            pygame.draw.line(screen, (0, 255, 0), (current_node[0] * object_size + object_size // 2, current_node[1] * object_size + object_size // 2),
                             (next_node[0] * object_size + object_size // 2, next_node[1] * object_size + object_size // 2), 2)

            # Interpolate TalAI position for smoother movement
            rov_x = current_node[0] * object_size + (next_node[0] - current_node[0]) * object_size // 2
            rov_y = current_node[1] * object_size + (next_node[1] - current_node[1]) * object_size // 2

            pygame.display.flip()
            pygame.time.delay(100)

    pygame.display.flip()

    pygame.time.Clock().tick(30)
