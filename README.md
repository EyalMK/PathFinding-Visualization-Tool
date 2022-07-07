# PathFinding-Visualization-Tool

This project is based on the A* path finding algorithm and its goal is to visualize it.

                                                    - The Algorithm -
The A* algorithm is based on nodes. A path has a start node and an end node. For each 'optimal' next node and its distance, we keep track of them
with an open set (as a queue). The distance will be determined by the 'F' score [F(n) = G(n) + H(n)].
H(n) - estimation of the distance from node n to the end node.
G(n) - current shortest distance from start node to node n.
Therefore - F(n) is the estimate of the start node to end node.

We start from the start node and look at the nearest neighbor node. We look at the edge and check the distance/the current path and we
compare it to the previous G(n) score, and we update it accordingly, we update the F score, save this path as the first neighbor node and its F score to the open set.
And then after finding the shortest path to the neighbor node, we check the shortest path to the next neighbor node and we repeat.
After considering all paths, we check the open set for the lowest F score.
The algorithm is finished.
At this point we find the path and backtrack. End node with the lowest F score came from the previous node T, node T came from node S and so on and so forth.

                                                   - The Visualization -
We will visualize the path finding with PyGame and it is the only prerequisite.
We will use colors to denote the status of each node, comments can be found in AStar.py above the class declaration.
It is best to find an alternative to colors, which will happen at later stages.
