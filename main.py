import math
import threading
import time
import qrng
import my_graph
import aco
import pandas as pd
import number_generator

def func_costo_TSP(nodes):
    #Function based on distance between points or nodes.
    #Each node has a coordinate value
    rank = len(nodes)
    cost_matr = pd.DataFrame(data=None, columns=range(rank), index=range(rank))
    coord = []
    for node in nodes:
        x = nodes[node]['x']
        y = nodes[node]['y']
        coord.append((x, y))
    for i in range(rank):
        xi, yi = coord[i][0], coord[i][1]
        for j in range(rank):
            xj, yj = coord[j][0], coord[j][1]
            if (xi == xj) & (yi == yj):
                cost_matr.iloc[i, j] = math.pow(10,10)
            else:
                cost_matr.iloc[i, j] = math.sqrt((xi -xj) **2 + (yi -yj)**2)
    return cost_matr, rank, coord
def _TSP(pheromone, alpha, beta, Q, ant_number, rank, costo_m, coord, best_fit, optimal_path, list,startTime_TSP):
    #Calculates the probability to choose a node
    probability = aco.chooseNode_probability(pheromone, alpha, beta, costo_m, Q)
    #Building two lists of nodes, initial nodes and not visit nodes based on ant number
    initial_node, not_visit_node = aco.ant_inizialization(coord, ant_number, rank)
    #Defines a fit list
    fit = [None] * ant_number
    #Inicialization of find the optimal path in the graph
    for ant in range(ant_number):
        #For each node in initial node list ant is assigned
        initial_node[ant] = aco.select_path_node(initial_node[ant], not_visit_node[ant], probability,list)
        #Estimates a fitness taking into account the assigned ant
        fit[ant] = aco.fitness_estimator(initial_node[ant], costo_m)
        #Update current ant pheromone
        pheromone = aco.update_pheromone(pheromone, fit[ant], initial_node[ant], Q)
        #Calculates the probability based on pheromona's update
        probability = aco.chooseNode_probability(pheromone, alpha, beta, costo_m, Q)
    if best_fit >= min(fit):
        best_fit = min(fit)
        #Defines the optimal path iterating initial node list searching the position of best fit in fit's list
        optimal_path = initial_node[fit.index(best_fit)]
    print('Nodes: ', coord)
    print('Path: ', optimal_path)
    print('Cost:', best_fit)
    endTime_TSP = time.time()
    total = startTime_TSP + endTime_TSP
    print('Time: ', total)
    type = 'TSP'
    #Drawing the optimal path
    aco.draw_path(optimal_path, coord, type)
def func_costo_HPP(nodes, edges):
    #This function is based on adjacency matrix (binary relation) or cost matrix to find the shortest path
    #if i = j the M[i, j] value is 0, M[i,j] represents the cost of
    #going from vertex i to vertex j.
    #For each edge that joins 2 nodes adds 1 to that place in the matrix
    nodes_aux = []
    edges_aux = []
    rank = len(nodes)
    coord = []
    for node in nodes.keys():
        nodes_aux.append(int(node))
    for node in nodes:
        x = nodes[node]['x']
        y = nodes[node]['y']
        coord.append((x, y))
    for i in edges.values():
        x = int(i[0])
        y = int(i[1])
        edge = (x, y)
        edges_aux.append(edge)
    adjacency_matrix_g = [[0 for j in range(len(nodes_aux))] for i in range(len(nodes_aux))]
    for i in range(len(adjacency_matrix_g)):
        for j in range(len(adjacency_matrix_g[i])):
            if (i + 1, j + 1) in edges_aux:
                #If exist an edge between vertix, the element of matrix is 1 otherwise 0
                adjacency_matrix_g[i][j] = 1
                adjacency_matrix_g[j][i] = 1
    cost = pd.DataFrame(adjacency_matrix_g)
    return cost, rank, coord
def _HPP(pheromone, alpha, beta, Q, ant_number, rank, costo_HPP, coord, best_fit, optimal_path, list,startTime_HPP):
    #Calculates the probability to choose a node
    probability = aco.chooseNode_probability(pheromone, alpha, beta, costo_HPP, Q)
    #Building two lists of nodes, initial nodes and not visit nodes based on ant number
    initial_node, not_visit_node = aco.ant_inizialization(coord, ant_number, rank)
    #Defines a fit list
    fit = [None] * ant_number
    #Inicialization of find the optimal path in the graph
    for ant in range(ant_number):
        #For each node in initial node list ant is assigned
        initial_node[ant] = aco.select_path_node(initial_node[ant], not_visit_node[ant], probability,list)
        #Estimates a fitness taking into account the assigned ant
        fit[ant] = aco.fitness_estimator(initial_node[ant], costo_HPP)
        #Update current ant pheromone
        pheromone = aco.update_pheromone(pheromone, fit[ant], initial_node[ant], Q)
        #Calculates the probability based on pheromona's update
        probability = aco.chooseNode_probability(pheromone, alpha, beta, costo_HPP, Q)
    if best_fit >= min(fit):
        best_fit = min(fit)
        #Defines the optimal path iterating initial node list searching the position of best fit in fit's list
        optimal_path = initial_node[fit.index(best_fit)]
    print('Nodes: ', coord)
    print('Path: ', optimal_path)
    endTime_HPP = time.time()
    total = startTime_HPP + endTime_HPP
    print('Time: ', total)
    type = 'HPP'
    #Drawing the optimal path
    aco.draw_path(optimal_path, coord, type)
if __name__ == '__main__':
    #Build the graph
    print("Building a graph..")
    file = "graph.graphml"
    node_number = 100
    my_graph.create_graph(file, node_number)
    print("Number of nodes: ", (node_number))
    print("----------------------------------------")

    #Reading the graph
    data_graph = my_graph.read_graph(file)
    nodes, edges = data_graph

    #Number Generator
    path_pseudo = "pseudo_random/pa_numbers.txt"
    path_rand = "random/q_numbers.txt"
    amount_numbers = 1000000
    print("Generating numbers")
    print("Connect to IBMQ")
    #Connection to IMBQ account
    #qrng.set_provider_as_IBMQ(
    #    '46d750be93a92ced7fce989ae6af269098f2f051ab76accf9882d6ea8483cebca9c2e5a7069db5f16e950654c9e67f463a5e95aeb7a19200579df1adac8a4461')
    #Connection to quantum computer 'ibmq_quito' with 5 qubits
    #qrng.set_backend('ibmq_quito')
    #Random and Pseudo random numbers generation
    #number_generator.generate_number(path_pseudo, path_rand, amount_numbers)

    #Read number generation files
    pseudo_list, quantum_list = number_generator.read_file(path_pseudo, path_rand)

    #Specify type of numbers to use for experiment
    type_number = "Pseudo"

    # ACO params
    alpha = 2
    beta = 1
    Q = 10.0
    ant_number = 100
    best_fit = math.pow(10, 10)
    optimal_path = []

    #TSP
    print("Travelling Salesman Problem with ACO")
    startTime_TSP = time.time()
    costo_m, rank, coord = func_costo_TSP(nodes)
    pheromone = pd.DataFrame(data=Q, columns=range(rank), index=range(rank))
    if type_number =="Random":
        tsp_thread = threading.Thread(target=_TSP(pheromone, alpha, beta, Q, ant_number, rank, costo_m, coord, best_fit, optimal_path,quantum_list,startTime_TSP))
        tsp_thread.start()
    if type_number =="Pseudo":
        tsp_thread =threading.Thread(target=_TSP(pheromone, alpha, beta, Q, ant_number, rank, costo_m, coord, best_fit, optimal_path,pseudo_list, startTime_TSP))
        tsp_thread.start()

    print("----------------------------------------")

    #HPP
    print("Hamiltonian Path Problem with ACO")
    startTime_HPP = time.time()
    costo_HPP, rank, coord = func_costo_HPP(nodes, edges)
    pheromone = pd.DataFrame(data=Q,columns=range(rank), index=range(rank))
    if type_number =="Random":
        hpp_thread = threading.Thread(target=_HPP(pheromone, alpha, beta, Q, ant_number, rank, costo_HPP, coord, best_fit, optimal_path,quantum_list,startTime_HPP))
        hpp_thread.start()
    if type_number =="Pseudo":
        hpp_thread = threading.Thread(target=_HPP(pheromone, alpha, beta, Q, ant_number, rank, costo_HPP, coord, best_fit, optimal_path,pseudo_list, startTime_HPP))
        hpp_thread.start()
