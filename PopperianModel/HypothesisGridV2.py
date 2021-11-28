import numpy as np
import random

MOVES = ['turn_left', 'forwards', 'turn_right']
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