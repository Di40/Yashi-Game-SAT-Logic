from pysat.formula import WCNF
from src.utils import euclidean_distance


def calculate_minimum_length_solution_constraints(lines, points, points_to_lines):
    """
    Create WCNF constraints for a minimum length solution.

    Args:
        lines (dict): Dictionary of lines represented by pairs of points.
        points (dict): Dictionary of points with their coordinates.
        points_to_lines (dict): Mapping of points to lines.

    Returns:
        WCNF: Weighted Conjunctive Normal Form formula representing constraints.
    """
    phi = WCNF()

    for (point_1, point_2) in lines.values():
        line_weight = -euclidean_distance(points[point_1], points[point_2])
        phi.append([points_to_lines[point_1][point_2]], weight=line_weight)

    return phi
