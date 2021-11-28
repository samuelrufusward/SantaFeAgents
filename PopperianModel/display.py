import pygame
import numpy as np

'''
def initialise_display(size, caption, trail):
    pygame.init()

    window = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Popperian Model")

    draw_trail(window, trail, size)

    currentCell = INITIAL_POSITION  # start at top left
    currentDirection = np.array([0, 1])  # starts facing east
    draw_ant(window, currentCell, currentDirection)
    pygame.display.update()

    for action in moves:

        pygame.time.wait(100)

        onwardsCellRow = (currentCell[0] + currentDirection[0]) % 32
        onwardsCellColumn = (currentCell[1] + currentDirection[1]) % 32
        onwardsCellPos = [onwardsCellRow, onwardsCellColumn]
        foodAhead = trail[onwardsCellPos[0], onwardsCellPos[1]]

        if action == "forwards":
            if foodAhead == 1:
                trail[onwardsCellPos[0], onwardsCellPos[1]] = 0
                draw_trail(window, trail)
            currentCell = onwardsCellPos

        elif action == "turn_left":
            currentDirection = np.array([-currentDirection[1], currentDirection[0]])

        elif action == "turn_right":
            currentDirection = np.array([currentDirection[1], -currentDirection[0]])

        draw_ant(window,currentCell, currentDirection)
        '''


def draw_trail(window, trail, SIZE):
    """Draws 32*32 grid which represents the Santa fe Trail, where black squares represent food"""

    pygame.draw.rect(window, (255, 255, 255), (0, 0, SIZE, SIZE))
    # draws grid
    for i in range(32):
        for j in range(32):
            if trail[i, j] == 1:
                pygame.draw.rect(window, (0, 0, 0), (j * 20, i * 20, 20, 20))


def draw_ant(window, currentCell, currentDirection):
    """Draws the position and directional orientation of the ant"""

    # ant pictures are 20*20 by default
    if currentDirection[0] == 0 and currentDirection[1] == 1:
        sprite = pygame.image.load('rightant.png')
    elif currentDirection[0] == 1 and currentDirection[1] == 0:
        sprite = pygame.image.load('downant.png')
    elif currentDirection[0] == -1 and currentDirection[1] == 0:
        sprite = pygame.image.load('upant.png')
    elif currentDirection[0] == 0 and currentDirection[1] == -1:
        sprite = pygame.image.load('leftant.png')

    window.blit(sprite, (currentCell[1] * 20, currentCell[0] * 20))  # puts sprite onto win at position defined to be to left

