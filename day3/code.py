import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file


def get_item_priority(item: str) -> int:
    a, A = ord("a"), ord("A")
    i = ord(item)

    if i >= a:
        # It falls between a - z, since a has a higher ASCII values than A
        return i - a + 1
    else:
        # It falls between A - Z
        return i - A + 27


if __name__ == "__main__":
    rucksacks_items = from_file.get_input_for(3)
    if rucksacks_items == None:
        print("input not found")
        sys.exit(1)

    # Part 1 - Find common items among compartments in a rucksack
    total_priority = 0

    for rucksack_contents in rucksacks_items:
        comparment_length = len(rucksack_contents) // 2
        compartment_one_items = set(rucksack_contents[:comparment_length])
        compartment_two_items = set(rucksack_contents[comparment_length:])

        total_priority += sum(
            [
                get_item_priority(item)
                for item in compartment_one_items.intersection(compartment_two_items)
            ]
        )

    # Total priority of all items common in both compartments of the rucksack
    print(total_priority)

    # Part 2 - Find priority of items for all the groups
    total_priority = 0

    i = 0
    total_rucksacks = len(rucksacks_items)
    while i < total_rucksacks:
        rucksack_one, rucksack_two, rucksack_three = [
            set(rucksacks_items[i + j]) for j in range(3)
        ]
        badge_item = (
            rucksack_one.intersection(rucksack_two).intersection(rucksack_three).pop()
        )
        total_priority += get_item_priority(badge_item)
        i += 3

    # Total priority for all the badge items for all the grouped elves
    print(total_priority)
