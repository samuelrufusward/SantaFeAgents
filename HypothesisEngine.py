import numpy as np

MOVES = ["tl", "m", "tr"]


def generate_trail():
    """Generates the generic santa fe trail"""
    trail = np.zeros((32, 32), dtype=int)
    trail[0, 1:4] = 1
    trail[1:5, 3] = 1
    trail[5, 3:7] = 1
    trail[5, 8:12] = 1
    trail[5:10, 12] = 1
    trail[11:15, 12] = 1
    trail[17:24, 12] = 1
    trail[24, 7:12] = 1
    trail[24, 3:5] = 1
    trail[25:29, 1] = 1
    trail[30, 2:6] = 1
    trail[28:30, 7] = 1
    trail[27, 8:15] = 1
    trail[24:27, 16] = 1
    trail[18:22, 16] = 1
    trail[15, 17] = 1
    trail[13:15, 20] = 1
    trail[7:11, 20] = 1
    trail[5, 21:23] = 1
    trail[3:5, 24] = 1
    trail[2, 25:28] = 1
    trail[3:5, 29] = 1
    trail[6, 29] = 1
    trail[9, 29] = 1
    trail[12, 29] = 1
    trail[14, 26:29] = 1
    trail[15, 23] = 1
    trail[18, 24] = 1
    trail[19, 27] = 1
    trail[22, 26] = 1
    trail[23, 23] = 1

    return trail


def generate_hypothesis_grid(gridSize):  # generates the santa fe trail
    """An all unitary hypothesis 2D grid, weightings will be added to each square in the grid following a successful
    hypothesis
    Used as the initial hypothesis grid - set to 7x7 because max distance from trail to next piece of food is 3sq's"""
    hypothesisGrid = np.ndarray(shape=(5, gridSize, gridSize), dtype=list)  # (z,y,x)

    # 1st layer : grid of vectors from origin,
    gridMid = int((gridSize-1) / 2)
    for k in range(gridSize):
        for j in range(gridSize):
            hypothesisGrid[0, j, k] = [k - gridMid, -(j - gridMid)]

    # 2nd layer : number of moves to get to position
    rowIndx = 0
    for row in hypothesisGrid[0]:
        collumnIndx = 0
        for vector in row:
            moveSequence = []
            verticalDisplacement = vector[1]
            horizontalDisplacement = vector[0]
            forwardSequence = [MOVES[1]] * abs(verticalDisplacement)
            lateralSequence = [MOVES[1]] * abs(horizontalDisplacement)

            if horizontalDisplacement > 0:                      # going right
                lateralSequence = [MOVES[2]] + lateralSequence
            elif horizontalDisplacement < 0:                    # going left
                lateralSequence = [MOVES[0]] + lateralSequence
            if verticalDisplacement >= 0:                        # going forwards
                moveSequence = forwardSequence + lateralSequence
            elif verticalDisplacement < 0:                      # going backwards
                if horizontalDisplacement == 0:  # only going backwards
                    lateralSequence = [MOVES[0]]
                moveSequence = lateralSequence + [lateralSequence[0]] + forwardSequence

            hypothesisGrid[1, rowIndx, collumnIndx] = moveSequence
            collumnIndx += 1
        rowIndx += 1

    # 3rd layer : weighting
    hypothesisGrid[2] = np.ones((gridSize, gridSize))
    hypothesisGrid[2, gridMid, gridMid] = 0

    # 4th layer : normalised weighting [(weighting/(no moves required)) / (sum of all normalised weightings)
    rowIndx = 0
    for row in hypothesisGrid[3]:
        collumnIndx = 0
        for normalisedWeighting in row:
            if len(hypothesisGrid[1, rowIndx, collumnIndx]) == 0:
                hypothesisGrid[3, rowIndx, collumnIndx] = 0
            else:
                hypothesisGrid[3, rowIndx, collumnIndx] = \
                    hypothesisGrid[2, rowIndx, collumnIndx] / len(hypothesisGrid[1, rowIndx, collumnIndx])
            collumnIndx += 1
        rowIndx += 1

    #5th layer : probabilistic normalised weightings
    weightingSum = 0
    for row in hypothesisGrid[3]:
        for normalisedWeighting in row:
            weightingSum += normalisedWeighting
    hypothesisGrid[4] = hypothesisGrid[3] / weightingSum

    return hypothesisGrid

hypothesisGrid = generate_hypothesis_grid(6)
#print(hypothesisGrid[4])
normalisedDistGrid = hypothesisGrid[4]
normalisedDistList = []
for normalisedDistRow in normalisedDistGrid:
    normalisedDistList = np.concatenate((normalisedDistList, normalisedDistRow), axis=None)
print(normalisedDistList)

movementsGrid = hypothesisGrid[1]
movementsList = []
for movementsGridRow in movementsGrid:
    movementsList = np.concatenate((movementsList, movementsGridRow), axis=None)

print(movementsList)

