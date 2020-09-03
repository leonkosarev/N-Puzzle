import numpy as np

class GridState():
    def __init__(self, curr_state, goal_state, step, parent = None):
        self.__curr_state = curr_state
        self.__goal_state = goal_state
        self.__step = step
        self.__parent = parent
        self.__score = step
        self.__get_potential()

    def __hash__(self):
        return hash(str(self.__curr_state))

    def __lt__(self, other):
        return self.__score < other.__score

    def __eq__(self, other):
        return self.__score == other.__score

    def __gt__(self, other):
        return self.__score > other.__score

    def get_curr_state(self):
        return self.__curr_state

    def get_step(self):
        return self.__step

    def get_parent(self):
        return self.__parent

    def calculate_potential(self):
        self.__score = self.__step
        for curr_tile, goal_tile in zip(self.__curr_state, self.__goal_state):
            if (curr_tile != goal_tile):
                self.__score += 1






