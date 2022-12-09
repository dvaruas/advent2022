import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file

movement_function = {
    "R": lambda pos: (pos[0] + 1, pos[1]),
    "L": lambda pos: (pos[0] - 1, pos[1]),
    "U": lambda pos: (pos[0], pos[1] + 1),
    "D": lambda pos: (pos[0], pos[1] - 1),
}

# Checks if the two given positions are adjacent to each other
def check_if_adjacent(
    position_one: tuple[int, int], position_two: tuple[int, int]
) -> bool:
    # If in the same row
    if position_one[1] == position_two[1]:
        if abs(position_one[0] - position_two[0]) == 1:
            return True
        return False

    # If in the same column
    if position_one[0] == position_two[0]:
        if abs(position_one[1] - position_two[1]) == 1:
            return True
        return False

    # If they are diagonally placed to each other
    if (
        abs(position_one[0] - position_two[0]) == 1
        and abs(position_one[1] - position_two[1]) == 1
    ):
        return True

    return False


def find_adjacent_position(
    current_position: tuple[int, int], adjacent_to: tuple[int, int]
) -> tuple[int, int]:
    # Check if both are the same position, if so current is fine
    if adjacent_to == current_position:
        return current_position

    # Check if both positions are already adjacent, if so current is fine
    if check_if_adjacent(position_one=adjacent_to, position_two=current_position):
        return current_position

    # The assumption is that
    # current_position and adjacent_to positions cannot be more than a block apart from each other ever
    # since we always keep updating them
    # So just move in a direction and they will both be adjacent (no need to check)

    if adjacent_to[1] == current_position[1]:
        # If we are in the same row
        if adjacent_to[0] < current_position[0]:
            # Move left
            return movement_function["L"](current_position)
        else:
            # Move right
            return movement_function["R"](current_position)
    elif adjacent_to[0] == current_position[0]:
        # If we are in the same column
        if adjacent_to[1] < current_position[1]:
            # Move down
            return movement_function["D"](current_position)
        else:
            # Move up
            return movement_function["U"](current_position)
    else:
        # Or maybe we need to move diagonally now
        if adjacent_to[1] < current_position[1]:
            # Move down
            current_position = movement_function["D"](current_position)
            if adjacent_to[0] < current_position[0]:
                # then left
                return movement_function["L"](current_position)
            else:
                # then right
                return movement_function["R"](current_position)
        else:
            # Move up
            current_position = movement_function["U"](current_position)
            if adjacent_to[0] < current_position[0]:
                # then left
                return movement_function["L"](current_position)
            else:
                # then right
                return movement_function["R"](current_position)


if __name__ == "__main__":
    moves_sequence = from_file.get_input_for(9)
    if moves_sequence == None:
        sys.exit(1)

    starting_position = (0, 0)
    # Part 1 - Find all position the tail has visited atleast once
    visited_positions = set()
    head_position = starting_position
    tail_position = starting_position
    visited_positions.add(tail_position)

    for move in moves_sequence:
        direction, steps = move.split()
        steps = int(steps)

        for s in range(steps):
            # Move the head as per the instruction given
            head_position = movement_function[direction](head_position)
            # Find new positions for the tail
            tail_position = find_adjacent_position(
                current_position=tail_position, adjacent_to=head_position
            )
            # Add the tails new position as a visited position
            visited_positions.add(tail_position)

    # All positions visited by the tail
    print(len(visited_positions))

    # Part 2 - Find all positions the tail at the end of the long rope has visited atleast once
    visited_positions.clear()

    # The positions are [head, 1, ...., 8, tail]
    all_positions = [starting_position] * 10
    visited_positions.add(all_positions[9])

    for move in moves_sequence:
        direction, steps = move.split()
        steps = int(steps)

        for s in range(steps):
            # Move the head as per the instruction given
            all_positions[0] = movement_function[direction](all_positions[0])
            # Find new positions for all the other knots of the rope
            for i in range(9):
                all_positions[i + 1] = find_adjacent_position(
                    current_position=all_positions[i + 1], adjacent_to=all_positions[i]
                )
            # Add the tails new position as a visited position
            visited_positions.add(all_positions[9])

    # All positions visited by just the tail
    print(len(visited_positions))
