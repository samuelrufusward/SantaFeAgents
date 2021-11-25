import random
import copy
from multiprocessing import Pool
from DarwinianModel import generate_trail, generate_dfa, mutate_dfa, run_iteration, crossover_automata, add_state, change_start, change_transition, delete_state
from GraphVisualisation import visualise_automata
import numpy as np
import pygame
import matplotlib.pyplot as plt
import time

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

    for i in range(600):

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
            return

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


def run_model(initial_dfa_size, num_generations, generation_size, max_dfa_states, number_steps=600):
    performance_dict = {}
    scores_list = []
    best_dfa = None
    mutant_scores_list = []
    parent_scores_list = []
    best_score_of_generations = []
    average_scores = []
    dfa_list = []
    converged = False
    print("\nGeneration Number: 0")

    for i in range(generation_size):
        dfa_model = generate_dfa(number_states=initial_dfa_size)
        dfa_list.append(dfa_model)
        score, history = run_iteration(dfa_model, number_steps=number_steps)
        scores_list.append(score)
        performance_dict[copy.deepcopy(dfa_model)] = [score, number_steps - len(history)]
    #print("performance dict:", performance_dict)

    average_score = sum(scores_list) / len(scores_list)
    #print("\naverage score:", average_score)
    #print("best score of generation:", max(scores_list))

    for i in range(num_generations):
        print("\nGeneration Number:", i+1)
        # Sort DFAs by score in descending order
        sorted_dfas_dict = {k: v for k, v in sorted(performance_dict.items(), key=lambda item: item[1])}
        #print("sorted dfa dict:", sorted_dfas_dict)
        sorted_dfas = list(reversed(list(sorted_dfas_dict.keys())))
        # Reset DFA performance dictionary
        performance_dict = {}
        best_score_of_generations.append(max(scores_list))
        # Visualise every 50 generations
        #if i % 30 == 0 and i > 5:
        #if converged:
            #visualise_iterations(sorted_dfas[0])
            #visualise_automata(sorted_dfas[0])

        best_dfa = sorted_dfas[0]
        parent_scores_list = []
        parent_dfas = sorted_dfas[0:50]
        for dfa_model in parent_dfas:
            parent_score, parent_movement_history = run_iteration(dfa_model, number_steps=number_steps)
            parent_scores_list.append(parent_score)
            performance_dict[copy.deepcopy(dfa_model)] = [parent_score, number_steps - len(parent_movement_history)]
            if parent_score == 89:
                converged = True
                #print("\nScore: 89")
                #print("Number of moves:", len(parent_movement_history))
                #print("Move history:", parent_movement_history)
                #print("Number of states:", len(dfa_model.states))
                #visualise_automata(dfa_model)
                #visualise_iterations(dfa_model)

        mutated_dfa_list = []
        mutant_scores_list = []
        for k in range(19):
            for dfa_model in parent_dfas:
                new_dfa = copy.deepcopy(dfa_model)

                if random.randint(0, 100) < 100:
                    for q in range(4):
                        if len(new_dfa.states) <= max_dfa_states:
                            weights=(10, 25, 60, 5)
                        else:
                            weights=(10, 0, 60, 5)
                        mutate_dfa(new_dfa, weights=weights)

                    mutant_score, mutant_movement_history = run_iteration(new_dfa, number_steps=number_steps)
                    if mutant_score == 89:
                        converged = True
                        #print("\nScore: 89")
                        #print("Number of moves:", len(mutant_movement_history))
                        #print("Move history:", mutant_movement_history)
                        #print("Number of states:", len(new_dfa.states))
                        #visualise_automata(new_dfa)
                        #visualise_iterations(new_dfa)
                    mutant_scores_list.append(mutant_score)
                    mutated_dfa_list.append(new_dfa)
                    performance_dict[copy.deepcopy(new_dfa)] = [mutant_score, number_steps - len(mutant_movement_history)]

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
        average_scores.append(average_score)

        #print("average score:", average_score)
        #print("best score of generation:", max(scores_list))
        #print("performance dict:", performance_dict)

    return best_score_of_generations, average_scores, converged, best_dfa


def plot_four_runs_on_same_figure():

    best_scores_list = []
    gens_to_converge_list = []

    for i in range(4):
        best_scores, average_scores, converged, best_dfa = run_model(4, 100, 1000, 5)

        score, action_history = run_iteration(best_dfa)
        number_of_moves = len(action_history)

        print("score:", score)
        print("no moves:", number_of_moves)
        visualise_automata(best_dfa)

        number_of_generations_to_converge = len([j for j in best_scores if j < 89]) + 1

        print("Number of generations to converge:", number_of_generations_to_converge)

        print(best_scores)

        best_scores_list.append(best_scores)
        gens_to_converge_list.append(number_of_generations_to_converge)

    generations = [i for i in range(0, 100)]
    plt.plot(generations, best_scores_list[0], 'g-', linewidth=2, alpha=0.7)
    plt.plot(generations, best_scores_list[1], 'b-', linewidth=2, alpha=0.7)
    plt.plot(generations, best_scores_list[2], 'y-', linewidth=2, alpha=0.7)
    plt.plot(generations, best_scores_list[3], 'm-', linewidth=2, alpha=0.7)
    plt.plot(generations, [89] * len(generations), 'r:', linewidth=3)
    plt.xlabel('Generation Number')
    plt.ylabel('Best of Generation Score')
    plt.title("Best of Generation Score over 100 Generations for Four Simulation Runs")
    plt.legend(['Iteration 1', 'Iteration 2', 'Iteration 3', 'Iteration 4', 'Optimal Score (89)'])
    plt.show()


def plot_best_score_over_generations():
    fig, axs = plt.subplots(2, 2)

    generations = [i for i in range(0, 100)]

    for i in range(2):
        for j in range(2):
            best_scores, average_scores, converged, best_dfa = run_model(4, 100, 1000, 6)

            score, action_history = run_iteration(best_dfa)
            number_of_moves = len(action_history)

            print("score:", score)
            print("no moves:", number_of_moves)
            visualise_automata(best_dfa)

            number_of_generations_to_converge = len([j for j in best_scores if j < 89]) + 1

            print("Number of generations to converge:", number_of_generations_to_converge)

            print(best_scores)

            axs[i, j].plot(generations, best_scores, linewidth=3)

            axs[i, j].plot(generations, [89]*len(generations), 'r:', linewidth=3)

    for ax in axs.flat:
        ax.set(xlabel='Generation', ylabel='Best Score')

    plt.legend(['Score', 'Optimal Score (89)'])
    plt.show()


def plot_average_best_score_over_generations(maxStates=5, numIterations=100):
    best_scores_list = []
    average_scores_list = []
    num_converged = 0
    generations_to_converge_list = []
    for i in range(numIterations):
        best_scores, average_scores, converged, best_dfa = run_model(4, 100, 1000, maxStates-1)
        best_scores_list.append(best_scores)
        average_scores_list.append(average_scores)
        if converged:
            num_converged += 1
            number_of_generations_to_converge = len([j for j in best_scores if j < 89]) + 1
            generations_to_converge_list.append(number_of_generations_to_converge)

    average_num_generations_to_converge = sum(generations_to_converge_list) / len(generations_to_converge_list)
    proportion_that_converged = num_converged / numIterations

    print("average number of generations to converge:", average_num_generations_to_converge)
    print("proportion that converged:", proportion_that_converged)

    summed_best_scores = np.zeros(100)
    summed_average_scores = np.zeros(100)

    for i in range(100):
        for scores in best_scores_list:
            summed_best_scores[i] += scores[i]
        for scores in average_scores_list:
            summed_average_scores[i] += scores[i]

    #print("summed scores:", summed_best_scores)

    best_scores_average = []
    average_scores_mean = []
    for i in range(100):
        best_scores_average.append(summed_best_scores[i] * (1 / numIterations))
        average_scores_mean.append(summed_average_scores[i] * (1 / numIterations))

    print("Best Scores Mean: ", best_scores_average)
    print("Average Scores Mean: ", average_scores_mean)

    # Write results to text file
    with open('statistics_output.txt', 'a') as f:
        f.write("\n ===Max" + str(maxStates) + " States===")
        f.write("\nBest Scores (Average): " + str(best_scores_average))
        f.write("\nMean Scores (Average): " + str(average_scores_mean))
        f.write("\nAverage Number of Generations to Converge: " + str(average_num_generations_to_converge))
        f.write("\nProportion that Converged: " + str(proportion_that_converged))
        f.close()

    generations = [i for i in range(0, 100)]

    plt.plot(generations, best_scores_average, 'b-', linewidth=4)
    plt.plot(generations, average_scores_mean, 'g-', linewidth=4)
    plt.plot(generations, [89] * len(generations), 'r:', linewidth=3)
    plt.legend(['Best Score', 'Mean Score', 'Optimal Score (89)'])
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.title('Averaged Generational Scores for 100 Simulation Runs (Maximum {} DFA States)'.format(maxStates))
    plt.show()


def plot_average_best_score_over_generations_same_axis():
    max6states_best_scores_mean =\
                      [11.0, 39.86, 48.15, 56.43, 62.33, 65.94, 68.1, 70.94, 74.11, 75.35000000000001, 76.46000000000001,
                      77.5, 78.07000000000001, 79.17, 79.64, 80.31, 80.86, 81.35000000000001, 81.62, 81.99, 82.52,
                      82.57000000000001, 82.7, 83.01, 83.03, 83.27, 83.49, 83.67, 83.74, 83.91, 84.15, 84.25, 84.27,
                      84.52, 84.55, 84.7, 84.7, 84.91, 84.91, 84.94, 85.07000000000001, 85.33, 85.33, 85.53, 85.61,
                      85.69, 85.7, 85.94, 85.94, 85.94, 85.94, 85.95, 86.02, 86.02, 86.02, 86.02, 86.02, 86.09, 86.09,
                      86.13, 86.13, 86.21000000000001, 86.48, 86.59, 86.59, 86.59, 86.72, 86.73, 86.73, 86.73, 86.73,
                      86.73, 86.73, 86.73, 86.73, 86.75, 86.77, 86.77, 86.77, 86.94, 86.94, 86.94, 86.94, 86.94, 86.95,
                      86.95, 86.95, 86.95, 86.96000000000001, 86.96000000000001, 86.96000000000001, 86.96000000000001,
                      86.96000000000001, 86.97, 86.97, 86.97, 86.97, 86.97, 86.97, 86.97]

    max10states_best_scores_mean =\
        [11.0, 38.08, 47.43, 57.83, 64.73, 70.61, 73.54, 75.84, 76.88, 77.87, 78.53, 80.27, 81.4, 82.14, 82.56, 83.11,
         83.60000000000001, 83.8, 84.02, 84.14, 84.17, 84.37, 84.78, 85.02, 85.15, 85.28, 85.28, 85.53, 85.63, 85.75,
         85.87, 85.92, 86.01, 86.01, 86.01, 86.15, 86.17, 86.18, 86.51, 86.62, 86.66, 86.67, 86.92, 86.96000000000001,
         86.96000000000001, 86.99, 86.99, 86.99, 87.01, 87.01, 87.07000000000001, 87.15, 87.15, 87.19, 87.19, 87.19,
         87.19, 87.37, 87.37, 87.37, 87.37, 87.37, 87.44, 87.44, 87.49, 87.60000000000001, 87.61, 87.64, 87.64,
         87.71000000000001, 87.71000000000001, 87.78, 87.79, 87.82000000000001, 87.83, 87.83, 87.83, 87.83, 87.83,
         87.83, 87.83, 87.83, 87.83, 87.83, 87.83, 87.83, 87.83, 87.83, 87.83, 87.83, 87.83, 87.83, 87.85000000000001,
         87.85000000000001, 87.85000000000001, 87.85000000000001, 87.85000000000001, 87.85000000000001,
         87.85000000000001, 87.9]

    max14states_best_scores_mean =\
        [11.0, 37.910000000000004, 47.800000000000004, 58.4, 64.45, 69.94, 72.76, 75.61, 76.87, 77.74, 78.44, 79.45,
         80.34, 81.2, 81.81, 82.29, 82.88, 83.2, 83.52, 83.69, 84.14, 84.23, 84.44, 84.57000000000001, 84.75, 84.94,
         85.04, 85.12, 85.46000000000001, 85.54, 85.57000000000001, 85.65, 85.71000000000001, 85.76, 85.82000000000001,
         85.82000000000001, 85.88, 85.95, 86.10000000000001, 86.13, 86.16, 86.26, 86.3, 86.34, 86.36, 86.36, 86.54,
         86.55, 86.56, 86.56, 86.58, 86.58, 86.58, 86.59, 86.59, 86.60000000000001, 86.7, 86.71000000000001, 86.87,
         86.89, 86.89, 86.89, 86.89, 86.89, 86.89, 86.89, 86.89, 86.89, 86.9, 86.9, 86.9, 86.9, 86.9, 86.9, 87.02,
         87.02, 87.02, 87.05, 87.05, 87.06, 87.17, 87.17, 87.17, 87.17, 87.17, 87.17, 87.25, 87.29, 87.29, 87.29, 87.3,
         87.3, 87.3, 87.3, 87.3, 87.31, 87.31, 87.31, 87.31, 87.31]

    generations = [i for i in range(0, 100)]

    plt.plot(generations, max6states_best_scores_mean, linewidth=2)
    plt.plot(generations, max10states_best_scores_mean, linewidth=2)
    plt.plot(generations, max14states_best_scores_mean, linewidth=2)
    plt.plot(generations, [89] * len(generations), 'r:', linewidth=3)
    plt.legend(['Max 6 States', 'Max 10 States', 'Max 14 States', 'Optimal Score (89)'])
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.title('Mean Best Score of Generation for 100 Simulations')
    plt.show()


def plot_known_solution():
    dfa = generate_dfa()
    dfa.states = ["q0", "q1", "q2", "q3", "q4"]
    dfa.transitions = {"q0": {0: ["q1", "tr"], 1: ["q0", "m"]},
                       "q1": {0: ["q2", "tr"], 1: ["q0", "m"]},
                       "q2": {0: ["q3", "tr"], 1: ["q0", "m"]},
                       "q3": {0: ["q4", "tr"], 1: ["q0", "m"]},
                       "q4": {0: ["q0", "m"], 1: ["q0", "m"]}}
    score, history = run_iteration(dfa)
    print("Score:", score)
    print("Number Moves:", len(history))
    visualise_automata(dfa)


def plot_optimal_solution():
    best_scores, average_scores, converged, best_dfa = run_model(4, 100, 1000, 8)
    print("Converged?" + str(converged))
    score, history = run_iteration(best_dfa)
    #visualise_iterations(best_dfa)
    print("Number of moves:", len(history))
    visualise_automata(best_dfa)


def plot_example_automata():
    automata = generate_dfa(number_states=2)
    automata.states = ['q0', 'q1', 'q2']
    automata.transitions = {'q0': {0: ['q1', 'tr'], 1: ['q0', 'm']},
                            'q1': {0: ['q2', 'tr'], 1: ['q1', 'm']},
                            'q2': {0: ['q0', 'tl'], 1: ['q2', 'm']}}
    visualise_automata(automata)


def plot_example_add_state():
    automata = generate_dfa(number_states=2)
    automata.states = ['q0', 'q1', 'q2']
    automata.transitions = {'q0': {0: ['q1', 'tr'], 1: ['q0', 'm']},
                            'q1': {0: ['q2', 'tr'], 1: ['q1', 'm']},
                            'q2': {0: ['q0', 'tl'], 1: ['q2', 'm']}}
    add_state(automata)
    visualise_automata(automata)


def plot_example_change_transition():
    automata = generate_dfa(number_states=2)
    automata.states = ['q0', 'q1', 'q2']
    automata.transitions = {'q0': {0: ['q1', 'tr'], 1: ['q0', 'm']},
                            'q1': {0: ['q2', 'tr'], 1: ['q1', 'm']},
                            'q2': {0: ['q0', 'tl'], 1: ['q2', 'm']}}
    change_transition(automata)
    visualise_automata(automata)


def plot_example_delete_state():
    automata = generate_dfa(number_states=2)
    automata.states = ['q0', 'q1', 'q2']
    automata.transitions = {'q0': {0: ['q1', 'tr'], 1: ['q0', 'm']},
                            'q1': {0: ['q2', 'tr'], 1: ['q1', 'm']},
                            'q2': {0: ['q0', 'tl'], 1: ['q2', 'm']}}
    delete_state(automata)
    visualise_automata(automata)


def plot_example_change_start():
    automata = generate_dfa(number_states=2)
    automata.states = ['q0', 'q1', 'q2']
    automata.transitions = {'q0': {0: ['q1', 'tr'], 1: ['q0', 'm']},
                            'q1': {0: ['q2', 'tr'], 1: ['q1', 'm']},
                            'q2': {0: ['q0', 'tl'], 1: ['q2', 'm']}}
    change_start(automata)
    visualise_automata(automata)


def plot_basic_automata():
    automata = generate_dfa(number_states=2)
    visualise_automata(automata)


if __name__ == "__main__":
    #run_model2(4, 600, 1000, 5)
    #plot_basic_automata()
    #plot_average_best_score_over_generations(maxStates=14, numIterations=100)
    #plot_best_score_over_generations()
    #plot_optimal_solution()
    #plot_average_best_score_over_generations_same_axis()
    #plot_best_score_over_generations()
    #plot_known_solution()
    #plot_four_runs_on_same_figure()
    for i in range(100):
        run_model(4, 100, 1000, 5)
