import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from typing import NamedTuple

from utils import from_file


class ElfSectionLimits(NamedTuple):
    lower: int
    upper: int


class ElfGroup(NamedTuple):
    first: ElfSectionLimits
    second: ElfSectionLimits


def check_n_in_range(n: int, range: ElfSectionLimits) -> bool:
    return n >= range.lower and n <= range.upper


if __name__ == "__main__":
    section_assignments = from_file.get_input_for(4)
    if section_assignments == None:
        print("day4/input.txt file not found")
        sys.exit(1)

    elf_groups: list[ElfGroup] = []
    for group_line in section_assignments:
        first_section, second_section = group_line.split(",")
        elf_groups.append(
            ElfGroup(
                first=ElfSectionLimits(*map(int, first_section.split("-"))),
                second=ElfSectionLimits(*map(int, second_section.split("-"))),
            )
        )

    # Part 1 - Find completely overlapping pairs among group sections
    total_overlaps = 0

    for group in elf_groups:
        first_section_limits = group.first
        second_section_limits = group.second

        if (
            first_section_limits.lower >= second_section_limits.lower
            and first_section_limits.upper <= second_section_limits.upper
        ) or (
            second_section_limits.lower >= first_section_limits.lower
            and second_section_limits.upper <= first_section_limits.upper
        ):
            total_overlaps += 1

    # Total complete overlaps between two sections
    print(total_overlaps)

    # Part 2 - Find atleast one overlapping pairs among group sections
    total_overlaps = 0

    for group in elf_groups:
        first_section_limits = group.first
        second_section_limits = group.second

        if any(
            [
                check_n_in_range(first_section_limits.lower, second_section_limits),
                check_n_in_range(first_section_limits.upper, second_section_limits),
                check_n_in_range(second_section_limits.lower, first_section_limits),
                check_n_in_range(second_section_limits.upper, first_section_limits),
            ]
        ):
            total_overlaps += 1

    # Total partial overlaps between two sections
    print(total_overlaps)
