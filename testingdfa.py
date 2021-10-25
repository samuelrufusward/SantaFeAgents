import numpy as np
import random
import pygame

pygame.init()
screenWidth = 640

# Initialises game window
win = pygame.display.set_mode((screenWidth, screenWidth))

# Sets display window caption to Chess
pygame.display.set_caption("Darwinian Ant Model")
##print(trail)


def update_display(trail, currentCell, currentDirection):
    pygame.draw.rect(win, (255, 255, 255), (0, 0, screenWidth, screenWidth))
    for i in range(32):
        for j in range(32):
            if trail[i, j] == 1:
                pygame.draw.rect(win, (0, 0, 0), (j * 20, i * 20, 20, 20))

    if currentDirection[0] == 0 and currentDirection[1] == 1:
        sprite = pygame.image.load('rightant.png')
    elif currentDirection[0] == 1 and currentDirection[1] == 0:
        sprite = pygame.image.load('downant.png')
    elif currentDirection[0] == -1 and currentDirection[1] == 0:
        sprite = pygame.image.load('upant.png')
    elif currentDirection[0] == 0 and currentDirection[1] == -1:
        sprite = pygame.image.load('leftant.png')

    win.blit(sprite, (currentCell[1] * 20, currentCell[0] * 20))
    #pygame.draw.rect(win, (0, 255, 0), (currentCell[1] * 20, currentCell[0] * 20, 20, 20))
    pygame.display.update()

class dfa_data:

    def __init__(self):
            self.states = ['q0', 'q1']
            self.inputSymbols = ['0', '1']
            self.transitions = {
                              'q0': {0: ['q0', 'tl'], 1: ['q1', 'm']},
                              'q1': {0: ['q0', 'tr'], 1: ['q1', 'm']},
                          }
            self.initialState = 'q0'
            self.initialDirection = np.array([0,1])
            self.actions = ['tl', 'tr', 'm']
            self.totalStatesNumber = 2


def mutate_dfa(dfa):

    possibleMutations = ["change start", "add state", "delete state", "change transition",
                 "add transition", "delete transition"]

    mutation = random.choices(possibleMutations, weights=(5, 20, 5, 25, 40, 5), k=1)
    mutation = mutation[0]

    #print("mutation:", mutation)

    if mutation == 'change start':
        dfa.initialState = random.choice(dfa.states)

    if mutation == 'add state':

        stateNumber = dfa.totalStatesNumber
        newState = 'q' + str(stateNumber)
        dfa.totalStatesNumber += 1

        #print("States before:", dfa.states)
        #print("New State to be added:", newState)
        dfa.states.append(newState)
        dfa.transitions[newState] = {0: ['', ''], 1: ['', '']}

    if mutation == 'delete state':
        # Have to make sure it can handle all states being deleted
        if len(dfa.states) > 2:

            stateToDelete = random.choice(dfa.states)
            if stateToDelete != dfa.initialState:

                dfa.states.remove(stateToDelete)

                del dfa.transitions[stateToDelete]

                for state in dfa.transitions:

                    if dfa.transitions[state][0][0] == stateToDelete:
                        dfa.transitions[state][0] = ['', '']
                    if dfa.transitions[state][1][0] == stateToDelete:
                        dfa.transitions[state][1] = ['', '']

    if mutation == 'change transition':
        if len(dfa.transitions) > 0:
            stateToChange = random.choice([state for state in dfa.transitions])
            #print("State to be changed:", stateToChange)
            stateInput = random.choice([0,1])
            #print("stateInput", stateInput)
            newState = random.choice(dfa.states)
            #print("newState", newState)
            newAction = random.choice(dfa.actions)
            #print("newAction", newAction)
            dfa.transitions[stateToChange][stateInput] = [newState, newAction]

    if mutation == 'add transition':
        emptyTransitions = []
        for state in dfa.transitions:
            if dfa.transitions[state][0] == ['', '']:
                emptyTransitions.append([state, 0])

            elif dfa.transitions[state][1] == ['', '']:
                emptyTransitions.append([state, 1])

        if emptyTransitions:
            newTransitionChoice = random.choice(emptyTransitions)

            stateToChange = newTransitionChoice[0]
            inputToChange = newTransitionChoice[1]

            newTransitionDestination = random.choice(dfa.states)
            newTransitionAction = random.choice(dfa.actions)

            dfa.transitions[stateToChange][inputToChange] = [newTransitionDestination, newTransitionAction]

    if mutation == 'delete transition':
        if dfa.transitions:
                state = random.choice(dfa.states)
                input = random.choice([0, 1])

                dfa.transitions[state][input] = ['', '']

    #print("States After:", dfa.states)
    #print("Transitions After", dfa.transitions)
    #print("Initial State After", dfa.initialState)

    return dfa


def run_iteration(dfa, visualise=False):
    #print("States:", dfa.states)
    #print("Transitions", dfa.transitions)
    #print("Initial State", dfa.initialState)
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

    #for row in trail:
        #print(row)

    dfaStateHistory = []
    agentActionHistory = []
    currentCell = [0, 0]
    #print("currentCell", currentCell)
    agentPosHistory = []
    agentPosHistory.append(currentCell)

    currentDirection = dfa.initialDirection
    currentCell = np.array([0,0])
    currentState = dfa.initialState
    score = 0
    if visualise:
        update_display(trail, currentCell, currentDirection)

    for i in range(1000):
        if visualise:
            pygame.time.wait(80)
        #print("current state:", currentState)
        if dfa.initialState == '':
            newState = currentState
            action = 'n'
            dfaStateHistory.append(newState)
            agentPosHistory.append(currentCell)
            agentActionHistory.append(action)

        adjecentCellRow = (currentCell[0] + currentDirection[0]) % 32
        adjecentCellColumn = (currentCell[1] + currentDirection[1]) % 32
        adjecentCellPos = [adjecentCellRow, adjecentCellColumn]

        adjecentCellValue = trail[adjecentCellPos[0], adjecentCellPos[1]]


        #print("adj cell pos", adjecentCellPos)
        #print("adj cell value", adjecentCellValue)
        transition = ['', '']
        try:

            transition = dfa.transitions[currentState][adjecentCellValue]

        except Exception as e:
            print("ERROR")
            print(e)
            print("currentState:", currentState)
            print("transitions:", dfa.transitions)

        if transition != ['', '']:
            newState = transition[0]
            action = transition[1]

            #print("new state",newState)
            #print("action", action)

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

        else:
            newState = currentState
            action = 'n'
        #print("current direction", currentDirection)
        #print("currentCell", currentCell)
        #print("score:", score)
        dfaStateHistory.append(newState)
        agentPosHistory.append(currentCell)
        agentActionHistory.append(action)
        currentState = newState
        #for row in trail:
            #print(row)
        #print("\n")
        #print("state history: ", dfaStateHistory)
    #print(score)
    #if score > 11:
        #print("Initial State:", dfa.initialState)
        #print("Successful tranitions:", dfa.transitions)
        if visualise:
            update_display(trail, currentCell, currentDirection)

    return score, agentActionHistory


scoresList = []


for j in range(100000):
    dfa2 = dfa_data()
    for i in range(10):
        dfa2 = mutate_dfa(dfa2)

    #print(dfa2.transitions)

    score, agentActionHistory = run_iteration(dfa2)
    scoresList.append(score)
    #print("Agent Action History:", agentActionHistory)
    if score > 20:
        print("Final Score:", score)

        run_iteration(dfa2, visualise=True)

# sorting the list
#scoresList.sort()
#counter = 0
# printing the last element
#for individualScore in scoresList:
    #if individualScore > 11:
        #counter+=1
#print("successful:", counter)
