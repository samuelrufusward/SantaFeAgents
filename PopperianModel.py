import copy
import itertools
import pygame
import numpy as np
import random
from DarwinianModel import generate_trail
from RunEvolutions import update_display
screenWidth = 640

MOVES = ["tl", "m", "tr"]
TURN_RIGHT = np.array([[0, 1], [-1, 0]])
TURN_LEFT = np.array([[0, -1], [1, 0]])
HALF_TURN = np.array([[-1, 0], [0, -1]])


def generate_hypothesis_grid(gridSize):
    """An all unitary hypothesis 2D grid, weightings will be added to each square in the grid following a successful
    hypothesis
    Used as the initial hypothesis grid - set to 7x7 because max distance from trail to next piece of food is 3sq's"""
    hypothesisGrid = np.ndarray(shape=(2, gridSize, gridSize), dtype=list)  # (z,y,x)

    # 1st layer : grid of vectors from origin,
    gridMid = int((gridSize - 1) / 2)

    for k in range(gridSize):
        for j in range(gridSize):
            movementVector = np.array([k - gridMid, -(j - gridMid)])
            movementSequence = vector2sequence(movementVector)
            sequenceLength = len(movementSequence)
            # + len(vector2sequence(invert_vector(movementVector)))

            if np.all(movementVector == 0):  # checks if vector is 0
                normalisedWeight = 0
            else:
                normalisedWeight = 1 / sequenceLength

            hypothesisGrid[0, j, k] = movementVector
            hypothesisGrid[1, j, k] = normalisedWeight

    return hypothesisGrid


def vector2sequence(vector):

    moveSequence = []
    verticalDisplacement = vector[1]
    horizontalDisplacement = vector[0]
    forwardSequence = [MOVES[1]] * abs(verticalDisplacement)
    lateralSequence = [MOVES[1]] * abs(horizontalDisplacement)

    if horizontalDisplacement > 0:  # going right
        lateralSequence = [MOVES[2]] + lateralSequence
    elif horizontalDisplacement < 0:  # going left
        lateralSequence = [MOVES[0]] + lateralSequence
    if verticalDisplacement >= 0:  # going forwards
        moveSequence = forwardSequence + lateralSequence
    elif verticalDisplacement < 0:  # going backwards
        if horizontalDisplacement == 0:  # only going backwards
            lateralSequence = [MOVES[0]]
        moveSequence = lateralSequence + [lateralSequence[0]] + forwardSequence

    return moveSequence


def sequence2vector(sequence):
    vector = np.array([0, 0])
    direction = np.array([0, 1])

    for move in sequence:
        if move == MOVES[1]:  # FORWARDS
            vector += direction
        elif move == MOVES[0]:  # LEFT
            direction = np.matmul(TURN_LEFT, direction)
        elif move == MOVES[2]:  # RIGHT
            direction = np.matmul(TURN_RIGHT, direction)

    return vector


def invert_vector(vector):

    global TURN_RIGHT, TURN_LEFT, HALF_TURN

    if vector[1] < 0:  # moving backwards
        reverseVector = np.matmul(HALF_TURN, -vector)
    elif vector[0] > 0:  # moving right
        reverseVector = np.matmul(TURN_LEFT, -vector)
    elif vector[0] < 0:  # moving left
        reverseVector = np.matmul(TURN_RIGHT, -vector)
    else:
        reverseVector = -vector

    return reverseVector


def get_hypothesis(hypothesisGrid):
    allWeights = hypothesisGrid[1].flatten()
    allHypothesis = hypothesisGrid[0].flatten()
    hypothesis = random.choices(allHypothesis, weights=allWeights)
    hypothesis = vector2sequence(hypothesis[0])

    return hypothesis


def update_weightings(hypothesis):
    """Will increment the successful hypothesis' weighting in the hypothesis grid and update its normalised weighting"""
    global hypothesisGrid

    rowIndx = 0
    sequence = vector2sequence(hypothesis)
    NumMoves = len(sequence)
    for row in hypothesisGrid[0]:
        collumnIndx = 0
        for vector in row:
            if np.all(vector == hypothesis):
                hypothesisWeight = hypothesisGrid[1, rowIndx, collumnIndx] * NumMoves
                hypothesisWeight += 1
                hypothesisGrid[1, rowIndx, collumnIndx] = hypothesisWeight / NumMoves
                break
            collumnIndx += 1
        rowIndx += 1

hypgrid = generate_hypothesis_grid(7)
a = 5

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


def run_model2(hypothesisGridSize=6):
    pygame.init()

    # Initialises game window
    win = pygame.display.set_mode((screenWidth, screenWidth))

    # Sets display window caption to Chess
    pygame.display.set_caption("Popperian Ant Model")
    hypothesisGrid = generate_hypothesis_grid(gridSize=7)

    trail = generate_trail()
    currentCell = [0, 0]
    currentDirection = np.array([0, 1])

    update_display(trail, win, currentCell, currentDirection)

    score = 0

    while score < 89:

        while score < 89:
            pygame.time.wait(100)
            adjecentCellRow = (currentCell[0] + currentDirection[0]) % 32
            adjecentCellColumn = (currentCell[1] + currentDirection[1]) % 32
            adjecentCellPos = [adjecentCellRow, adjecentCellColumn]
            adjecentCellValue = trail[adjecentCellPos[0], adjecentCellPos[1]]
            if adjecentCellValue == 1:
                moves = ['m']
            else:
                moves = get_hypothesis(hypothesisGrid)
                print("MOVES:", moves)

            for action in moves:

                if action == 'm':
                    trail[adjecentCellPos[0], adjecentCellPos[1]] = 0
                    currentCell = adjecentCellPos

                elif action == 'tl':
                    currentDirection = np.array([-currentDirection[1], currentDirection[0]])

                elif action == 'tr':
                    currentDirection = np.array([currentDirection[1], -currentDirection[0]])

                elif action == 'n':
                    pass

                update_display(trail, win, currentCell, currentDirection)


if __name__ == "__main__":
    # Agent that can see 7 moves into future
    run_model2()
    # TO DO:
    # If future moves is small it won't always have a clear best choice for which moves is best in the long run
    # When this happens it should chose a random one and keep going
    # For a whole population doing this, save these random choices and add weightings to the more successful ones
    # Branch splitting for each decision when same score for multiple paths to generate decision tree
    # Weightings for this decision tree updated based on final score/ number moves, then next generation uses this
    # tree with weightings to probabilistically make decisions
