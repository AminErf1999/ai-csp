from cell import Cell
from constraints import RemainingMagnetConstraint
from typing import Generic, TypeVar, Dict, List, Optional
from constraints import Constraint


V = TypeVar('V')
D = TypeVar('D')


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables  # variables to be constrained
        self.domains: Dict[V, List[D]] = domains  # domain of each variable
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError(
                    "Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(variable, assignment):
                return False
        return True

    def forward_check(self, assignment: Dict[V, D], cell: V, domains: Dict[V, List[D]]):
        mutual_cell = cell.mutual_cell
        neighbor_cells = cell.neighbors

        unassignedVairables = [
            v for v in self.variables if v not in assignment]

        if (assignment[cell] == '+'):
            for neighbor in neighbor_cells:
                if ('+' in domains[neighbor]):
                    domains[neighbor].remove('+')
            # mutual cell is already a neighbor
            if ('0' in domains[mutual_cell]):
                domains[mutual_cell].remove('0')

        elif (assignment[cell] == '-'):
            for neighbor in neighbor_cells:
                if ('-' in domains[neighbor]):
                    domains[neighbor].remove('-')
            # mutual cell is already a neighbor
            if ('0' in domains[mutual_cell]):
                domains[mutual_cell].remove('0')
        elif (assignment[cell] == '0'):
            if ('+' in domains[mutual_cell]):
                domains[mutual_cell].remove('+')
            if ('-' in domains[mutual_cell]):
                domains[mutual_cell].remove('-')

        for neighbor in neighbor_cells:
            if (len(domains[neighbor]) == 0):
                # print('forward chaining found a wrong assignment sooner!')
                return False

        return True

    def retrieveMagnet(self, assigned_value, cell: V) -> None:
        if assigned_value == '+':
            RemainingMagnetConstraint.remaining_magnet["pos"]["row"][cell.position[0]] += 1
            RemainingMagnetConstraint.remaining_magnet["pos"]["col"][cell.position[1]] += 1
        elif assigned_value == '-':
            RemainingMagnetConstraint.remaining_magnet["neg"]["row"][cell.position[0]] += 1
            RemainingMagnetConstraint.remaining_magnet["neg"]["col"][cell.position[1]] += 1

    def mrv_heuristic(self, unassigned, domains) -> Cell:
        minimum_remaining_value = unassigned[0]
        for variable in unassigned:
            if (len(domains[minimum_remaining_value]) == 1):
                return minimum_remaining_value
            if (len(domains[variable]) < len(domains[minimum_remaining_value])):
                minimum_remaining_value = variable

        return minimum_remaining_value

    def backtracking_search(self, assignment: Dict[V, D] = {}, domains: Dict[V, List[D]] = {}) -> Optional[Dict[V, D]]:
        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [
            v for v in self.variables if v not in assignment]

        first: V = self.mrv_heuristic(unassigned, domains)  # MRV heuristic
        # first: V = unassigned[0]  # normal backtrack

        # domains order should be changed here for  LCV heuristic
        for value in domains[first]:

            local_domains = dict()
            for cell, domain in domains.items():
                local_domains[cell] = domain.copy()

            local_assignment = assignment.copy()  # creates a brand new object
            local_assignment[first] = value

            # print(
            #     f'for cell: {first.position},with domain: {local_domains[first]}, value: {local_assignment[first]}')

            if self.consistent(first, local_assignment):
                if (not self.forward_check(local_assignment, first, local_domains)):
                    self.retrieveMagnet(local_assignment[first], first)
                    continue
                result: Optional[Dict[V, D]] = self.backtracking_search(
                    local_assignment, local_domains)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result

                if result is None:
                    self.retrieveMagnet(local_assignment[first], first)

        return None
