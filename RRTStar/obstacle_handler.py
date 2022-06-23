import numpy as np

class Obstacle:
    def __init__(self, coords, is_dynamic = None, transformation_matrix=None):
        self.coords = coords
        self.is_dynamic = is_dynamic
        self.transformation_matrix = transformation_matrix
    def transform(self):
        if self.is_dynamic:
            return self.transformation_matrix @ self.coords #Make sure matrix multiplication happens
        else:
            return self.coords
        


class Obstacle_Handler:
    '''
    The obstacles are defined as follows:
    [lower left x, lower left y, upper right x, upper right y]
    Each obstacle has 2 points, the lower left and the upper right.
    
    At each step, the obstacles are transformed by the transformation matrix.

    When returning the obstacles, need to convert to a list of lists.
    '''
    def __init__(self) -> None:
        self.obstacles = []
        self.transformations = []

    def add_obstacle(self, obstacle: np.ndarray):
        self.obstacles.append(obstacle)
        print(self.obstacles)
    
    def add_transformations(self, transformation: np.ndarray):
        self.transformations.append(transformation)
    
    def transform(self):
        for i in range(len(self.obstacles)):
            self.obstacles[i] = self.transformations[i].dot(self.obstacles[i])
    
    def get_obstacles(self):
        # return [self.obstacles[0][0], self.obstacles[0][1], self.]
        pass
            