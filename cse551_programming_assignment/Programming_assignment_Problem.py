# FUNNY problem

import os
import numpy as numpy
import math
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import breadth_first_order

# ============================================================================ #
# @brief print_Paths: This function is used to print the paths in the network flow.
#         Here, we need to convert the nodes in graph, say node, 0<=node<=73 to the 
#         disjoint vertices in grid, say v(x, y) such that 1 <= x, y <= n
# @param list_path: The list of the paths in the graph
# @param grid_dim: The dimension of the grid, say n
# @return: None
# ============================================================================ #
def print_Paths(list_path, grid_dim):
    for path in list_path:
        i = 1
        
        #ignoring the last path which is a path from sink to sink
        if path != list_path[-1]:
            print("PATH from", end = " ")
        
        #ignoring first and last element in the list which corresponds to source and sink
        #running the loop from 1 to n -1, where n is length of the path list  
        while i < (len(path) - 1):
            x = math.ceil((path[i])/(2* grid_dim) )
            y = math.ceil(((path[i])/2) % grid_dim)
            
            #Conditions to print in the desired output format
            if i == 1:
                print(f"{x, y} :", end = " ")
            
            #Incrementing i by 2 to skip one of vin or vout node    
            i += 2
            
            #Conditions to print in the desired output format
            if i < (len(path) - 1):
                print (f"{x, y}", end = " -> ")
            else:
               print (f"{x, y}") 
            
            
# ============================================================================ #
# @brief calculate_max_flow: This function is used to calculate maximum flow of the network graph
# @param G: Graph
# @param s: Source
# @param t: Sink
# @return: Max Flow 
# ============================================================================ #
def calculate_max_flow(G, s, t):
    flow = 0
    src, sink = s, t
    list_of_path = []
    j = sink
    val = [sink]

    #Performing BFS using STL from scipy
    node_graph, ps = breadth_first_order(csr_matrix(G), 0, directed=True, return_predecessors=True)
    
    # calculate paths from source to sink
    while ps[j] != -9999:
        val.append(ps[j])
        j = ps[j]

    minimum_path = val[::-1]
    list_of_path.append(minimum_path)
    # print("augmented_path")
    # print(minimum_path)

    while src in minimum_path:
        minimum_value = numpy.inf

        #find capacity of bottleneck edge
        for i in range(1, len(minimum_path)):
            start_index, end_index = minimum_path[i - 1], minimum_path[i]
            if G[start_index][end_index] < minimum_value:
                minimum_value = G[start_index][end_index]

        bneckEdge = minimum_value
        flow += bneckEdge
        # print("bottleneckEdge")
        # print(bneckEdge)
        temp_Graph = G

        for i in range(1, len(minimum_path)):
            start_index, end_index = minimum_path[i - 1], minimum_path[i]
            temp_Graph[start_index][end_index] -= bneckEdge
            temp_Graph[end_index][start_index] += bneckEdge

        G = temp_Graph
        # print("temp_Graph")
        # print(temp_Graph)

        node_graph, ps = breadth_first_order(csr_matrix(G), 0, directed=True, return_predecessors=True)
        j = sink
        val = [sink]
        while ps[j] != -9999:
            val.append(ps[j])
            j = ps[j]

        minimum_path = val[::-1]
        list_of_path.append(minimum_path)
        # print("augmented_path")
        # print(minimum_path)
    return flow, list_of_path

# ============================================================================ #
# @brief createGridVertices: This function is used to create the matrix for the network graph
# @param grid_dim: The dimendion n for the grid
# @param startingVertices: The list of starting vertices
# ============================================================================ #
def createGridVertices(grid_dim, startingVertices):
    # Total number of nodes = grid_dim * grid_dim * 2 + 2 [Total nodes in the grid i.e. grid_dimension * grid_dimension divided into two nodes vin and vout + source node and sink node]
    G = grid_dim * grid_dim * 2 + 2
    node = numpy.zeros((G, G), dtype=numpy.int64)
    path_list = []

    # Vin-Vout edges changed to unit capacity that is 1
    for i in range(1, grid_dim * grid_dim * 2, 2):
        node[i][i + 1] = 1

    # Sides for Sink node (Upper, Lower)
    for i in range(1, grid_dim + 1):
        node[2 * i][G - 1] = 1
        node[2 * (grid_dim - 1) * grid_dim + 2 * i][G - 1] = 1

    # Sides for Sink node (left, right)
    for i in range(grid_dim):
        node[i * 2 * grid_dim + 2][G - 1] = 1
        node[2 * grid_dim * (i + 1)][G - 1] = 1

    # Source to given vertices in the graph (S to Vin)
    for i in startingVertices:
        node[0][(i[0] - 1) * 2 * grid_dim + (2 * (i[1] - 1)) + 1] = 1

    # From each vertex to its neighbour vertices (Right neighbours)
    for i in range(2, grid_dim * grid_dim * 2 + 1, 2):
        if i % (2 * grid_dim) != 0:
            node[i][i + 1] = 1

    # From each vertex to its neighbour vertices (Left neighbours)
    for i in range(2, grid_dim * grid_dim * 2 + 1, 2):
        if (i - 2) % (2 * grid_dim) != 0:
            node[i][i - 3] = 1

    # From each vertex to its neighbour vertices (above neighbours)
    for i in range(2, grid_dim * grid_dim * 2 + 1, 2):
        if i - (2 * grid_dim) > 0:
            node[i][i - (2 * grid_dim) - 1] = 1

    # From each vertex to its neighbour vertices (below neighbours)
    for i in range(2, grid_dim * grid_dim * 2 + 1, 2):
        if i + (2 * grid_dim) < grid_dim * grid_dim * 2 + 1:
            node[i][i + (2 * grid_dim) - 1] = 1

    # print("node: ")
    # print(node)
    max_flow, path_list = calculate_max_flow(node, 0, G - 1)

    return max_flow, path_list

# ============================================================================ #
# Main Function
# ============================================================================ #
if __name__ == '__main__':
    arr = []
    path_list = []
    file_path = os.path.join(os.curdir, r"Datasets\dataset1.txt")
    # file_path = os.path.join(os.curdir, r"Datasets\dataset2.txt")
    with open(file_path) as f:
        for line_in_file in f:
            arr.append((map(int, line_in_file.strip().split())))

    grid1, grid2, total_count = arr[0]
    grid_dim = grid1
    if grid1 != grid2:
        print ("The grid dimensions are invalid. It is not a square grid")
    else:
        startingVertices = []
        for k in range(total_count):
            x, y = arr[k + 1]
            startingVertices.append((x, y))
        # print (startingVertices)

        final_flow, path_list = createGridVertices(grid_dim, startingVertices)
        print (f"Maximum Flow:  {final_flow}")
        # print (f"path_list:  {path_list}")        
        ln = len(startingVertices)
        print (f"len(startingVertices):  {ln}")
        if final_flow == len(startingVertices):
            print ("Yes, the solution exists")
            print_Paths(path_list, grid_dim)
        else:
            print ("No, there exists no solution to this problem")
        
