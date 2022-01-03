from csp import CSP
from typing import Dict, List, Optional
from cell import Cell
from constraints import OpposeMagnetConstraint, RemainingMagnetConstraint, SameAdjacentPoleConstraint


if __name__ == "__main__":

    n, m = (int(i) for i in input().split())

    remaining_magnet = {
        "pos": {
            "row": [],
            "col": []
        },
        "neg": {
            "row": [],
            "col": []
        }
    }
    remaining_magnet["pos"]["row"] = [int(i) for i in input().split()]
    remaining_magnet["neg"]["row"] = [int(i) for i in input().split()]
    remaining_magnet["pos"]["col"] = [int(i) for i in input().split()]
    remaining_magnet["neg"]["col"] = [int(i) for i in input().split()]

    variables: List[Cell] = []
    table = []
    for i in range(n):
        table.append(input().split())

    for i in range(len(table)):
        for j in range(len(table[0])):
            cell_value = int(table[i][j])
            cell = Cell([i, j])
            cell.set_value(cell_value)
            variables.append(cell)

    def is_neighbor(variable: Cell, other_variable: Cell, max_row, max_col) -> bool:

        variable_row = variable.position[0]
        variable_col = variable.position[1]

        other_variable_row = other_variable.position[0]
        other_variable_col = other_variable.position[1]

        variable_neighbors_rows = [i for i in [variable_row +
                                               1, variable_row - 1] if 0 <= i <= max_row]
        variable_neighbors_cols = [i for i in [variable_col +
                                               1, variable_col - 1] if 0 <= i <= max_col]

        if (variable_row == other_variable_row and other_variable_col in variable_neighbors_cols):
            return True
        if (variable_col == other_variable_col and other_variable_row in variable_neighbors_rows):
            return True

        return False

    def is_mutual(variable: Cell, other_variable: Cell) -> bool:
        if (variable.get_value() == other_variable.get_value()):
            return True

    for variable in variables:
        for other in variables:
            if variable == other:
                continue
            else:
                if is_neighbor(variable, other, n, m):
                    variable.add_neighbor(other)
                    if is_mutual(variable, other):
                        variable.add_mutual_cell(other)

    # for variable in variables:
    #     if variable.mutual_cell is not None:
    #         print(f'variable position: {variable.position}')
    #         print(
    #             f'mutual of this variable is: {variable.mutual_cell.position}')
    #         print('______________________')

    # for variable in variables:
    #     print(f'variable position: {variable.position}')
    #     for neighbor in variable.neighbors:
    #         print(f'neighbors of this variable are: {neighbor.position}')
    #     print('_________________')

    domains: Dict[Cell, List[str]] = {}
    for variable in variables:
        domains[variable] = ['+', '-', '0']

    csp: CSP[Cell, str] = CSP(variables, domains)

    RemainingMagnetConstraint.remaining_magnet = remaining_magnet
    csp.add_constraint(SameAdjacentPoleConstraint(variables))
    csp.add_constraint(OpposeMagnetConstraint(variables))
    csp.add_constraint(RemainingMagnetConstraint(variables))

    # print(f'pos: {RemainingMagnetConstraint.remaining_magnet["pos"]}')
    # print(f'neg: {RemainingMagnetConstraint.remaining_magnet["neg"]}')

    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        index = 0
        solutions = []
        for cell in solution:
            index += 1
            solutions.append(solution[cell])
            if (index % m == 0):
                print(solutions)
                solutions = []
    #             index = 0

    # print(f'pos: {RemainingMagnetConstraint.remaining_magnet["pos"]}')
    # print(f'neg: {RemainingMagnetConstraint.remaining_magnet["neg"]}')
