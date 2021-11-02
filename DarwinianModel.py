import copy

import numpy as np
import random
defaultWeights=(0, 30, 0, 0, 70, 0)


class DfaData:

    def __init__(self):
        self.states = ['q0', 'q1']
        self.inputSymbols = ['0', '1']
        self.transitions = {
                          'q0': {0: ['q0', 'tl'], 1: ['q1', 'm']},
                          'q1': {0: ['q0', 'tr'], 1: ['q1', 'm']},
                      }
        self.initialState = 'q0'
        self.initialDirection = np.array([0, 1])
        self.actions = ['tl', 'tr', 'm']
        self.totalStatesNumber = 2


def generate_trail():
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


def change_start(dfa):

    dfaCopy = copy.deepcopy(dfa)
    dfa.initialState = random.choice(dfaCopy.states)


def add_state(dfa):

    dfaCopy = copy.deepcopy(dfa)
    stateNumber = dfaCopy.totalStatesNumber
    newState = 'q' + str(stateNumber)
    dfa.totalStatesNumber += 1
    dfa.states.append(newState)
    dfa.transitions[newState] = {0: [random.choice(dfaCopy.states), random.choice(dfaCopy.actions)],
                                 1: [random.choice(dfaCopy.states), random.choice(dfaCopy.actions)]}


def change_transition(dfa):

    dfaCopy = copy.deepcopy(dfa)

    if len(dfa.transitions) > 0:
        stateToChange = random.choice([state for state in dfaCopy.transitions])
        stateInput = random.choice([0, 1])
        newState = random.choice(dfaCopy.states)
        newAction = random.choice(dfaCopy.actions)
        dfa.transitions[stateToChange][stateInput] = [newState, newAction]


def generate_dfa(number_states=2):

    new_dfa = DfaData()

    if number_states-2 > 0:
        for i in range(number_states-2):
            add_state(new_dfa)

    return new_dfa


def mutate_dfa(dfa, weights):
    #      [change start, add state, change transition]
    possibleMutations = [1, 2, 3]

    mutation = random.choices(possibleMutations, weights=weights, k=1)
    mutation = mutation[0]

    if mutation == 1:
        change_start(dfa)

    elif mutation == 2:
        add_state(dfa)

    elif mutation == 3:
        change_transition(dfa)


def run_iteration(dfa, number_steps=600):

    trail = generate_trail()
    dfaStateHistory = []
    agentActionHistory = []
    currentCell = [0, 0]
    agentPosHistory = []
    agentPosHistory.append(currentCell)
    currentDirection = dfa.initialDirection
    currentCell = np.array([0,0])
    currentState = dfa.initialState
    score = 0

    for i in range(number_steps):
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

        if currentState in dfa.transitions:
            transition = dfa.transitions[currentState][adjecentCellValue]
        else:
            print(currentState, "not in", dfa.transitions)
            print("states:", dfa.states)
            return

        if transition != ['', '']:
            newState = transition[0]
            action = transition[1]

            if action == 'm':
                if adjecentCellValue == 1:
                    trail[adjecentCellPos[0], adjecentCellPos[1]] = 0
                    score += 1
                currentCell = adjecentCellPos
                if score == 89:
                    return score, agentActionHistory

            elif action == 'tl':
                currentDirection = np.array([-currentDirection[1], currentDirection[0]])

            elif action == 'tr':
                currentDirection = np.array([currentDirection[1], -currentDirection[0]])

            elif action == 'n':
                pass

        else:
            newState = currentState
            action = 'n'

        dfaStateHistory.append(newState)
        agentPosHistory.append(currentCell)
        agentActionHistory.append(action)
        currentState = newState

    return score, agentActionHistory

