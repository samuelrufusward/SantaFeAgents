import copy
import itertools
import pygame
import numpy as np
from DarwinianModel import generate_trail
from RunEvolutions import update_display
screenWidth = 640


def visualise_moves(moves):
    pygame.init()

    # Initialises game window
    win = pygame.display.set_mode((screenWidth, screenWidth))

    # Sets display window caption to Chess
    pygame.display.set_caption("Popperian Ant Model")

    trail = generate_trail()
    currentCell = [0, 0]
    currentDirection = np.array([0, 1])

    update_display(trail, win, currentCell, currentDirection)

    for action in moves:

        pygame.time.wait(100)

        adjecentCellRow = (currentCell[0] + currentDirection[0]) % 32
        adjecentCellColumn = (currentCell[1] + currentDirection[1]) % 32
        adjecentCellPos = [adjecentCellRow, adjecentCellColumn]
        adjecentCellValue = trail[adjecentCellPos[0], adjecentCellPos[1]]

        if action == 'm':
            if adjecentCellValue == 1:
                trail[adjecentCellPos[0], adjecentCellPos[1]] = 0
            currentCell = adjecentCellPos

        elif action == 'tl':
            currentDirection = np.array([-currentDirection[1], currentDirection[0]])

        elif action == 'tr':
            currentDirection = np.array([currentDirection[1], -currentDirection[0]])

        elif action == 'n':
            pass

        update_display(trail, win, currentCell, currentDirection)


def test_move(move, currentCell, currentDirection, trail):

    score = 0

    for action in move:

        adjecentCellRow = (currentCell[0] + currentDirection[0]) % 32
        adjecentCellColumn = (currentCell[1] + currentDirection[1]) % 32
        adjecentCellPos = [adjecentCellRow, adjecentCellColumn]
        adjecentCellValue = trail[adjecentCellPos[0], adjecentCellPos[1]]

        if action == 'm':
            if adjecentCellValue == 1:
                trail[adjecentCellPos[0], adjecentCellPos[1]] = 0
                score += 1
            currentCell = adjecentCellPos

        elif action == 'tl':
            currentDirection = np.array([-currentDirection[1], currentDirection[0]])

        elif action == 'tr':
            currentDirection = np.array([currentDirection[1], -currentDirection[0]])

        elif action == 'n':
            pass

    return score, currentCell, currentDirection, trail


def run_model(numFutureMoves):
    trail = generate_trail()
    currentCell = [0,0]
    currentDirection = np.array([0, 1])
    cumulativeScore = 0
    scoresList = []
    optimalMoves = []

    actions = ['tr', 'tl', 'm']
    possibleMoves = [p for p in itertools.product(actions, repeat=numFutureMoves)]

    while cumulativeScore < 89:
        # Iterates through all possible moves
        for move in possibleMoves:
            test_trail = copy.deepcopy(trail)
            testResult = test_move(move, currentCell, currentDirection, test_trail)
            moveScore = testResult[0]
            scoresList.append(moveScore)

        # Selects best scoring set of actions
        index_max = np.argmax(scoresList)
        bestScore = scoresList[index_max]
        print("\nBest Score:", bestScore)
        bestMove = possibleMoves[index_max]
        print("Best Moves:", bestMove)

        for action in bestMove:
            optimalMoves.append(action)

        test_trail = copy.deepcopy(trail)
        bestResult = test_move(bestMove, currentCell, currentDirection, test_trail)

        # Updates trail and agent data to result of the best scoring set of actions
        currentCell = bestResult[1]
        currentDirection = bestResult[2]
        trail = bestResult[3]

        cumulativeScore += bestScore
        print("Cumulative Score:", cumulativeScore)

        scoresList = []

    visualise_moves(optimalMoves)


if __name__ == "__main__":
    # Agent that can see 7 moves into future
    run_model(numFutureMoves=8)
    # TO DO:
    # If future moves is small it won't always have a clear best choice for which moves is best in the long run
    # When this happens it should chose a random one and keep going
    # For a whole population doing this, save these random choices and add weightings to the more successful ones
    # Branch splitting for each decision when same score for multiple paths to generate decision tree
