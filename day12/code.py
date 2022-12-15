from __future__ import annotations

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file


class Point:
    x: int
    y: int
    elevation: int
    visited: bool

    def __init__(self, x: int, y: int, elevation: int) -> None:
        self.x = x
        self.y = y
        self.elevation = elevation
        self.visited = False

    def can_move_to(self, o: Point, reverse=False) -> bool:
        return (
            self.elevation - o.elevation <= 1
            if reverse
            else o.elevation - self.elevation <= 1
        )

    def reset(self):
        self.visited = False

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)


if __name__ == "__main__":
    puzzle_input = from_file.get_input_for(12)
    if puzzle_input == None:
        sys.exit(1)

    start_point: Point = None
    end_point: Point = None

    grid: list[list[Point]] = []
    for i, line in enumerate(puzzle_input):
        grid_line = []
        for j, c in enumerate(line):
            p = Point(i, j, ord(c))
            if c == "E":
                p.elevation = ord("z")
                end_point = p
            elif c == "S":
                p.elevation = ord("a")
                start_point = p
            grid_line.append(p)
        grid.append(grid_line)

    width = len(grid[0])
    height = len(grid)
    point_within_grid = lambda i, j: i >= 0 and i < height and j >= 0 and j < width

    # Part 1 - Find the shortest path from the start to end point

    # Using Dijkstra's algorithm, start -> end
    queue: list[tuple[int, Point]] = [(0, start_point)]

    while True:
        if len(queue) == 0:
            print("Did not find end position starting from {}".format(start_point))
            break

        steps_taken, current_point = queue.pop(0)

        if current_point.visited:
            continue
        current_point.visited = True

        if current_point == end_point:
            # Shortest number of steps taken to reach the end point
            print(steps_taken)
            break

        for di, dj in [[0, -1], [0, 1], [-1, 0], [1, 0]]:
            x, y = current_point.x + di, current_point.y + dj
            if not point_within_grid(x, y):
                continue

            next_point = grid[x][y]
            if current_point.can_move_to(next_point):
                queue.append((steps_taken + 1, next_point))

    # Reset
    [p.reset() for gl in grid for p in gl]

    # Part 2 - Find the start position, starting from which end will be shortest
    # A start position can be any position which has the least height, that of 'a'

    # Using Dijkstra's algorithm again in the reverse. end -> start
    queue: list[tuple[int, Point]] = [(0, end_point)]
    end_elevation = ord("a")

    while True:
        if len(queue) == 0:
            print(
                "Did not find least height position backtracking from {}".format(
                    end_point
                )
            )
            break

        steps_taken, current_point = queue.pop(0)

        if current_point.visited:
            continue
        current_point.visited = True

        if current_point.elevation == end_elevation:
            # Shortest number of steps taken to reach the point with least elevation
            print(steps_taken)
            break

        for di, dj in [[0, -1], [0, 1], [-1, 0], [1, 0]]:
            x, y = current_point.x + di, current_point.y + dj
            if not point_within_grid(x, y):
                continue

            next_point = grid[x][y]
            if current_point.can_move_to(next_point, reverse=True):
                queue.append((steps_taken + 1, next_point))
