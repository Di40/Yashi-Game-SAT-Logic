from pysat.formula import WCNF
from shapely.geometry import LineString
from itertools import combinations


def lines_cross(line1, line2, line_segments):
    l1_segment = line_segments[line1]
    l2_segment = line_segments[line2]
    return l1_segment.intersects(l2_segment) and not l1_segment.touches(l2_segment)


def calculate_no_crossing_constraint(lines, points):
    phi_no_crossing = WCNF()
    line_ids = list(lines.keys())
    line_segments = {line_id: LineString([points[line[0]], points[line[1]]]) for line_id, line in lines.items()}

    # Use itertools combinations to generate pairs of lines
    for l1_id, l2_id in combinations(line_ids, 2):
        if lines_cross(l1_id, l2_id, line_segments):
            phi_no_crossing.append([-l1_id, -l2_id])
        # If two lines are crossing, append the formula that forces to not use them at once.

    return phi_no_crossing
