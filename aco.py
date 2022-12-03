import numpy as np
import random
import number_generator
from matplotlib import pyplot as plt

def chooseNode_probability(pheromone, alpha,beta, cost_matrix, Q):
    #Probability to choose a node based in pheromone
    #Pheromone value represents the actual pheromone
    #Alpha is the pheromone importance
    #Q is a constant
    #Cost_matrix represents the LK factor
    probability = Q / cost_matrix
    final_prob = probability.replace(np.inf,0)
    for i in range(len(final_prob)):
        for j in range(len(final_prob)):
            final_prob.iloc[i, j] = pow(pheromone.iloc[i, j], alpha) * pow(final_prob.iloc[i, j], beta)
    return final_prob
def ant_inizialization(coord, ant_number, rank):
    #Initial ant format
    initial_node, not_visit_node = [None] * ant_number, [None]*ant_number
    for i in range(rank):
        node = random.randint(0, rank-1)
        initial_node[i] = [node]
        not_visit_node[i] = list(range(rank))
        not_visit_node[i].remove(node)
    return initial_node, not_visit_node
def select_path_node(initial_node, not_visit_node, probability,list):
    #Initial node complete path
    next_node = 0
    while len(not_visit_node) > 0:
        if len(not_visit_node) == 1:
            next_node = not_visit_node[0]
        else:
            fit = []
            for i in not_visit_node: fit.append(
                probability.loc[initial_node[-1], i])  # Take out the node transfer probability corresponding to not visit node
            #Linking pseudo and random numbers generation
            q = number_generator.queue_number(list)
            for i in range(len(q)):
                rand_numb = q.pop()
                accumulator = 0.0
                for i, ele in enumerate(fit):
                    accumulator += ele
                    aux = (rand_numb*10)/accumulator
                    if (rand_numb*10) == 0 and accumulator == 0:
                        next_node = random.choice(not_visit_node)
                    if accumulator >= aux:
                        next_node = not_visit_node[i]
                        break
        initial_node.append(next_node)
        not_visit_node.remove(next_node)
    return initial_node
def fitness_estimator(initial_node, cost_m):
    #Calculate the path's cost
    total = 0
    for i in range(len(initial_node)-1):
        total_aux = cost_m.loc[initial_node[i], initial_node[i+1]] #distance of path
        total = total + total_aux
    total_aux = cost_m.loc[initial_node[-1], initial_node[0]]
    total = total + total_aux
    return round(total, 3)
def update_pheromone(pheromone, fit, initial_node, Q):
    #Update actual pheromone
    for i in range(len(initial_node)-1):
        pheromone.iloc[initial_node[i], initial_node[i+1]] += Q/fit
    pheromone.iloc[initial_node[-1], initial_node[0]] += Q/fit
    return pheromone
def draw_path(optimal_path, nodes, type):
    x, y = [], []
    for node in optimal_path:
        Coord = nodes[node]
        x.append(Coord[0])
        y.append(Coord[1])
    x.append(x[0])
    y.append(y[0])

    plt.plot(x, y, 'r-', color='#4169E1', alpha=0.8, linewidth=0.8)
    if type == 'HPP':
        plt.title('HPP with ACO')
    else:
        plt.title('TSP with ACO')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
