import numpy as np

class GridState():
    def __init__(self, curr_state, goal_state, step, parent = None):
        self.curr_state = curr_state
        self.goal_state = goal_state
        self.step = step
        self.parent = parent
        self.score = step
        self.calculate_potential()

    def __hash__(self):
        return hash(str(self.curr_state))

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score

    def __gt__(self, other):
        return self.score > other.score

    def get_curr_state(self):
        return self.curr_state

    def get_step(self):
        return self.step

    def get_parent(self):
        return self.parent

    def manhattan_distance(self, x_curr, y_curr, x_goal, y_goal):
        return abs(x_curr-x_goal)+abs(y_curr-y_goal)

    def calculate_potential(self):
        for tile in self.curr_state:
            i_curr = self.curr_state.index(tile)
            i_goal = self.goal_state.index(tile)
            x_curr, y_curr = i_curr // int(np.sqrt(len(self.curr_state))), i_curr % int(np.sqrt(len(self.curr_state)))
            x_goal, y_goal = i_goal // int(np.sqrt(len(self.curr_state))), i_goal % int(np.sqrt(len(self.curr_state)))
            self.score += self.manhattan_distance(x_curr, y_curr, x_goal, y_goal)

    def calculate_potential_two(self):
        self.score = self.step
        for curr_tile, goal_tile in zip(self.curr_state, self.goal_state):
            if (curr_tile != goal_tile):
                self.score += 1






