# CSE 551 Programming Assignment – Spring’21 [Funny Problem]

Problem: 
To determine whether there are m-vertex disjoint paths from the starting points to any m distinct points in the boundary. 

Steps to run the project:

pip install numpy
pip install scipy
python '.\Programming_aasignment_Problem.py'


Note: The input for the project needs to be mentioned in Datasets>dataset1.txt
You can also change the dataset file name at Line 120 in Programming_aasignment_Problem.py 

Problem Description:

Fact: 
Two paths from vertex u to vertex v are said to be vertex disjoint if they do not contain any common internal vertex in them.


Solution: 

Let’s take an example with a network, G=(V, E) with vertex capacity as d: V -> R and edge capacities as c: E-> R.
For every v ∈ V, we need ∑_(u∈V)〖{f(u,v)│f(u,v)>0}≤d(v)〗

To solve the problem, we can use Maximum Flow algorithm. We need to convert the given ‘Funny Problem’ to Single Source – Single Sink Maximum Flow Path. This problem can be reduced to network flow problem with each vertex having unit capacity of 1. 
We would add source vertex s and destination vertex t to the grid. We will connect s to each of the m starting points and we will connect t to every boundary point on the grid. Every edge from the source and every edge to the sink will have the capacity as 1. 
The solution to the funny problem is equivalent to the answer of whether there is a maximum flow of value at least m in the given network. 
By applying the below algorithm, we can reduce this problem to vertex capacities to a traditional flow problem with edge capacities in linear time. These computations, along with the flow back to the grid provides the vertex disjoint paths for this problem.
We create a new flow network here, G^'=(V^',〖 E〗^') with edge capacities such that for every maximum flow in G would correspond to a maximum flow in G^'. Let the edge capacity of G^' be c^' : E^' -> R.

We will use Edmond-Karp algorithm here to calculate the maximum flow. Edmond-Karp is the implementation of Ford-Fulkerson method that uses BFS (Breadth First Search) to find augmented paths. 

Implementation algorithm:

	Add two additional vertices for source, s and sink, t
	For each vertex u in the set of starting vertices for this problem(Total starting points = m), add edge from s to u with capacity as 1
	Split each vertex v ∈ V in the graph into two vertices : v_in and v_out (except source s and sink t)
	For each vertex v, add an edge from v_in to v_out with unit capacity of 1.
Therefore, V^' = {v_in,v_out  | v ∈ V},
〖 E〗^'={(u_out,v_in )  ┤|(u,v)  ∈E} ∪{(v_in,v_out )| v ∈ V}
c^' (u_out,v_in )=c(u,v),for every (u,v)  ∈E 
c^' (v_in,v_out )=d(v),for every (v)  ∈V 

	For each of the grid boundary vertices v (Total boundary points = 4n – 4), add an edge from v_out  to t with unit capacity of 1. [Any undirected edge (u, v) in original network G is now replaced by two directed edges (v_out, v_in)  and (v_in, v_out). Therefore, any flow through the original network satisfying vertex capacities corresponds to a flow with the same value in the new network, satisfying edge capacities. It is computable in linear time.]
	Ensure that for every edge in graph G, the edge capacity = 1, and for every vertex, the vertex capacity = 1
	Maximum Flow from s-t is calculated using Edmonds-Karp Algorithm
	s-t max-flow would give the maximum number of s-t vertex disjoint paths
	If Maximum s-t flow = |V|, where V is set of vertices in the set, (m in this case), then all the vertices in V can reach the boundary vertices in grid using vertex disjoint paths  and there is a solution to this ‘funny’ problem.
	The maximum flow can’t be greater than the value of m by looking at the cut which has s by itself.
	If Maximum Flow value is less than m, then there is no solution which exists for the given network, because otherwise we could construct a flow with value m from the list of disjoint paths that are the ideal path solutions for the problem.


Complexity of the algorithm:

Cost of splitting vertex V into two vertices v_in and v_out to obtain V^'  is O(V) and cost of adding extra edges from vertices v_in to v_out  and assigning it the capacity d(v), repeated |V| times in also O(V). 
Modified vertex and edge sets in the maximum-flow network, 
|V^'| = 2.|V|
|E^'| = |E| + |V|
Cost of implementing Ford-Fulkerson Method algorithm for maximum flow on  G^' = O (E^'.|f^*|) = O((E + V) .|f^*|), where f^* is the maximum flow, provided the capacities are of integral values (unit value in this case).
After running Edmonds-Karp implementation on G^', the running time is O (V^' E^'2).
Total complexity = Graph Modification Cost + Max Flow Algorithm Cost 
		        = O (V) + O (V^' E^'2) = O (V^' E^'2)	
		        = O (2.V. 〖(E+V)〗^2)		[The complexity might vary depending on the selection of the max-flow algorithm]
Based on the input size for this problem, the complexity can have a tighter bound. As the input grid has n^2 points and 2n^2 – 2n undirected edges, the original network G would have 2 + n^2 = O(n^2) vertices and m + (4n-4) + 2(2n^2-2n) = m + 4n^2 – 4 = O(n^2) directed edges. Therefore, the running time using Edmonds-Karp implementation would be O (VE^2) = O(n^6). 
Now, upper bound for Ford-Fulkerson based algorithms = O((E + V) .|f^*|), where f^* is the maximum flow. In this problem, |f^*| ≤4n-4 and |E| + |V| = O(n^2)
Therefore, the tighter bound for the overall complexity = O((E + V) .|f^*|) = O(n^3)
