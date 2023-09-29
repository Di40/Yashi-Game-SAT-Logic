from typing import Dict, NewType, Tuple

# The coordinate of a point (either the x or y value).
Coordinate = NewType("Coordinate", float)

# An identifier for a point.
PointID = NewType("Point_ID", int)

# An identifier for a line.
LineID = NewType("Line_ID", int)

# The coordinates of a point as a tuple (x, y).
Point = NewType("Point", Tuple[Coordinate, Coordinate])

# A line connecting two points, defined as a tuple (Point1ID, Point2ID).
Line = NewType("Line", Tuple[PointID, PointID])

# A dictionary that maps line identifiers to their corresponding points.
Lines = NewType("Lines", Dict[LineID, Line])

# A dictionary that maps point identifiers to their (x, y) coordinates.
Points = NewType("Points", Dict[PointID, Point])

# A dictionary that maps pairs of points to the line formed by connecting them.
PointsToLine = NewType("PointsToLine", Dict[PointID, Dict[PointID, LineID]])

# Graph related data types:
Edge = NewType("Edge", Tuple[float, float, float])
Vertex = NewType("Vertex", float)
Cycle = NewType("Cycle", set[Edge])
