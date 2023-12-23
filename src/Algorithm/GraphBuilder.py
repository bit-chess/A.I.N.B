from collections import deque
from typing import List

class GraphBuilder:
    def __init__(self):
        self.maxn = 10000010
        self.graph = [[] for _ in range(self.maxn)]  # Grafo NÓSxARESTA
        self.nodes_pos = []  # Lista com as coordenadas das peças
        self.node_weights = [0] * self.maxn
        self.depth_node = [0] * self.maxn  # profundidades dos nós
        self.count_nodes = 1

    def createGraph(self, c):
        # graph[0].append(0)
        self.nodes_pos.append(c)
        self.depth_node[0] = 0

    def create_graph(self, node_father, u):
        if node_father == -1:
            return
        for i in range(len(u)):
            self.nodes_pos.append(u[i])
            self.graph[node_father].append(self.count_nodes)
            self.depth_node[self.count_nodes] = self.depth_node[node_father] + 1
            self.count_nodes += 1


    def createGraphFromNodes(self, node_father, u):
        if node_father == -1:
            return
        for board in u:
            # self.count_nodes += 1
            self.nodes_pos.append(board)
            self.graph[node_father].append(self.count_nodes)
            self.depth_node[self.count_nodes] = self.depth_node[node_father] + 1
            self.count_nodes += 1

    def setWeight(self, u, weight):
        self.node_weights[u] = weight

    def getWeight(self, u):
        return self.node_weights[u]

    def getGraph(self):
        return self.graph

    def howManyNodes(self):
        return self.count_nodes

    def getDepth(self):
        mark = [False] * self.maxn
        dist = [0] * self.maxn
        queue = deque()
        queue.append(0)
        mark[0] = True

        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if not mark[v]:
                    dist[v] = dist[u] + 1
                    queue.append(v)
                    mark[v] = True

        return dist[self.count_nodes]

    def getDepthFromNode(self, u):
        return self.depth_node[u]

    def getBoard(self, node):
        return self.nodes_pos[node]

    def getSon(self, u):
        return self.graph[u]

    def printGraph(self):
        for i in range(self.count_nodes):
            print(f"The node: {i} has connections with this Boards -> {self.graph[i]}")

    def printWeightGraph(self):
        for i in range(self.count_nodes):
            print(f"The node: {i} has this weight -> {self.node_weights[i]}")
