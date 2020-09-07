from queue import PriorityQueue, Queue
from grid_state import GridState
import numpy as np
import time

class GridSolver():
    # Class for describing and solving N-Puzzle configurations of any size

    def __init__(self, init_state, goal_state, max_iter=500000):
        self.init_state = init_state
        self.goal_state = goal_state
        self.MAX = 1000000
        self.max_iter = max_iter
        self.path = []
        self.number_of_steps = 0
        self.summary = ""

    def set_max_iter(self, max_iter):
        self.max_iter = max_iter

    def get_path(self):
        return self.path

    def get_summary(self):
        return self.summary


    def solve_grid(self):
        # Solves grid using A* algorithm and manhattan distance heuristic.
        # The move sequence is inserted into self.path

        visited_nodes = set()
        nodes = PriorityQueue(self.MAX)
        init_node = GridState(self.init_state.flatten().tolist(), self.goal_state.flatten().tolist(), 0)
        nodes.put(init_node)
        epochs = 0
        while nodes.qsize() and epochs <= self.max_iter:
            epochs += 1
            curr_node = nodes.get()
            curr_state = curr_node.get_curr_state()
            if str(curr_state) in visited_nodes:
                continue
            visited_nodes.add(str(curr_state))
            if curr_state == self.goal_state.flatten().tolist():
                while curr_node.get_parent():
                    self.path.append(curr_node)
                    curr_node = curr_node.get_parent()
                break
            self.scan_neighbours(curr_node, nodes, visited_nodes)
        if epochs > self.max_iter:
                print('Out of time')
        return self.path

    def gap_location(self, curr_state):
        # Locates the empty tile on the grid and returns it's coordinates

        empty_tile = curr_state.index(0)
        i, j = empty_tile // self.goal_state.shape[0], empty_tile % self.goal_state.shape[0]
        return (i,j)

    def scan_neighbours(self, curr_node, next_nodes, visited_nodes):
        # Scans all neighbours of current node.
        # If the neighbour hasn't been visited, it will be inserted into next_nodes

        curr_state = curr_node.get_curr_state()
        i, j = self.gap_location(curr_state)
        curr_state = np.array(curr_state).reshape(self.goal_state.shape[0], self.goal_state.shape[0])
        for (x, y) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_state = np.array(curr_state)
            if i + x >= 0 and i + x < self.goal_state.shape[0] and j + y >= 0 and j + y < self.goal_state.shape[0]:
                new_state[i, j], new_state[i + x, j + y] = new_state[i + x, j + y], new_state[i, j]
                grid_state = GridState(new_state.flatten().tolist(), self.goal_state.flatten().tolist(),
                                       curr_node.get_step() + 1, curr_node)
                if str(grid_state.get_curr_state()) not in visited_nodes:
                    next_nodes.put(grid_state)




