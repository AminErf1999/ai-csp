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

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [
            v for v in self.variables if v not in assignment]

        # heuristic for choosing variable will go here...
        first: V = unassigned[0]
        # heuristic for choosing domain will go here..
        for value in self.domains[first]:
            local_assignment = assignment.copy()  # creates a brand new object
            local_assignment[first] = value

            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(
                    local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result

                if result is None:
                    if local_assignment[first] == '+':
                        RemainingMagnetConstraint.remaining_magnet["pos"]["row"][first.position[0]] += 1
                        RemainingMagnetConstraint.remaining_magnet["pos"]["col"][first.position[1]] += 1
                    elif local_assignment[first] == '-':
                        RemainingMagnetConstraint.remaining_magnet["neg"]["row"][first.position[0]] += 1
                        RemainingMagnetConstraint.remaining_magnet["neg"]["col"][first.position[1]] += 1

        return None
