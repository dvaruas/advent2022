from __future__ import annotations

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from functools import reduce
from typing import Optional

from utils import from_file


class Node:
    name: str
    parent: Optional[Node]
    children: list[Node]
    __size: Optional[int]

    def __init__(
        self, name: str, size: Optional[int] = None, parent: Optional[Node] = None
    ) -> None:
        self.name = name
        self.parent = parent
        self.children = []
        self.__size = size

    @property
    def is_dir(self) -> bool:
        return len(self.children) != 0

    @property
    def size(self) -> int:
        if self.__size != None:
            return self.__size
        self.__size = sum([c.size for c in self.children])
        return self.__size

    def get_or_add_child(self, name: str, size: Optional[int] = None) -> Node:
        for c in self.children:
            if c.name == name:
                # This child already exists at this level, just return it
                return c
        # Did not find an existing child, create a new one
        n = Node(name, size=size, parent=self)
        self.children.append(n)
        return n

    def print_node(self, level: Optional[int] = 0):
        print(
            "{}{} (size: {}, children: {})".format(
                "|" * level, self.name, self.size, len(self.children)
            )
        )
        for c in self.children:
            c.print_node(level=level + 1)


if __name__ == "__main__":
    puzzle_input = from_file.get_input_for(7)
    if puzzle_input == None:
        sys.exit(1)

    # We always start at the root
    head = Node("/")
    temp = head

    for line in puzzle_input[1:]:
        if line.startswith("$"):
            # This is a command line
            command_type = line[2:4]
            if command_type == "cd":
                # This is a change of directory command.
                if line[5:] == "..":
                    # Option 1 : going one step back, move to the parent
                    head = head.parent
                # Option 2 : going one step forward into a sub-directory
                else:
                    head = head.get_or_add_child(line[5:])
            else:
                # It is otherwise a list command, we don't care about these
                pass
        else:
            # These contain important info about contents of dir
            part_one, part_two = line.split()
            if part_one == "dir":
                # This is a sub directory, try to add a node with that name
                head.get_or_add_child(part_two)
            else:
                # This is a file with contents information inside this directory
                head.get_or_add_child(name=part_two, size=int(part_one))

    # Print out the parsed directory structure to check if everything is fine
    # temp.print_node()

    # Part 1 - Find the sum of sizes of all directories with atmost 100000 size
    head = temp

    def get_total_size_over(n: Node) -> int:
        total = 0
        if n.is_dir:
            if n.size <= 100000:
                total += n.size
            total += sum([get_total_size_over(c) for c in n.children])
        return total

    # Total size of all files which are over 100000
    print(get_total_size_over(head))

    # Part 2 - Find the directory to delete which will increase unused space to atleast 30000000
    head = temp
    total_disk_space = 70000000  # Given
    free_space_available = total_disk_space - head.size
    free_space_required = 30000000 - free_space_available

    def find_candidate_dirs_over(n: Node) -> list[Node]:
        candidate_dirs: list[Node] = []
        if n.is_dir:
            if n.size >= free_space_required:
                candidate_dirs.append(n)
            for c in n.children:
                candidate_dirs.extend(find_candidate_dirs_over(c))
        return candidate_dirs

    all_candidate_dirs = find_candidate_dirs_over(head)
    dir_to_remove: Node = reduce(
        lambda x, y: x if x.size < y.size else y, all_candidate_dirs
    )

    # Size of the smallest directory satisfying our criteria which we choose to remove finally
    print(dir_to_remove.size)
