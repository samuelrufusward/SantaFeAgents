import copy
import itertools
import numpy as np
from DarwinianModel import generate_trail


def test_move(moves, currentCell, currentDirection, trail):

    score = 0

    for action in moves:

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

        test_trail = copy.deepcopy(trail)
        bestResult = test_move(bestMove, currentCell, currentDirection, test_trail)

        # Updates trail and agent data to result of the best scoring set of actions
        currentCell = bestResult[1]
        currentDirection = bestResult[2]
        trail = bestResult[3]

        cumulativeScore += bestScore
        print("Cumulative Score:", cumulativeScore)

        scoresList = []


if __name__ == "__main__":
    # Agent that can see 7 moves into future
    run_model(numFutureMoves=7)
