import math
import numpy as np
import my_graph

def distancias(point1: dict, point2: dict):
    dist = math.sqrt((point1['x'] - point2['x']) ** 2 + (point1['y'] - point2['y']) ** 2)
    return dist
def func_costo_TSP(nodes):
    cost_matrix = []
    rank = len(nodes)
    coord = []
    for node in nodes:
        x = nodes[node]['x']
        y = nodes[node]['y']
        coord.append(dict(x= x, y= y))
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distancias(coord[i], coord[j]))
        cost_matrix.append(row)
    return(cost_matrix, rank)
def _TSP(costo):
    costo_m, rank = costo
    print('Cost Matrix',costo_m)
if __name__ == '__main__':
    #Build the graph
    print("Building a graph..")
    file = "graph.graphml"
    node_number = 8
    my_graph.create_graph(file, node_number)

    #Reading the graph
    data_graph = my_graph.read_graph(file)
    nodes, edges = data_graph

    #TSP
    costo_TSP = func_costo_TSP(nodes)
    _TSP(costo_TSP)

'''
#distancias
    for i in dic_data:
        a = np.array(i['x'])
        b = np.array(i['y'])
        dist = np.sqrt(np.sum(np.square(a - b)))

def data_graph(path, document):
    points = []
    with open(path + document, mode='r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', "")
            links = line.split(',')
            source = int(links[0])
            target = int(links[1])
            points.append(dict(x=source, y=target))
    print(points)
    return points
'''
