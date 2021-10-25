from DarwinianModel import *


def sorting_of_element(list1, list2):
    # initializing blank dictionary
    f_1 = {}

    # initializing blank list
    final_list = []

    # Addition of two list in one dictionary
    f_1 = {list1[i]: list2[i] for i in range(len(list2))}

    # sorting of dictionary based on value
    f_lst = {k: v for k, v in sorted(f_1.items(), key=lambda item: item[1])}

    # Element addition in the list
    for i in f_lst.keys():
        final_list.append(i)
    return final_list


list1 = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
list2 = [0, 1, 1, 0, 1, 2, 2, 0, 1]


def run_model(num_of_initial_mutations, num_generations, generation_size):
    scores_list = []
    dfa_list = []

    for j in range(generation_size):
        dfa = DfaData()
        for i in range(num_of_initial_mutations):
            dfa = mutate_dfa(dfa)

        # print(dfa2.transitions)

        score, action_history = run_iteration(dfa)
        scores_list.append(score)
        # print("Agent Action History:", agentActionHistory)
        dfa_list.append(dfa)

    average_score = sum(scores_list) / len(scores_list)
    print("average score:", average_score)
    print("best of generation:", max(scores_list))

    for j in range(num_generations):

        sum_of_scores = sum(scores_list)
        if sum_of_scores == 0:
            print("Evolutions failed: best score reached 0.")
            return

        prob_dist = []
        for score in scores_list:
            prob_dist.append(score / sum_of_scores)

        next_gen_dfas = random.choices(dfa_list, weights=prob_dist, k=len(prob_dist))

        for i in range(len(next_gen_dfas)):
            for k in range(10):
                next_dfa = next_gen_dfas[i]
                next_gen_dfas[i] = mutate_dfa(next_dfa)

        scores_list = []
        dfa_list = []
        #print("generation size:", len(next_gen_dfas))
        for dfa in next_gen_dfas:
            score, action_history = run_iteration(dfa)
            scores_list.append(score)
            # print("Agent Action History:", agentActionHistory)
            dfa_list.append(dfa)

        average_score = sum(scores_list) / len(scores_list)
        print("average score:", average_score)
        print("best of generation:", max(scores_list))


def run_model2(num_of_initial_mutations, num_generations, generation_size):
    scores_list = []
    dfa_list = []

    for j in range(generation_size):
        dfa = DfaData()
        for i in range(num_of_initial_mutations):
            dfa = mutate_dfa(dfa)

        # print(dfa2.transitions)

        score, action_history = run_iteration(dfa)
        scores_list.append(score)
        # print("Agent Action History:", agentActionHistory)
        dfa_list.append(dfa)

    average_score = sum(scores_list) / len(scores_list)
    print("average score:", average_score)
    print("best of generation:", max(scores_list))

    for j in range(num_generations):

        sum_of_scores = sum(scores_list)
        if sum_of_scores == 0:
            print("Evolutions failed: best score reached 0.")
            return

        prob_dist = []
        for score in scores_list:
            prob_dist.append(score / sum_of_scores)

        next_gen_dfas = random.choices(dfa_list, weights=prob_dist, k=len(prob_dist))

        for i in range(len(next_gen_dfas)):
            next_dfa = next_gen_dfas[i]
            if random.randint(0,100) < 20:
                next_gen_dfas[i] = mutate_dfa(next_dfa)

        scores_list = []
        dfa_list = []
        #print("generation size:", len(next_gen_dfas))
        for dfa in next_gen_dfas:
            score, action_history = run_iteration(dfa)
            scores_list.append(score)
            # print("Agent Action History:", agentActionHistory)
            dfa_list.append(dfa)

        average_score = sum(scores_list) / len(scores_list)
        print("\naverage score:", average_score)
        print("best of generation:", max(scores_list))


def run_model3(num_of_initial_mutations, num_generations, generation_size):
    scores_list = []
    dfa_list = []

    for j in range(generation_size):
        dfa = DfaData()
        for i in range(num_of_initial_mutations):
            dfa = mutate_dfa(dfa)

        # print(dfa2.transitions)

        score, action_history = run_iteration(dfa)
        scores_list.append(score)
        # print("Agent Action History:", agentActionHistory)
        dfa_list.append(dfa)

    average_score = sum(scores_list) / len(scores_list)
    print("average score:", average_score)
    print("best of generation:", max(scores_list))

    for j in range(num_generations):

        sum_of_scores = sum(scores_list)
        if sum_of_scores == 0:
            print("Evolutions failed: best score reached 0.")
            return

        prob_dist = []
        for score in scores_list:
            prob_dist.append(score / sum_of_scores)

        next_gen_dfas = random.choices(dfa_list, weights=prob_dist, k=len(prob_dist))

        for i in range(len(next_gen_dfas)):
            next_dfa = next_gen_dfas[i]
            if random.randint(0,100) < (1-prob_dist[i]) * 100:
                next_gen_dfas[i] = mutate_dfa(next_dfa)


        scores_list = []
        dfa_list = []
        #print("generation size:", len(next_gen_dfas))
        for dfa in next_gen_dfas:
            score, action_history = run_iteration(dfa)
            scores_list.append(score)
            # print("Agent Action History:", agentActionHistory)
            dfa_list.append(dfa)

        average_score = sum(scores_list) / len(scores_list)
        print("\naverage score:", average_score)
        print("best of generation:", max(scores_list))


def run_model4(num_of_initial_mutations, num_generations, generation_size):
    scores_list = []
    dfa_list = []
    generation = 0
    for j in range(generation_size):
        dfa = DfaData()
        for i in range(num_of_initial_mutations):
            dfa = mutate_dfa(dfa)

        # print(dfa2.transitions)

        score, action_history = run_iteration(dfa)
        scores_list.append(score)
        # print("Agent Action History:", agentActionHistory)
        dfa_list.append(dfa)

    average_score = sum(scores_list) / len(scores_list)
    print("Generation:", generation)
    print("Best of generation:", max(scores_list))
    print("Average score:", average_score)

    for j in range(num_generations):
        generation += 1

        sum_of_scores = sum(scores_list)
        if sum_of_scores == 0:
            print("Evolutions failed: best score reached 0.")
            return

        # Sort dfa list by score
        sorted_dfas = sorting_of_element(dfa_list, scores_list)
        next_gen_dfas = sorted_dfas

        # Keeps top 20 performing dfas the same, mutate the others
        for i in range(0, len(next_gen_dfas) - 50):
            next_gen_dfas[i] = mutate_dfa(next_gen_dfas[i])

        scores_list = []
        dfa_list = []
        #print("generation size:", len(next_gen_dfas))
        for dfa in next_gen_dfas:
            score, action_history = run_iteration(dfa)
            scores_list.append(score)
            # print("Agent Action History:", agentActionHistory)
            dfa_list.append(dfa)

        average_score = sum(scores_list) / len(scores_list)
        print("\n")
        print("Generation:", generation)
        print("Best of generation:", max(scores_list))
        print("Average score:", average_score)

run_model4(10, 50, 1000)

# Add max dfa depth level at which point only changes no additions