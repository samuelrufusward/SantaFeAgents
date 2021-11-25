import copy
from GraphVisualisation import visualise_automata
import numpy as np
import random
import time
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
    newState = 'q' + str(stateNumber+1)
    dfa.totalStatesNumber += 1
    dfa.states.append(newState)
    dfa.transitions[newState] = {0: [random.choice(dfaCopy.states), random.choice(dfaCopy.actions)],
                                 1: [random.choice(dfaCopy.states), random.choice(dfaCopy.actions)]}


def delete_state(dfa):
    print("states before:", dfa.states)
    print("transitions before:", dfa.transitions)
    stateToDelete = random.choice(dfa.states)
    dfa.states.remove(str(stateToDelete))
    print("states after:", dfa.states)
    dfaCopy = copy.deepcopy(dfa)
    for state in dfa.transitions:
        if dfa.transitions[state][0][0] == str(stateToDelete):
            dfa.transitions[state][0][0] = str(random.choice(dfaCopy.states))
        elif dfa.transitions[state][1][0] == str(stateToDelete):
            dfa.transitions[state][1][0] = str(random.choice(dfaCopy.states))
    dfa.transitions.pop(str(stateToDelete))
    print("transitions after:", dfa.transitions)


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

    if number_states-2 >= 0:
        for i in range(number_states-2):
            add_state(new_dfa)

    return new_dfa


def mutate_dfa(dfa, weights):
    #      [change start, add state, change transition, delete state]
    possibleMutations = [1, 2, 3, 4]

    mutation = random.choices(possibleMutations, weights=weights, k=1)
    mutation = mutation[0]

    if mutation == 1:
        change_start(dfa)

    elif mutation == 2:
        add_state(dfa)

    elif mutation == 3:
        change_transition(dfa)

    elif mutation == 4:
        delete_state(dfa)


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


def crossover_automata2(dfa1, dfa2):

    dfa1copy = copy.deepcopy(dfa1)
    dfa2copy = copy.deepcopy(dfa2)

    # Selects random state from dfa1 to be cross-over
    crossoverState = random.choice(dfa1copy.states)
    print("crossover state:", crossoverState)

    # Makes state labels from dfa1 and dfa2 unique
    labelSwapDict = {}
    for key in dfa2copy.transitions:
        labelSwapDict[key] = "q" + str(dfa1copy.totalStatesNumber)
        dfa1copy.totalStatesNumber += 1

    print("dfa1 states:", dfa1copy.states)
    print("dfa1 transitions:", dfa1copy.transitions)
    print("dfa1 start state:", dfa1copy.initialState)
    print("\n")
    print("dfa2 states:", dfa2copy.states)
    print("dfa2 transitions:", dfa2copy.transitions)
    print("dfa2 start state:", dfa2copy.initialState)

    print(labelSwapDict)

    # Swaps all the transition labels for dfa2 to unique values
    for key in dfa2copy.transitions:
        dfa2copy.transitions[key][0][0] = labelSwapDict[dfa2copy.transitions[key][0][0]]
        dfa2copy.transitions[key][1][0] = labelSwapDict[dfa2copy.transitions[key][1][0]]

    # Updates keys for dfa2's transition dictionary to new unique values
    for state in dfa2copy.states:
        dfa2copy.transitions[labelSwapDict[state]] = dfa2copy.transitions[state]
        del dfa2copy.transitions[state]

    # Updates dfa2's initial state to unique value
    dfa2copy.initialState = labelSwapDict[dfa2copy.initialState]

    # Sets all instances of dfa2's initial state to the crossover point from dfa1 (NEW THING TO WORK ON)
    for key in dfa2copy.transitions:
        if dfa2copy.transitions[key][0][0] == str(labelSwapDict[dfa2copy.initialState]):
            dfa2copy.transitions[key][0][0] = str(crossoverState)
        if dfa2copy.transitions[key][1][0] == str(labelSwapDict[dfa2copy.initialState]):
            dfa2copy.transitions[key][1][0] = str(crossoverState)

    # Swaps all the state labels for dfa2 to unique values
    for i in range(len(dfa2copy.states)):
        dfa2copy.states[i] = labelSwapDict[dfa2copy.states[i]]

    # Replaces transitions going from the crossover state in dfa1 with those from the initial state of dfa2
    dfa1copy.transitions[crossoverState] = dict(copy.deepcopy(dfa2copy.transitions[dfa2copy.initialState]))

    # Removes initial state from dfa2
    dfa2copy.transitions.pop(dfa2copy.initialState)

    # Adds dfa2's transitions to dfa1's
    dfa1copy.transitions.update(dfa2copy.transitions)

    # Adds dfa2's states to dfa1's
    dfa1copy.states += dfa2copy.states

    # Updates dfa2's total state number
    dfa1copy.totalStatesNumber = dfa2copy.totalStatesNumber

    return dfa1copy


def crossover_automata(dfa1, dfa2):

    dfa1copy = copy.deepcopy(dfa1)
    dfa2copy = copy.deepcopy(dfa2)

    print("dfa1 states:", dfa1copy.states)
    print("dfa1 transitions:", dfa1copy.transitions)
    print("dfa1 start state:", dfa1copy.initialState)
    print("\n")
    print("dfa2 states:", dfa2copy.states)
    print("dfa2 transitions:", dfa2copy.transitions)
    print("dfa2 start state:", dfa2copy.initialState)

    # Selects random state from dfa1 to be cross-over
    crossoverState = random.choice(dfa1copy.states)
    print("crossover state:", crossoverState)

    # Makes state labels from dfa1 and dfa2 unique
    labelSwapDict = {}
    for key in dfa2copy.transitions:
        labelSwapDict[key] = "q" + str(dfa1copy.totalStatesNumber)
        dfa1copy.totalStatesNumber += 1

    labelSwapDict[copy.deepcopy(dfa2copy.initialState)] = str(crossoverState)

    print(labelSwapDict)

    # Swaps all the transition labels for dfa2 to unique values
    for key in dfa2copy.transitions:
        dfa2copy.transitions[key][0][0] = labelSwapDict[dfa2copy.transitions[key][0][0]]
        dfa2copy.transitions[key][1][0] = labelSwapDict[dfa2copy.transitions[key][1][0]]

    # Updates keys for dfa2's transition dictionary to new unique values
    for state in dfa2copy.states:
        dfa2copy.transitions[labelSwapDict[state]] = dfa2copy.transitions[state]
        del dfa2copy.transitions[state]

    # Updates dfa2's initial state to unique value
    #dfa2copy.initialState = labelSwapDict[dfa2copy.initialState]

    # Swaps all the state labels for dfa2 to unique values
    for i in range(len(dfa2copy.states)):
        dfa2copy.states[i] = labelSwapDict[dfa2copy.states[i]]

    print("\n")
    print("dfa2 states:", dfa2copy.states)
    print("dfa2 transitions:", dfa2copy.transitions)
    #print("dfa2 start state:", dfa2copy.initialState)

    # Adds dfa2's transitions to dfa1's
    dfa1copy.transitions.update(dfa2copy.transitions)

    # Adds dfa2's states to dfa1's
    dfa1copy.states += dfa2copy.states

    # Updates dfa2's total state number
    dfa1copy.totalStatesNumber = dfa2copy.totalStatesNumber

    print("dfa1 states:", dfa1copy.states)
    print("dfa1 transitions:", dfa1copy.transitions)
    print("dfa1 start state:", dfa1copy.initialState)

    return dfa1copy


#dfa1 = generate_dfa(number_states=3)
#visualise_automata(dfa1)
#time.sleep(3)
#dfa2 = generate_dfa(number_states=4)
#visualise_automata(dfa2)
#time.sleep(3)
#newdfa = crossover_automata(dfa1, dfa2)
#visualise_automata(newdfa)

#print(newdfa.transitions) # Stills maps to q5
