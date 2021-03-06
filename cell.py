from typing import Dict, List


class Cell():
    def __init__(self, position: list) -> None:
        self.position = position
        self.value = 0
        self.mutual_cell = None
        self.neighbors: List[Cell] = []

    def set_value(self, value: int):
        self.value = value

    def get_value(self):
        return self.value

    def add_mutual_cell(self, cell):
        self.mutual_cell = cell

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
