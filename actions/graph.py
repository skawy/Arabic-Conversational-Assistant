# from collections import defaultdict
# from FCAI_DB import FCAI_DB
#
#
# class Graph:
#     def __init__(self, rows):
#         self.graph = defaultdict(list)
#         self.add_node(rows)
#         self.visited = [False] * len(self.graph)
#         self.num_nodes = len(self.graph)
#
#     def add_edge(self, node1, node2):
#         self.graph[node1].append(node2)
#
#     def add_node(self, rows):
#         for i in rows:
#             self.add_edge(i[1], i[0])
#
#     def bfs(self, start, goal):
#         explored = []
#         queue = [[start]]  # add start node to queue
#         if start == goal:  # Check if start equal node
#             print("Same Node")
#             return "Same Node"
#
#         # Loop to traverse the graph
#         # with the help of the queue
#         while queue:
#             path = queue.pop(0)  # get first element of queue
#             node = path[-1]  # node equal last element in path
#
#             # Condition to check if the
#             # current node is not visited
#             if node not in explored:
#                 neighbours = self.graph[node]  # get values of this node
#                 # Loop to iterate over the
#                 # neighbours of the node
#                 for neighbour in neighbours:
#                     new_path = list(path)
#                     new_path.append(neighbour)  # add neighbour to new path
#                     queue.append(new_path)
#                     # check if goal is reached return shortest path
#                     if neighbour == goal:
#                         print("Shortest path = ", *new_path)
#                         return new_path
#                 explored.append(node)  # add visited node
#
#
# fcai = FCAI_DB()
# row = fcai.print_tables('programming')
# g = Graph(row)
#
#
# x = g.bfs('CS', 'DS')
# print(x)
