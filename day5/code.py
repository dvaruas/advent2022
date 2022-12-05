import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import re
from copy import deepcopy
from typing import NamedTuple

from utils import from_file


class Instruction(NamedTuple):
    num_crates: int
    stack_from: int
    stack_to: int


if __name__ == "__main__":
    puzzle_input = from_file.get_input_for(5, strip_chars="\n")
    if puzzle_input == None:
        sys.exit(1)

    crate_stacks: dict[int, list[str]] = {}

    # Parse the lines to get the stack input
    total_lines = len(puzzle_input)
    i = 0
    while i < total_lines:
        line = puzzle_input[i]
        # The first line we reach which doesn't have any entry marks the end of
        # the stack info and beginning of the instructions lines
        if len(line) == 0:
            break
        i += 1

    # Get the keys first for the different stacks
    for k in puzzle_input[i - 1].split():
        crate_stacks[int(k)] = []

    # Fill up the stacks with the crate elements
    j = i - 2
    while j >= 0:
        line = puzzle_input[j]
        k = 1
        l = 1
        while k < len(line):
            c = line[k]
            if c != " ":
                crate_stacks[l].append(c)
            l += 1
            k += 4
        j -= 1

    instructions: list[Instruction] = []
    # Parse statements to fill up the instrcutions
    i += 1
    while i < total_lines:
        m = re.fullmatch(r"move (\d+) from (\d+) to (\d+)", puzzle_input[i])
        instructions.append(
            Instruction(
                num_crates=int(m.group(1)),
                stack_from=int(m.group(2)),
                stack_to=int(m.group(3)),
            )
        )
        i += 1

    # Save a backup, will be used for the second part
    crate_stacks_backup = deepcopy(crate_stacks)

    # Part 1 - Move crates with first type of crane
    for inst in instructions:
        total_crates_src = len(crate_stacks[inst.stack_from])

        # Get the items from the source stack
        src_items = crate_stacks[inst.stack_from][total_crates_src - inst.num_crates :]
        # Reverse it, since we are taking it one after another
        src_items.reverse()
        # Place it in the destionation stack
        crate_stacks[inst.stack_to].extend(src_items)
        # Clean up the source stack
        crate_stacks[inst.stack_from] = crate_stacks[inst.stack_from][
            : total_crates_src - inst.num_crates
        ]
    # Resulting top items from all stacks after instructions are executed
    print("".join([crate_stacks[k][-1] for k in crate_stacks]))

    # Get back initial state of crates from our backup
    crate_stacks = crate_stacks_backup

    # Part 2 - Move crates with second type of crane
    for inst in instructions:
        total_crates_src = len(crate_stacks[inst.stack_from])

        # Get the items from the source stack
        src_items = crate_stacks[inst.stack_from][total_crates_src - inst.num_crates :]
        # Place it in the destionation stack
        crate_stacks[inst.stack_to].extend(src_items)
        # Clean up the source stack
        crate_stacks[inst.stack_from] = crate_stacks[inst.stack_from][
            : total_crates_src - inst.num_crates
        ]
    # Resulting top items from all stacks after instructions are executed
    print("".join([crate_stacks[k][-1] for k in crate_stacks]))
