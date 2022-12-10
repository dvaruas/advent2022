import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from typing import Optional

from utils import from_file


def find_blocking_tree(
    size_to_check: int,
    check_against_elements: list[int],
    search_range: tuple[int, int],
    reverse: bool = False,
) -> Optional[int]:
    start, end = search_range[0], search_range[1]

    check_ranger = range(start, end)
    if reverse:
        check_ranger = range(end - 1, start - 1, -1)

    for i in check_ranger:
        if size_to_check <= check_against_elements[i]:
            return i

    # Returns None if we reached the edge and did not find anything >= size_to_check
    return None


if __name__ == "__main__":
    tree_grid_input = from_file.get_input_for(8)
    if tree_grid_input == None:
        sys.exit(1)

    tree_grid_row_wise = []
    for tree_line in tree_grid_input:
        tree_grid_row_wise.append([int(t) for t in tree_line])

    # Given: a square grid, so number of rows and columns are same
    grid_size = len(tree_grid_row_wise)

    tree_grid_column_wise = []
    for i in range(grid_size):
        tree_grid_column_wise.append(
            [tree_grid_row_wise[j][i] for j in range(grid_size)]
        )

    # Part 1 - Finding total trees from outside the grid
    # All trees on the edge are always visible from the outside, so add them
    trees_visible = (grid_size - 1) * 4

    for i in range(1, grid_size - 1):
        row_elems = tree_grid_row_wise[i]
        for j in range(1, grid_size - 1):
            column_elems = tree_grid_column_wise[j]
            tree_size = tree_grid_row_wise[i][j]

            if find_blocking_tree(tree_size, row_elems, (0, j), reverse=True) == None:
                # Check if we can see the edge towards the left from the tree
                trees_visible += 1
            elif find_blocking_tree(tree_size, row_elems, (j + 1, grid_size)) == None:
                # Check if we can see the edge towards the right from the tree
                trees_visible += 1
            elif (
                find_blocking_tree(tree_size, column_elems, (0, i), reverse=True)
                == None
            ):
                # Check if we can see the edge towards the top from the tree
                trees_visible += 1
            elif (
                find_blocking_tree(tree_size, column_elems, (i + 1, grid_size)) == None
            ):
                # Check if we can see the edge towards the bottom from the tree
                trees_visible += 1

    # Total number of trees which can be seen from the edges
    print(trees_visible)

    # Part 2 - Highest scenic score among all trees in the grid
    highest_scenic_score = 0
    for i in range(1, grid_size - 1):
        row_elems = tree_grid_row_wise[i]
        for j in range(1, grid_size - 1):
            column_elems = tree_grid_column_wise[j]
            tree_size = tree_grid_row_wise[i][j]

            scenic_score = 1

            # Checking on the left side of the tree
            blocking_tree_index = find_blocking_tree(
                tree_size, row_elems, (0, j), reverse=True
            )
            if blocking_tree_index == None:
                scenic_score *= j
            else:
                scenic_score *= j - blocking_tree_index

            # Checking on the right side of the tree
            blocking_tree_index = find_blocking_tree(
                tree_size, row_elems, (j + 1, grid_size)
            )
            if blocking_tree_index == None:
                scenic_score *= grid_size - j - 1
            else:
                scenic_score *= blocking_tree_index - j

            # Checking on the top side of the tree
            blocking_tree_index = find_blocking_tree(
                tree_size, column_elems, (0, i), reverse=True
            )
            if blocking_tree_index == None:
                scenic_score *= i
            else:
                scenic_score *= i - blocking_tree_index

            # Checking on the bottom side of the tree
            blocking_tree_index = find_blocking_tree(
                tree_size, column_elems, (i + 1, grid_size)
            )
            if blocking_tree_index == None:
                scenic_score *= grid_size - i - 1
            else:
                scenic_score *= blocking_tree_index - i

            if scenic_score > highest_scenic_score:
                highest_scenic_score = scenic_score

    # The highest scenic score among all scores for all trees
    print(highest_scenic_score)
