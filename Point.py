import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        x_dis = abs(self.x - other.x)
        y_dis = abs(self.y - other.y)
        distance_to_other = np.sqrt((x_dis ** 2) + (y_dis ** 2))
        return distance_to_other

    def __repr__(self):
        return f"({str(self.x)}, {str(self.y)})"