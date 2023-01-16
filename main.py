import random

import pygame

from _agent import Agent, RandomAgent
from _grid import Grid

def quit_event_detected():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False


def single_run_pygame(grid_rows=5, grid_cols=6, nr_obstacles=5, too_many_moves=100, cell_pixels=20):
    pygame.init()
    window = pygame.display.set_mode((grid_rows * cell_pixels, grid_cols * cell_pixels))
    window.fill(pygame.Color('white'))
    pygame.display.set_caption('Path finder')
    font = pygame.freetype.SysFont('Arial', 30)

    agent = single_run(grid_rows, grid_cols, nr_obstacles, too_many_moves)
    for obs in agent.grid.obstacles:
        pygame.draw.rect(window, pygame.Color('black'), (*(x * cell_pixels for x in obs), cell_pixels, cell_pixels))
    pygame.draw.rect(window, pygame.Color('green'), (*(x * cell_pixels for x in agent.grid.origin), cell_pixels, cell_pixels))
    pygame.draw.rect(window, pygame.Color('red'), (*(x * cell_pixels for x in agent.grid.destination), cell_pixels, cell_pixels))
    pygame.display.update()

    path_iter = iter(agent.path)
    idx = 0

    run = True
    while run:
        try:
            next_pos = next(path_iter)
            pygame.display.set_caption(f'Path finder - moves: {idx}')
            #text_surface, _ = font.render(f'Move nr {idx}', pygame.Color('black'))
            #window.blit(text_surface, (0, 0))
            pygame.draw.rect(window, pygame.Color('blue'), (*(x * cell_pixels for x in next_pos), cell_pixels, cell_pixels))
            idx = idx + 1
        except StopIteration:
            pass
        pygame.time.delay(100)
        run = not quit_event_detected()
        pygame.display.update()


def single_run(grid_rows=5, grid_cols=6, nr_obstacles=5, too_many_moves=100):
    grid = Grid(grid_rows, grid_cols)
    grid.add_random_obstacles(nr_obstacles=nr_obstacles)
    agent = RandomAgent(grid)
    while not agent.at_destination() and agent.nr_of_moves < too_many_moves:
        agent.decide_move()
    if agent.at_destination():
        print(f"Success in {agent.nr_of_moves} moves!")
    else:
        print(f"Fail!")
    return agent


def multiple_runs(total_runs, grid_rows=5, grid_cols=6, nr_obstacles=5, too_many_moves=100):
    successes = 0
    for trial in range(total_runs):
        agent = single_run(grid_rows, grid_cols, nr_obstacles, too_many_moves)
        if agent.at_destination():
            successes = successes + 1
    print(f"Success: {successes / total_runs * 100}%")

if __name__ == '__main__':
    grid_rows = 20
    grid_cols = 20
    obstacles_ratio = .05

    single_run_pygame(
        grid_rows=grid_rows,
        grid_cols=grid_cols,
        nr_obstacles=int(grid_rows*grid_cols*obstacles_ratio),
        #nr_obstacles=10,
        too_many_moves=1000,
        cell_pixels=10
    )
    
#     grid_rows = 20
#     grid_cols = 20
#     obstacles_ratio = .05

#     multiple_runs(100, grid_rows, grid_cols, int(grid_rows*grid_cols*obstacles_ratio))