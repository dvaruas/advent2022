import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from typing import Optional

from utils import from_file


class GridSquare:
    filled_with_rock: bool
    filled_with_sand: bool

    def __init__(self) -> None:
        self.filled_with_rock = False
        self.filled_with_sand = False

    @property
    def is_filled(self) -> bool:
        return self.filled_with_rock or self.filled_with_sand

    def cleanup(self):
        self.filled_with_sand = False

    def __str__(self) -> str:
        if self.filled_with_rock:
            return "#"
        elif self.filled_with_sand:
            return "o"
        return "."


class Grid:
    width: int
    height: int
    actual_row_numbers_range: tuple[int, int]
    actual_column_numbers_range: tuple[int, int]
    grid: list[list[GridSquare]]

    def __init__(
        self, puzzle_input: list[str], initial_sand_position: tuple[int, int]
    ) -> None:
        # Find the min and max to determine the width and height of the grid
        # Include the initial position as well to locate it on the grid
        all_xs = [initial_sand_position[0]]
        all_ys = [initial_sand_position[1]]

        for line in puzzle_input:
            grid_points = line.split("->")
            for point in grid_points:
                # A point is of the format 498,4
                y, x = [int(p) for p in point.split(",")]
                all_xs.append(x)
                all_ys.append(y)

        self.actual_row_numbers_range = (min(all_xs), max(all_xs))
        self.actual_column_numbers_range = (min(all_ys), max(all_ys))
        self.width = (
            self.actual_column_numbers_range[1]
            - self.actual_column_numbers_range[0]
            + 1
        )
        self.height = (
            self.actual_row_numbers_range[1] - self.actual_row_numbers_range[0] + 1
        )
        self.grid = []
        for _ in range(self.height):
            grid_line = [GridSquare() for __ in range(self.width)]
            self.grid.append(grid_line)

        # Fill up the rock positions from the puzzle input
        for line in puzzle_input:
            grid_points = line.split("->")
            i = 0
            while i < len(grid_points) - 1:
                this_point, next_point = grid_points[i], grid_points[i + 1]

                this_point = tuple([int(p) for p in this_point.split(",")])
                this_point = (this_point[1], this_point[0])
                this_point = self.__convert_point_from_actual(this_point)

                next_point = tuple([int(p) for p in next_point.split(",")])
                next_point = (next_point[1], next_point[0])
                next_point = self.__convert_point_from_actual(next_point)

                if this_point[0] == next_point[0]:
                    # If points are in the same row
                    rfunc = (
                        range(this_point[1], next_point[1] + 1)
                        if this_point[1] < next_point[1]
                        else range(next_point[1], this_point[1] + 1)
                    )
                    px = this_point[0]
                    for py in rfunc:
                        self.grid[px][py].filled_with_rock = True
                elif this_point[1] == next_point[1]:
                    # Points are in the same column
                    rfunc = (
                        range(this_point[0], next_point[0] + 1)
                        if this_point[0] < next_point[0]
                        else range(next_point[0], this_point[0] + 1)
                    )
                    py = this_point[1]
                    for px in rfunc:
                        self.grid[px][py].filled_with_rock = True

                i += 1

    # Sets a rock flooring at the bottom which is seemingly infinte, but....
    # it actually isn't as a sand particle can only drop a certain extent given the conditions
    def set_infinite_rock_flooring(
        self, add_height: int, initial_sand_position: tuple[int, int]
    ) -> None:
        # Increase width of the existing grid
        desired_width_on_each_side = (self.height + add_height) - 1
        desired_expanse_on_left = desired_width_on_each_side - (
            initial_sand_position[1] - self.actual_column_numbers_range[0]
        )
        desired_expanse_on_right = desired_width_on_each_side - (
            self.actual_column_numbers_range[1] - initial_sand_position[1]
        )
        for i in range(self.height):
            left = [GridSquare() for __ in range(desired_expanse_on_left)]
            right = [GridSquare() for _ in range(desired_expanse_on_right)]
            self.grid[i] = left + self.grid[i] + right
        self.width = len(self.grid[0])

        # Increase height of the existing grid
        for _ in range(add_height):
            grid_line = [GridSquare() for __ in range(self.width)]
            self.grid.append(grid_line)
        self.height += add_height

        # Update the ranges for the actual row, col numbers
        self.actual_row_numbers_range = (
            self.actual_row_numbers_range[0],
            self.actual_row_numbers_range[1] + add_height,
        )
        self.actual_column_numbers_range = (
            self.actual_column_numbers_range[0] - desired_expanse_on_left,
            self.actual_column_numbers_range[1] + desired_expanse_on_right,
        )

        # Set rocks at the bottom of the floor
        bottom_line = self.grid[-1]
        for g in bottom_line:
            g.filled_with_rock = True

    # Converts an actual point to a grid point
    def __convert_point_from_actual(self, point: tuple[int, int]) -> tuple[int, int]:
        return (
            point[0] - self.actual_row_numbers_range[0],
            point[1] - self.actual_column_numbers_range[0],
        )

    def is_point_in_grid(self, point: tuple[int, int]) -> bool:
        return (
            self.actual_row_numbers_range[0]
            <= point[0]
            <= self.actual_row_numbers_range[1]
            and self.actual_column_numbers_range[0]
            <= point[1]
            <= self.actual_column_numbers_range[1]
        )

    # If point is not in grid, returns None. Else returns true if the point is filled
    def is_point_filled(self, point: tuple[int, int]) -> Optional[bool]:
        if not self.is_point_in_grid(point):
            return None
        grid_point = self.__convert_point_from_actual(point)
        grid_square = self.grid[grid_point[0]][grid_point[1]]
        return grid_square.is_filled

    # If point is not in the grid, returns None
    # Returns true or false depending on if the point could be filled with sand
    def fill_point_with_sand(self, point: tuple[int, int]) -> Optional[bool]:
        if not self.is_point_in_grid(point):
            return None
        grid_point = self.__convert_point_from_actual(point)
        grid_square = self.grid[grid_point[0]][grid_point[1]]
        if grid_square.is_filled:
            return False
        grid_square.filled_with_sand = True
        return True

    def cleanup(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j].cleanup()

    def __str__(self) -> str:
        lines = []
        for grid_line in self.grid:
            lines.append("".join(str(s) for s in grid_line))
        return "\n".join(lines)


if __name__ == "__main__":
    puzzle_input = from_file.get_input_for(14)
    if puzzle_input == None:
        sys.exit(1)

    # This is the starting position for all sand particles
    initial_sand_position = (0, 500)

    # Create the grid from the puzzle input
    grid = Grid(puzzle_input, initial_sand_position)

    # Part 1 -- Find total sand units grid can accomodate until it flows to abyss below
    sand_units = 0

    # Keep filling sand until we are out of the grid bounds for any sand particle
    out_of_grid = False
    while not out_of_grid:
        # Keep going until sand is settled at a grid position
        # or we are out of the grid, in which case stop completely
        potential_position = initial_sand_position

        while True:
            # Find the position we can go down to till we hit rock or go out of grid
            next_position = (potential_position[0] + 1, potential_position[1])
            while True:
                res = grid.is_point_filled(next_position)
                if res == None:
                    # We have gone out of grid, time to quit
                    out_of_grid = True
                    break
                elif res == True:
                    # The position is filled, so we cannot go any further down
                    break
                else:
                    # Keep going to see how further down we can go
                    potential_position = next_position
                    next_position = (potential_position[0] + 1, potential_position[1])

            if out_of_grid:
                break

            # Try to go to the left diagonally
            next_position = [potential_position[0] + 1, potential_position[1] - 1]
            res = grid.is_point_filled(next_position)
            if res == None:
                # We have gone out of grid, time to quit
                out_of_grid = True
            elif res == True:
                # We are blocked and cannot go to the left
                pass
            else:
                # This is another potential position, update it and start again
                potential_position = next_position
                continue

            if out_of_grid:
                break

            # Try to go to the right diagonally
            next_position = [potential_position[0] + 1, potential_position[1] + 1]
            res = grid.is_point_filled(next_position)
            if res == None:
                # We have gone out of grid, time to quit
                out_of_grid = True
            elif res == True:
                # We are blocked and cannot go to the right
                pass
            else:
                # This is another potential position, update it and start again
                potential_position = next_position
                continue

            if out_of_grid:
                break

            # If we reached here that means that we have reached a stable position for the sand particle
            # Fill this position with sand
            grid.fill_point_with_sand(potential_position)
            sand_units += 1
            break

    print(sand_units)

    # Part 2 -- With infinite rock flooring at height+2, how many sand units can the grid accomodate before blocking the source
    sand_units = 0

    grid.cleanup()
    grid.set_infinite_rock_flooring(2, initial_sand_position)

    # Keep filling sand until we reach the initial position
    while True:
        # When the initial position is filled, it's time to quit this search
        if grid.is_point_filled(initial_sand_position) == True:
            break

        # Keep going until sand is settled at a grid position
        # We assume we will never go out of grid coz our grid is setup accordingly
        potential_position = initial_sand_position

        while True:
            # Find the position we can go down to till we hit rock
            next_position = (potential_position[0] + 1, potential_position[1])
            while True:
                res = grid.is_point_filled(next_position)
                if res == True:
                    # The position is filled, so we cannot go any further down
                    break
                else:
                    # Keep going to see how further down we can go
                    potential_position = next_position
                    next_position = (potential_position[0] + 1, potential_position[1])

            # Try to go to the left diagonally
            next_position = [potential_position[0] + 1, potential_position[1] - 1]
            res = grid.is_point_filled(next_position)
            if res == True:
                # We are blocked again
                pass
            else:
                # This is another potential position, update it
                potential_position = next_position
                continue

            # Try to go to the right
            next_position = [potential_position[0] + 1, potential_position[1] + 1]
            res = grid.is_point_filled(next_position)
            if res == True:
                # We are blocked again
                pass
            else:
                # This is another potential position, update it
                potential_position = next_position
                continue

            # If we reached here that means that we have reached a stable position for the sand particle
            # Fill this position with sand
            grid.fill_point_with_sand(potential_position)
            sand_units += 1
            break

    print(sand_units)
