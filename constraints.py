from cell import Cell
from typing import Generic, TypeVar, Dict, List
from abc import ABC, abstractmethod


V = TypeVar('V')
D = TypeVar('D')


class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, cell, assignment: Dict[V, D]) -> bool:
        ...


class RemainingMagnetConstraint(Constraint[Cell, str]):  # 3
    remaining_magnet: Dict

    def __init__(self, cells: List[Cell]) -> None:
        super().__init__(cells)

    def has_remaining_magnet(self, sign: str, position: List[int]) -> bool:
        if (RemainingMagnetConstraint.remaining_magnet[sign]["row"][position[0]] > 0 and RemainingMagnetConstraint.remaining_magnet[sign]["col"][position[1]] > 0):
            return True

    def get_remaining_pos_magnet_count(self, direction: str, position: List[int]) -> int:
        if (direction == 'row'):
            return RemainingMagnetConstraint.remaining_magnet['pos']['row'][position[0]]
        elif (direction == 'col'):
            return RemainingMagnetConstraint.remaining_magnet['pos']['col'][position[1]]

    def get_remaining_neg_magnet_count(self, direction: str, position: List[int]) -> int:
        if (direction == 'row'):
            return RemainingMagnetConstraint.remaining_magnet['neg']['row'][position[0]]
        elif (direction == 'col'):
            return RemainingMagnetConstraint.remaining_magnet['neg']['col'][position[1]]

    def get_unassigned_cells_count(self, direction: str, position: List[int]) -> int:
        if (direction == 'row'):
            return len(
                RemainingMagnetConstraint.remaining_magnet['pos']['row']) - position[1] - 1
        elif(direction == 'col'):
            return len(
                RemainingMagnetConstraint.remaining_magnet['pos']['col']) - position[0] - 1

    def satisfied(self, cell: Cell, assignment: Dict[Cell, int]) -> bool:
        cellPos = cell.position

        if (assignment[cell] == '+'):
            if (not self.has_remaining_magnet('pos', cellPos)):
                # print('-- no remaining positive magnet --')
                return False
            elif (self.get_remaining_pos_magnet_count('row', cellPos) - 1 > self.get_unassigned_cells_count('row', cellPos)
                    or self.get_remaining_pos_magnet_count('col', cellPos) - 1 > self.get_unassigned_cells_count('col', cellPos)):
                # print('-- more positive magnet than remaining cells --')
                return False
            RemainingMagnetConstraint.remaining_magnet["pos"]["row"][cellPos[0]] -= 1
            RemainingMagnetConstraint.remaining_magnet["pos"]["col"][cellPos[1]] -= 1

        elif (assignment[cell] == '-'):
            if (not self.has_remaining_magnet('neg', cellPos)):
                # print('-- no remaining negative magnet --')
                return False
            elif (self.get_remaining_neg_magnet_count('row', cellPos) - 1 > self.get_unassigned_cells_count('row', cellPos)
                    or self.get_remaining_neg_magnet_count('col', cellPos) - 1 > self.get_unassigned_cells_count('col', cellPos)):
                # print('-- more negative magnet than remaining cells --')
                return False
            RemainingMagnetConstraint.remaining_magnet["neg"]["row"][cellPos[0]] -= 1
            RemainingMagnetConstraint.remaining_magnet["neg"]["col"][cellPos[1]] -= 1

        elif (assignment[cell] == '0'):
            if(self.get_remaining_pos_magnet_count('row', cellPos) > self.get_unassigned_cells_count('row', cellPos)
                    or self.get_remaining_pos_magnet_count('col', cellPos) > self.get_unassigned_cells_count('col', cellPos)
                    or self.get_remaining_neg_magnet_count('row', cellPos) > self.get_unassigned_cells_count('row', cellPos)
                    or self.get_remaining_neg_magnet_count('col', cellPos) > self.get_unassigned_cells_count('col', cellPos)):
                # print('-- more positive and negative magnet than remaining cells --')
                return False

            return True

        return True


class SameAdjacentPoleConstraint(Constraint[Cell, str]):  # 1
    def __init__(self, cells: List[Cell]) -> None:
        super().__init__(cells)

    def satisfied(self, cell: Cell, assignment: Dict[Cell, int]) -> bool:
        neighbors: List[Cell] = cell.neighbors

        for neighbor in neighbors:
            if (neighbor not in assignment):
                continue
            elif(assignment[neighbor] == '0'):
                continue
            elif (assignment[neighbor] == assignment[cell]):
                return False
        return True


class OpposeMagnetConstraint(Constraint[Cell, str]):  # 2
    def __init__(self, cells: List[Cell]) -> None:
        super().__init__(cells)

    def satisfied(self, cell: Cell, assignment: Dict[Cell, int]) -> bool:
        mutual_cell: Cell
        if cell.mutual_cell is not None:
            mutual_cell = cell.mutual_cell

        if (mutual_cell not in assignment):
            return True
        elif (assignment[mutual_cell] == '-' and assignment[cell] in ['-', '0']):
            return False
        elif (assignment[mutual_cell] == '+' and assignment[cell] in ['+', '0']):
            return False
        elif (assignment[mutual_cell] == '0' and assignment[cell] in ['+', '-']):
            return False

        return True
