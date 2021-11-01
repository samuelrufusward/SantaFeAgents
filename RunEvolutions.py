import random
import copy
from DarwinianModel import DfaData, generate_trail, clone_dfa, mutate_dfa, mutate_dfa2, run_iteration
import numpy as np
import pygame
import time
from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA
screenWidth = 640


def update_display(trail, win, currentCell, currentDirection):
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


def visualise_dfa():
    new_dfa = VisualDFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q0', '1': 'q2'},
            'q2': {'0': 'q2', '1': 'q1'}
        },
        initial_state='q0',
        final_states={'q1'}
    )

    new_dfa.show_diagram(view=True)


def visualise_iterations(dfa):
    pygame.init()

    # Initialises game window
    win = pygame.display.set_mode((screenWidth, screenWidth))

    # Sets display window caption to Chess
    pygame.display.set_caption("Darwinian Ant Model")
    trail = generate_trail()

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

    update_display(trail, win, currentCell, currentDirection)

    for i in range(800):

        pygame.time.wait(50)
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

        update_display(trail, win, currentCell, currentDirection)

        if score == 89:
            pygame.time.wait(5000)
            break

    return score, agentActionHistory

def sorting_of_element(list1, list2):
    # initializing blank dictionary
    f_1 = {}

    # initializing blank list
    final_list = []

    # Addition of two list in one dictionary
    f_1 = {list1[i]: list2[i] for i in range(len(list2))}

    # sorting of dictionary based on value
    f_lst = {k: v for k, v in sorted(f_1.items(), key=lambda item: item[1])}
    #print("f_list", f_lst)
    # Element addition in the list
    for i in f_lst.keys():
        final_list.append(i)
    return final_list


def run_model(num_of_initial_mutations, num_generations, generation_size, max_dfa_states):

    scores_list = []
    dfa_list = []

    for j in range(generation_size):
        dfa_model = DfaData()
        for i in range(num_of_initial_mutations):
            # Only additive mutations initially (add state, add transition)
            weights = (0, 30, 0, 0, 70, 0)
            dfa_model = mutate_dfa(dfa_model, weights=weights)
        dfa_list.append(dfa_model)

    for j in range(num_generations):

        for dfa_model in dfa_list:
            score, action_history = run_iteration(dfa_model)
            scores_list.append(score)
            # print("Agent Action History:", agentActionHistory)
            if score == 89:
                visualise_iterations(dfa_model)

        sum_of_scores = sum(scores_list)
        if sum_of_scores == 0:
            print("Evolutions failed: best score reached 0.")
            return

        average_score = sum(scores_list) / len(scores_list)
        print("\naverage score:", average_score)
        print("best score of generation:", max(scores_list))

        new_dfa_list = []

        # Sort dfa list by score
        sorted_dfas = list(reversed(sorting_of_element(dfa_list, scores_list)))

        new_dfa_list.append(sorted_dfas[0])

        for dfa_model in sorted_dfas[1:]:
            if len(dfa_model.states) > max_dfa_states:
                weights = (10, 0, 0, 70, 20, 0)
            else:
                weights = (5, 25, 0, 25, 45, 0)
            mutated_dfa = mutate_dfa(dfa_model, weights=weights)
            new_dfa_list.append(mutated_dfa)

        dfa_list = new_dfa_list
        scores_list = []


def run_model2(num_of_initial_mutations, num_generations, generation_size, max_dfa_states):

    scores_list = []
    dfa_list = []

    for j in range(generation_size):
        dfa_model = DfaData()
        for i in range(num_of_initial_mutations):
            # Only additive mutations initially (add state, add transition)
            weights = (10, 30, 60)
            dfa_model = mutate_dfa2(dfa_model, weights=weights)
        dfa_list.append(dfa_model)

    for j in range(num_generations):

        for dfa_model in dfa_list:
            score, action_history = run_iteration(dfa_model)
            scores_list.append(score)
            # print("Agent Action History:", agentActionHistory)
            if score == 89:
                visualise_iterations(dfa_model)

        sum_of_scores = sum(scores_list)
        if sum_of_scores == 0:
            print("Evolutions failed: best score reached 0.")
            return

        average_score = sum(scores_list) / len(scores_list)
        print("\naverage score:", average_score)
        print("best score of generation:", max(scores_list))

        new_dfa_list = []
        parent_list = []
        mutant_list = []

        # Sort dfa list by score
        sorted_dfas = list(reversed(sorting_of_element(dfa_list, scores_list)))
        #print("Sorted dfas:", sorted_dfas)

        parent_dfas = sorted_dfas[0:5]
        for parent in parent_dfas:
            cloned_parent = clone_dfa(parent)
            parent_list.append(cloned_parent)

        for i in range(199):
            for parent in parent_dfas:
                new_dfa = clone_dfa(parent)
                mutant_list.append(new_dfa)

        score1, history1 = run_iteration(parent_list[0])
        print("Score1:", score1)

        new_dfa_list = parent_list
        print("parent list:", new_dfa_list)

        #print(len(new_dfa_list))
        #print(new_dfa_list)

        for i in range(len(mutant_list)):
            dfa_model = mutant_list[i]
            if random.randint(0, 100) < 10:
                if len(dfa_model.states) >= max_dfa_states:
                    weights = (10, 30, 60)
                else:
                    weights = (10, 0, 90)
                mutated_dfa = mutate_dfa2(dfa_model, weights=weights)
                mutant_list[i] = mutated_dfa

        score2, history2 = run_iteration(new_dfa_list[0])
        print("Score2:", score2)

        new_dfa_list += mutant_list
        print("full list", new_dfa_list)

        dfa_list = new_dfa_list
        scores_list = []


def run_model3(num_of_initial_mutations, num_generations, generation_size, max_dfa_states):

    scores_list = []
    dfa_list = []

    for j in range(generation_size):
        dfa_model = DfaData()
        for i in range(num_of_initial_mutations):
            # Only additive mutations initially (add state, add transition)
            weights = (10, 30, 60)
            dfa_model = mutate_dfa2(dfa_model, weights=weights)
        dfa_list.append(dfa_model)

    for j in range(num_generations):

        for dfa_model in dfa_list:
            score, action_history = run_iteration(dfa_model)
            scores_list.append(score)
            # print("Agent Action History:", agentActionHistory)
            if score == 89:
                visualise_iterations(dfa_model)

        sum_of_scores = sum(scores_list)
        if sum_of_scores == 0:
            print("Evolutions failed: best score reached 0.")
            return

        average_score = sum(scores_list) / len(scores_list)
        print("\naverage score:", average_score)
        print("best score of generation:", max(scores_list))

        new_dfa_list = []

        # Sort dfa list by score
        sorted_dfas = list(reversed(sorting_of_element(dfa_list, scores_list)))

        new_dfa_list.append(sorted_dfas[0])

        for dfa_model in sorted_dfas[1:]:
            if len(dfa_model.states) > max_dfa_states:
                weights = (10, 30, 60)
            else:
                weights = (10, 0, 90)
            mutated_dfa = mutate_dfa2(dfa_model, weights=weights)
            new_dfa_list.append(mutated_dfa)

        dfa_list = new_dfa_list
        scores_list = []


def run_model4(num_of_initial_mutations, num_generations, generation_size, max_dfa_states):

    scores_list = []
    mutant_scores_list = []
    parent_scores_list = []
    dfa_list = []
    print("\nGeneration Number: 0")

    for i in range(generation_size):
        dfa_model = DfaData()
        for j in range(num_of_initial_mutations):
            dfa_model = mutate_dfa2(dfa_model, weights=(10, 30, 60))
        dfa_list.append(dfa_model)
        score, history = run_iteration(dfa_model)
        scores_list.append(score)

    average_score = sum(scores_list) / len(scores_list)
    print("\naverage score:", average_score)
    print("best score of generation:", max(scores_list))

    for i in range(num_generations):
        print("\nGeneration Number:", i+1)
        # Sort DFAs by score in descending order
        sorted_dfas = list(reversed(sorting_of_element(dfa_list, scores_list)))

        # Visualise every 50 generations
        #if i % 50 == 0:
        #    visualise_iterations(sorted_dfas[0])

        parent_scores_list = []
        parent_dfas = sorted_dfas[0:5]
        for dfa_model in parent_dfas:
            parent_score, parent_history = run_iteration(dfa_model)
            parent_scores_list.append(parent_score)
            if parent_score == 89:
                print("Score: 89")
                print("Number of moves:", len(parent_history))
                visualise_iterations(dfa_model)

        mutated_dfa_list = []
        mutant_scores_list = []
        for k in range(199):
            for dfa_model in parent_dfas:
                new_dfa = copy.deepcopy(dfa_model)
                if random.randint(0, 100) < 60:
                    if len(new_dfa.states) <= max_dfa_states:
                        weights = (10, 30, 60)
                    else:
                        weights = (10, 0, 90)
                    mutated_dfa = mutate_dfa2(new_dfa, weights=weights)

                    mutant_score, mutant_history = run_iteration(mutated_dfa)
                    if mutant_score == 89:
                        print("Score: 89")
                        print("Number of moves:", len(mutant_history))
                        visualise_iterations(mutated_dfa)
                    mutant_scores_list.append(mutant_score)
                    mutated_dfa_list.append(mutated_dfa)

        dfa_list = []
        scores_list = []

        for dfa_model in parent_dfas:
            dfa_list.append(dfa_model)
        for dfa_model in mutated_dfa_list:
            dfa_list.append(dfa_model)
        for score in parent_scores_list:
            scores_list.append(score)
        for score in mutant_scores_list:
            scores_list.append(score)

        average_score = sum(scores_list) / len(scores_list)

        print("average score:", average_score)
        print("best score of generation:", max(scores_list))


def run_model5(num_of_initial_mutations, num_generations, generation_size, max_dfa_states):

    scores_list = []
    mutant_scores_list = []
    parent_scores_list = []
    dfa_list = []
    print("\nGeneration Number: 0")

    for i in range(generation_size):
        dfa_model = DfaData()
        for j in range(num_of_initial_mutations):
            dfa_model = mutate_dfa2(dfa_model, weights=(10, 30, 60))
        dfa_list.append(dfa_model)
        score, history = run_iteration(dfa_model, number_steps=500)
        scores_list.append(score)

    average_score = sum(scores_list) / len(scores_list)
    print("\naverage score:", average_score)
    print("best score of generation:", max(scores_list))

    for i in range(num_generations):
        print("\nGeneration Number:", i+1)
        # Sort DFAs by score in descending order
        sorted_dfas = list(reversed(sorting_of_element(dfa_list, scores_list)))

        # Visualise every 50 generations
        if i % 50 == 0:
            visualise_iterations(sorted_dfas[0])

        parent_scores_list = []
        parent_dfas = sorted_dfas[0:10]
        for dfa_model in parent_dfas:
            parent_score, parent_movement_history = run_iteration(dfa_model, number_steps=500)
            parent_scores_list.append(parent_score)
            if parent_score == 89:
                print("Score: 89")
                print("Number of moves:", len(parent_movement_history))
                print("Move history:", parent_movement_history)
                visualise_iterations(dfa_model)

        mutated_dfa_list = []
        mutant_scores_list = []
        for k in range(99):
            for dfa_model in parent_dfas:
                new_dfa = copy.deepcopy(dfa_model)
                if random.randint(0, 100) < 60:

                    if len(new_dfa.states) <= max_dfa_states:
                        weights=(10, 30, 60)
                    else:
                        weights=(20, 0, 80)
                    mutated_dfa = mutate_dfa2(new_dfa, weights=weights)

                    mutant_score, mutant_movement_history = run_iteration(mutated_dfa, number_steps=500)
                    if mutant_score == 89:
                        print("Score: 89")
                        print("Number of moves:", len(mutant_movement_history))
                        print("Move history:", mutant_movement_history)
                        visualise_iterations(mutated_dfa)
                    mutant_scores_list.append(mutant_score)
                    mutated_dfa_list.append(mutated_dfa)

        dfa_list = []
        scores_list = []

        for dfa_model in parent_dfas:
            dfa_list.append(dfa_model)
        for dfa_model in mutated_dfa_list:
            dfa_list.append(dfa_model)
        for score in parent_scores_list:
            scores_list.append(score)
        for score in mutant_scores_list:
            scores_list.append(score)

        average_score = sum(scores_list) / len(scores_list)

        print("average score:", average_score)
        print("best score of generation:", max(scores_list))


def run_model6(num_of_initial_mutations, num_generations, generation_size, max_dfa_states):

    scores_list = []
    mutant_scores_list = []
    parent_scores_list = []
    dfa_list = []
    print("\nGeneration Number: 0")

    for i in range(generation_size):
        dfa_model = DfaData()
        for j in range(num_of_initial_mutations):
            dfa_model = mutate_dfa2(dfa_model, weights=(10, 30, 60))
        dfa_list.append(dfa_model)
        score, history = run_iteration(dfa_model, number_steps=500)
        scores_list.append(score)

    average_score = sum(scores_list) / len(scores_list)
    print("\naverage score:", average_score)
    print("best score of generation:", max(scores_list))

    for i in range(num_generations):
        print("\nGeneration Number:", i+1)
        # Sort DFAs by score in descending order
        sorted_dfas = list(reversed(sorting_of_element(dfa_list, scores_list)))

        # Visualise every 50 generations
        if i+1 % 50 == 0:
            visualise_iterations(sorted_dfas[0])

        parent_scores_list = []
        parent_dfas = sorted_dfas[0:100]
        for dfa_model in parent_dfas:
            parent_score, parent_movement_history = run_iteration(dfa_model, number_steps=500)
            parent_scores_list.append(parent_score)
            if parent_score == 89:
                print("Score: 89")
                print("Number of moves:", len(parent_movement_history))
                print("Move history:", parent_movement_history)
                visualise_iterations(dfa_model)

        mutated_dfa_list = []
        mutant_scores_list = []
        for k in range(9):
            for dfa_model in parent_dfas:
                new_dfa = copy.deepcopy(dfa_model)

                for q in range(3):
                    if random.randint(0, 100) < 50:

                        if len(new_dfa.states) <= max_dfa_states:
                            weights = (10, 30, 60)
                        else:
                            weights = (20, 0, 80)
                        mutated_dfa = mutate_dfa2(new_dfa, weights=weights)

                        mutant_score, mutant_movement_history = run_iteration(mutated_dfa, number_steps=500)
                        if mutant_score == 89:
                            print("Score: 89")
                            print("Number of moves:", len(mutant_movement_history))
                            print("Move history:", mutant_movement_history)
                            visualise_iterations(mutated_dfa)
                        mutant_scores_list.append(mutant_score)
                        mutated_dfa_list.append(mutated_dfa)

        dfa_list = []
        scores_list = []

        for dfa_model in parent_dfas:
            dfa_list.append(dfa_model)
        for dfa_model in mutated_dfa_list:
            dfa_list.append(dfa_model)
        for score in parent_scores_list:
            scores_list.append(score)
        for score in mutant_scores_list:
            scores_list.append(score)

        average_score = sum(scores_list) / len(scores_list)

        print("average score:", average_score)
        print("best score of generation:", max(scores_list))


def run_model7(num_of_initial_mutations, num_generations, generation_size, max_dfa_states):

    scores_list = []
    mutant_scores_list = []
    parent_scores_list = []
    dfa_list = []
    print("\nGeneration Number: 0")

    for i in range(generation_size):
        dfa_model = DfaData()
        for j in range(num_of_initial_mutations):
            dfa_model = mutate_dfa2(dfa_model, weights=(10, 30, 60))
        dfa_list.append(dfa_model)
        score, history = run_iteration(dfa_model, number_steps=500)
        scores_list.append(score)

    average_score = sum(scores_list) / len(scores_list)
    print("\naverage score:", average_score)
    print("best score of generation:", max(scores_list))

    for i in range(num_generations):
        print("\nGeneration Number:", i+1)
        # Sort DFAs by score in descending order
        sorted_dfas = list(reversed(sorting_of_element(dfa_list, scores_list)))

        # Visualise every 50 generations
        #if i % 50 == 0:
        #    visualise_iterations(sorted_dfas[0])

        parent_scores_list = []
        parent_dfas = sorted_dfas[0:100]
        for dfa_model in parent_dfas:
            parent_score, parent_movement_history = run_iteration(dfa_model, number_steps=500)
            parent_scores_list.append(parent_score)
            if parent_score == 89:
                print("Score: 89")
                print("Number of moves:", len(parent_movement_history))
                print("Move history:", parent_movement_history)
                visualise_iterations(dfa_model)

        mutated_dfa_list = []
        mutant_scores_list = []
        for k in range(9):
            for dfa_model in parent_dfas:
                new_dfa = copy.deepcopy(dfa_model)

                for q in range(3):
                    if random.randint(0, 100) < 70:

                        if len(new_dfa.states) <= max_dfa_states:
                            weights=(10, 30, 60)
                        else:
                            weights=(20, 0, 80)
                        mutated_dfa = mutate_dfa2(new_dfa, weights=weights)

                        mutant_score, mutant_movement_history = run_iteration(mutated_dfa, number_steps=500)
                        if mutant_score == 89:
                            print("Score: 89")
                            print("Number of moves:", len(mutant_movement_history))
                            print("Move history:", mutant_movement_history)
                            visualise_iterations(mutated_dfa)
                        mutant_scores_list.append(mutant_score)
                        mutated_dfa_list.append(mutated_dfa)

        dfa_list = []
        scores_list = []

        for dfa_model in parent_dfas:
            dfa_list.append(dfa_model)
        for dfa_model in mutated_dfa_list:
            dfa_list.append(dfa_model)
        for score in parent_scores_list:
            scores_list.append(score)
        for score in mutant_scores_list:
            scores_list.append(score)

        average_score = sum(scores_list) / len(scores_list)

        print("average score:", average_score)
        print("best score of generation:", max(scores_list))


if __name__ == "__main__":
    run_model6(10, 600, 5000, 15)
    #visualise_dfa()