import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from ast import literal_eval
from typing import Optional

from utils import from_file


# Returns True if left is less than right, else returns False
# Returns None if both are equal and we are indecisive
def in_right_order(left: list | int, right: list | int) -> Optional[bool]:
    # If either left or right is not a list, convert it into one
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]

    left_length = len(left)
    right_length = len(right)

    i = 0
    while i < left_length and i < right_length:
        l, r = left[i], right[i]

        if isinstance(l, int) and isinstance(r, int):
            # If the left number is less than right, return True
            if l < r:
                return True
            elif l > r:
                return False
        else:
            # If either one or both are lists we try to compare them recursively
            res = in_right_order(l, r)
            if res != None:
                # We reached a decisive answer in that compare
                return res

        i += 1

    if i == left_length and i == right_length:
        # If both ran out of elements, it means we are indecisive
        return None
    if i == left_length:
        # Left side ran out of elements, which is a successful case
        return True
    if i == right_length:
        # Right side ran out of elements, which is a failure case
        return False


if __name__ == "__main__":
    puzzle_input = from_file.get_input_for(13)
    if puzzle_input == None:
        sys.exit(1)

    all_packets: list = []

    # Parse the input to get all the packets info
    n = len(puzzle_input)
    i = 0
    while i < n:
        # Read the left list
        left = literal_eval(puzzle_input[i])

        # Read the right list
        right = literal_eval(puzzle_input[i + 1])

        # Save both lists
        all_packets.append(left)
        all_packets.append(right)

        # Skip to the next group
        i += 3

    # Part 1 -- Find sum of indices of all groups of packets in right order
    sum = 0

    index = 1
    n = len(all_packets)
    i = 0
    while i < n:
        if in_right_order(all_packets[i], all_packets[i + 1]) == True:
            sum += index
        index += 1
        i += 2

    # Sum of all indices of groups in correct order
    print(sum)

    # Part 2 -- Find the decoder key for the distress signal

    # Add the two divider packets into the mix
    all_packets.append([[2]])
    all_packets.append([[6]])

    # Sort the packets using insertion sort, put in ascending order
    n = len(all_packets)
    i = 1
    while i < n:
        item = all_packets[i]
        j = i - 1
        while j >= 0:
            if in_right_order(all_packets[j], item) == True:
                break
            all_packets[j + 1] = all_packets[j]
            j -= 1
        all_packets[j + 1] = item
        i += 1

    # Find index of the two divider packets
    first_index = all_packets.index([[2]]) + 1
    second_index = all_packets.index([[6]]) + 1

    # Value of the decoder key which is the product of the two indices
    print(first_index * second_index)
