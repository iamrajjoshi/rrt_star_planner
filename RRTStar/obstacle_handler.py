import numpy as np

class Obstacle:
    def __init__(self, coords, is_dynamic = None, movement_list = None, step_list = None):
        self.coords = coords
        self.is_dynamic = is_dynamic
        self.movement_list = movement_list
        self.step_list = step_list
        self.curr_time_step = 0

    def transform(self, step_size):
        if self.is_dynamic and len(self.movement_list) > 0:
            curr_movement = self.movement_list[0]
            self.coords[0] += curr_movement[0]
            self.coords[2] += curr_movement[0]

            self.coords[1] += curr_movement[1]
            self.coords[3] += curr_movement[1]
            self.curr_time_step += step_size
            
            if self.curr_time_step >= self.step_list[0]:
                self.movement_list.pop(0)
                self.step_list.pop(0)
                self.curr_time_step = 0
            return self.coords

        else:
            return self.coords
        


class Obstacle_Handler:
    '''
    The obstacles are defined as follows:
    [lower left x, lower left y, upper right x, upper right y]
    Each obstacle has 2 points, the lower left and the upper right.
    
    Each dynamic obstacle has a list of movements and a list of time_steps. The list of movements is a list of [x, y] movements, 
    and the list of time_steps is a list time_steps where time_step[i] is how long the robot will perform the ith movement.

    When returning the obstacles, need to convert to a list of lists.
    '''
    def __init__(self, step_size = 1.0) -> None:
        self.obstacles = []
        self.step_size = step_size

    def add_obstacle(self, obstacle: Obstacle):
        self.obstacles.append(obstacle)
    
    def transform(self):
        for i in range(len(self.obstacles)):
            self.obstacles[i].transform(self.step_size)
    
    def get_obstacles(self):
        arr = []
        for i in range(len(self.obstacles)):
            arr.append(self.obstacles[i].coords)
        return np.array(arr)
            