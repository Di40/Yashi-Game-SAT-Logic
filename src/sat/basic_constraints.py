from pysat.formula import WCNF
from src.sat.no_crossing_constraint import calculate_no_crossing_constraint
from src.sat.no_cycles_constraint import calculate_no_cycles_constraint
from src.sat.exactly_k_constraint import calculate_exactly_k_constraint


def generate_yashi_basic_constraints(graph, lines, points, pointsToLine):
    """
        Generate fundamental constraints for a Yashi game.

        Parameters:
        - graph (Graph): The graph representing the game board's structure.
        - lines (Lines): A dictionary mapping line identifiers to pairs of points.
        - points (Points): A list of points in the puzzle.
        - pointsToLine (PointsToLine): A dictionary mapping points to the lines they belong to.

        Returns:
        - phi (WCNF): The WCNF formula representing the core constraints of the Yashi game.

        This function generates fundamental constraints for solving a Yashi game, where players connect points
        with lines while adhering to specific rules. The constraints include:

        1. No_crossing constraints: Lines must not cross each other.
        2. No_cycles constraints: The game board's structure should not contain cycles (loops).
        3. Exactly_n-1 constraints: Exactly  n−1  lines must be used to connect the points.

        The combined WCNF formula enforces these constraints and can be used by a SAT solver to solve the Yashi puzzle.
        """

    # Calculate constraints
    no_crossing_constraints = calculate_no_crossing_constraint(lines, points)
    no_cycles_constraints = calculate_no_cycles_constraint(graph, pointsToLine)
    exactly_n_minus_1_constraints = calculate_exactly_k_constraint(lines.keys(), len(points) - 1)

    # Combine all hard constraints
    hard_constraints = (no_crossing_constraints.hard +
                        no_cycles_constraints.hard +
                        exactly_n_minus_1_constraints.hard)

    # Create the WCNF formula
    phi = WCNF()
    phi.extend(hard_constraints)

    return phi
