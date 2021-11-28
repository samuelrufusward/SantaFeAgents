import pickle
import pygame.surfarray
from test import Popperian
WINDOW_SIZE = 640

with open('best_ant_animation', 'rb') as handle:
    frames = pickle.load(handle)

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
for frame in frames:
    surf = pygame.surfarray.make_surface(frame)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    pygame.time.wait(200)
