import graphviz
import matplotlib.pyplot as plt
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'


def visualise_automata(dfa):
    dot = graphviz.Digraph(comment='Automata State Diagram')
    for state in dfa.states:
        if str(state) == str(dfa.initialState):
            dot.node(str(state), "(START)  " + str(state))
        else:
            dot.node(str(state), str(state))

    for state in dfa.transitions:
        dot.edge(str(state), str(dfa.transitions[state][0][0]), label="0 / " + str(dfa.transitions[state][0][1]))
        dot.edge(str(state), str(dfa.transitions[state][1][0]), label="1 / " + str(dfa.transitions[state][1][1]))

    dot.render('test-output/round-table.gv', view=True)

