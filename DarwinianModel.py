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


def clone_dfa(dfa):

    newDfa = DfaData()
    newDfa.states = list(dfa.states)
    newDfa.inputSymbols = list(dfa.inputSymbols)
    newDfa.transitions = dict(dfa.transitions)
    newDfa.initialState = str(dfa.initialState)
    newDfa.initialDirection = list(dfa.initialDirection)
    newDfa.actions = list(dfa.actions)
    newDfa.totalStatesNumber = int(dfa.totalStatesNumber)

    return newDfa


def mutate_dfa(dfa, weights):

    possibleMutations = ["change start", "add state", "delete state", "change transition",
                 "add transition", "delete transition"]

    mutation = random.choices(possibleMutations, weights=weights, k=1)
    mutation = mutation[0]                      #weights=(5, 20, 5, 25, 40, 5)

    if mutation == 'change start':
        dfa.initialState = random.choice(dfa.states)

    if mutation == 'add state':

        #stateNumber = dfa.totalStatesNumber
        #newState = 'q' + str(stateNumber)
        #dfa.totalStatesNumber += 1
        #dfa.states.append(newState)
        #dfa.transitions[newState] = {0: ['', ''], 1: ['', '']}
        stateNumber = dfa.totalStatesNumber
        newState = 'q' + str(stateNumber)
        dfa.totalStatesNumber += 1
        dfa.states.append(newState)
        dfa.transitions[newState] = {0: [random.choice(dfa.states), random.choice(dfa.actions)],
                                             1: [random.choice(dfa.states), random.choice(dfa.actions)]}

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
            stateInput = random.choice([0,1])
            newState = random.choice(dfa.states)
            newAction = random.choice(dfa.actions)
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

    return dfa


def mutate_dfa2(dfaToMutate, weights):
    possibleMutations = ["change start", "add state", "change transition"]

    mutation = random.choices(possibleMutations, weights=weights, k=1)
    mutation = mutation[0]

    if mutation == "change start":
        dfaToMutate.initialState = random.choice(dfaToMutate.states)

    elif mutation == "add state":
        stateNumber = dfaToMutate.totalStatesNumber
        newState = 'q' + str(stateNumber)
        dfaToMutate.totalStatesNumber += 1
        dfaToMutate.states.append(newState)
        dfaToMutate.transitions[newState] = {0: [random.choice(dfaToMutate.states), random.choice(dfaToMutate.actions)],
                                             1: [random.choice(dfaToMutate.states), random.choice(dfaToMutate.actions)]}

    elif mutation == "change transition":
        stateToChange = random.choice(dfaToMutate.states)
        inputToChange = random.choice([0,1])

        newTargetState = random.choice(dfaToMutate.states)
        newTargetAction = random.choice(dfaToMutate.actions)

        dfaToMutate.transitions[stateToChange][inputToChange] = [newTargetState, newTargetAction]

    mutatedDfa = dfaToMutate
    return mutatedDfa


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

