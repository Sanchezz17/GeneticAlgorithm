import numpy as np


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance(self, other: 'Point') -> float:
        """Возвращает расстояние между двумя точками."""
        x_dis = abs(self.x - other.x)
        y_dis = abs(self.y - other.y)
        distance_to_other = np.sqrt((x_dis ** 2) + (y_dis ** 2))
        return distance_to_other

    def __str__(self) -> str:
        return f"({str(self.x)}, {str(self.y)})"
