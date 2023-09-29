from collections import defaultdict

from src.custom_types import Lines, Points, PointsToLine

def get_direction_params(direction, x, y, grid_size):
    # end_of_grid, increment, variable_to_move
    directions = {
        "right": (grid_size, 1, x),
        "left": (-1, -1, x),
        "up": (grid_size, 1, y),
        "down": (-1, -1, y),
    }
    return directions.get(direction, (0, 0, 0))

def get_neighbor_based_on_direction(grid, direction, x, y, i):
    if direction in ["right", "left"]:
        neighbor_x, neighbor_y = i, y
    else:
        neighbor_x, neighbor_y = x, i
    return grid[neighbor_x].get(neighbor_y, None)

def connect_points_to_lines(df_points):
    grid_size = len(df_points)
    points, lines = {}, {}
    grid = defaultdict(dict)
    line_added = defaultdict(bool)
    point_to_lines = defaultdict(dict)

    # Create points and grid dictionaries
    for _, x in df_points.iterrows():
        pointID, x, y = x["point"], x["x"], x["y"]
        points[pointID] = (x, y)
        grid[x][y] = pointID

    # Allowed directions - by doing this we deal with the "No diagonal lines" constraint
    directions = ["up", "down", "left", "right"]

    line_id = 1  # We will increment this as an ID for the lines in the grid
    for current_point, (x, y) in points.items():

        for direction in directions:
            end_of_grid, increment, variable_to_move = get_direction_params(direction, x, y, grid_size)

            for i in range(variable_to_move + increment, end_of_grid, increment):
                neighbor_point = get_neighbor_based_on_direction(grid, direction, x, y, i)
                if neighbor_point is not None:
                    sorted_points = tuple(sorted([current_point, neighbor_point]))
                    if not line_added[sorted_points]:
                        lines[line_id] = sorted_points
                        point_to_lines[neighbor_point][current_point] = line_id
                        point_to_lines[current_point][neighbor_point] = line_id
                        line_added[sorted_points] = True
                        line_id += 1
                    break

    return lines, points, point_to_lines
