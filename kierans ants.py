import numpy as np
import trail
import HypothesisGridV2 as grid
import random
import pygame
import display

INITIAL_DIRECTION = np.array([0, 1])
INITIAL_POSITION = np.array([0, 0])
MAX_MOVES = 600

LEFT = np.array([[0, -1], [1, 0]])
RIGHT = np.array([[0, 1], [-1, 0]])

SANTA_FE = trail.generate_trail()
WINDOW_SIZE = 640


# for sake of convention x axis goes down from top left and y axis goes rightwards
class KANT:

    def __init__(self, path):
        self.path = path
        self.position = INITIAL_POSITION
        self.direction = INITIAL_DIRECTION
        self.score = 0
        self.moves = 0

    def move_forward(self):
        """Will move the ant one unit forwards in the direction it is facing"""

        self.position += self.direction
        self.moves += 1

        display.draw_ant(window, self.position, self.direction)
        pygame.display.update()
        return

    def turn(self, direction):
        """Will turn the ant left or right depending on the direction parameter"""

        self.direction = np.matmul(direction, self.direction)
        self.moves += 1

        display.draw_ant(window, self.position, self.direction)
        pygame.display.update()
        return

    def food_ahead(self):
        """Will evaluate whether there is food in the square directly in front of the ant"""

        blockAhead = self.position + self.direction
        if self.path[blockAhead[0], blockAhead[1]] == 1:
            return True
        else:
            return False

    def eat_food(self):
        """Will remove food from the trail at the position the ant is standing"""

        self.path[self.position[0], self.position[1]] = 0
        self.score += 1
        return


class Popperian(KANT):

    GRID_SIZE = 7
    hypothesisGrid = grid.generate_hypothesis_grid(GRID_SIZE)

    def __init__(self, path):
        super().__init__(path)
        self.memory = {'displacement': np.array([0, 0]), 'orientation': np.array([0, 1])}
        self.hypothesis = np.array([0, 0])

    def get_hypothesis(self):
        """Will get a pseudo random vector from the hypothesis grid based on each hypothesis' individual weightings"""

        allWeights = self.hypothesisGrid[1].flatten()
        allHypothesis = self.hypothesisGrid[0].flatten()
        hypothesis = random.choices(allHypothesis, weights=allWeights)
        self.hypothesis = hypothesis[0]

        return

    def find_food(self, vector):
        """Will move to a vector, and will terminate on acquisition of food. Will return true if food is found, and
        false if not - by extension if false is returned it means that the ant has moved to the hypothesis and has not
        found food"""

        moveSequence = grid.vector2sequence(vector)

        for move in moveSequence:
            if self.food_ahead():
                self.move_forward()
                self.eat_food()

                self.memory['displacement'] += self.memory['orientation']

                return True

            else:
                if move == 'forwards':
                    self.move_forward()
                    self.memory['displacement'] += self.memory['orientation']
                if move == 'turn_left':
                    self.turn(LEFT)
                    self.memory['orientation'] = np.matmul(LEFT, self.direction)
                if move == 'turn_right':
                    self.turn(RIGHT)
                    self.memory['orientation'] = np.matmul(RIGHT, self.direction)
        return False

    def run_hypothesis(self):
        """Walks ant to a hypothesis, and back if no food is found"""

        self.memory = {'displacement': np.array([0, 0]), 'orientation': np.array([0, 1])}
        facingLeft = np.array([-1, 0])
        facingRight = np.array([1, 0])
        facingBack = np.array([0, -1])

        if self.find_food(self.hypothesis):  # if food is found along or at the hypothesis
            self.update_weightings(self.memory['displacement'])

            return True
        else:
            reverseVector = grid.invert_vector(self.memory['displacement'])
            if self.find_food(reverseVector):  # if food is found along the route back
                self.update_weightings(self.memory['displacement'])

                return True
            else:  # turn to face original orientation
                if np.all(self.memory['orientation'] == facingBack):
                    self.turn(LEFT)
                    self.turn(LEFT)

                elif np.all(self.memory['orientation'] == facingLeft):
                    self.turn(RIGHT)

                elif np.all(self.memory['orientation'] == facingRight):
                    self.turn(LEFT)

        return False

    @classmethod
    def update_weightings(cls, successfulHypothesis):
        rowIndx = 0
        sequence = grid.vector2sequence(successfulHypothesis)
        NumMoves = len(sequence)
        for row in cls.hypothesisGrid[0]:
            collumnIndx = 0
            for movementVector in row:
                if np.all(movementVector == successfulHypothesis):
                    hypothesisWeight = cls.hypothesisGrid[1, rowIndx, collumnIndx] * NumMoves
                    hypothesisWeight += 1
                    cls.hypothesisGrid[1, rowIndx, collumnIndx] = hypothesisWeight / NumMoves
                    return
                collumnIndx += 1
            rowIndx += 1


if __name__ == "__main__":
    pygame.init()

    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Popperian Model")

    display.draw_trail(window, SANTA_FE, WINDOW_SIZE)

    ant = Popperian(SANTA_FE)

    display.draw_ant(window, ant.position, ant.direction)
    pygame.display.update()

    while ant.moves <= MAX_MOVES:
        if ant.food_ahead():
            ant.move_forward()
            ant.eat_food()
        else:
            successful = False
            while not successful:
                ant.get_hypothesis()
                successful = ant.run_hypothesis()

    print("First ant has eaten" + ant.score + "foodskins")



"""
a= ant(1,1)
arr=[]
class colony:
    def __init__(self, gen, trail):

    for i in range(100):
        arr.append(ant(i,1))
    arr[1].movex(1)
a.movex(1)
"""