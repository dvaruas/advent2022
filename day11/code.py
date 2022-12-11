import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from copy import deepcopy
from re import findall, fullmatch
from typing import Callable

from utils import from_file


class Monkey:
    items: list[int]
    monkey_operation: Callable[[int], int]
    determining_divisor: int
    next_indices: dict[bool, int]
    times_inspected: int

    def __init__(
        self,
        items: list[int],
        monkey_operation: Callable[[int], int],
        determining_divisor: int,
        monkey_index_if_true: int,
        monkey_index_if_false: int,
    ) -> None:
        self.items = items
        self.monkey_operation = monkey_operation
        self.determining_divisor = determining_divisor
        self.next_indices = {True: monkey_index_if_true, False: monkey_index_if_false}
        self.times_inspected = 0

    def get_next_monkey_index(self, item: int) -> int:
        return self.next_indices[item % self.determining_divisor == 0]


def parse_input_lines(puzzle_input: list[str]) -> dict[int, Monkey]:
    monkeys: dict[int, Monkey] = {}

    i = 0
    n = len(puzzle_input)
    while True:
        # The first line is something like -- "Monkey 0:"
        line = puzzle_input[i]
        i += 1
        m = fullmatch(r"Monkey (\d):", line)
        monkey_number = int(m.group(1))

        # The second line is something like -- "Starting items: 79, 98"
        line = puzzle_input[i]
        i += 1
        monkey_items = [int(v) for v in findall(r"\d+", line)]

        # The third line is something like -- Operation: new = old * 19
        line = puzzle_input[i]
        i += 1
        m = fullmatch(r"Operation: new = old ([\*|\+]) (\d+|old)", line)
        operator, the_other_part = m.group(1), m.group(2)
        the_function = None
        if the_other_part == "old":
            if operator == "+":
                the_function = lambda x: 2 * x
            else:
                the_function = lambda x: x * x
        else:
            # It is a number
            if operator == "*":
                the_function = (lambda y: lambda x: x * y)(int(the_other_part))
            else:
                the_function = (lambda y: lambda x: x + y)(int(the_other_part))

        # The fourth line is something like -- Test: divisible by 23
        line = puzzle_input[i]
        i += 1
        m = fullmatch(r"Test: divisible by (\d+)", line)
        divide_by = int(m.group(1))

        # The fifth line is something like -- If true: throw to monkey 2
        line = puzzle_input[i]
        i += 1
        m = fullmatch(r"If true: throw to monkey (\d+)", line)
        throw_to_if_true = int(m.group(1))

        # The sixth line is something like -- If false: throw to monkey 3
        line = puzzle_input[i]
        i += 1
        m = fullmatch(r"If false: throw to monkey (\d+)", line)
        throw_to_if_false = int(m.group(1))

        monkeys[monkey_number] = Monkey(
            items=monkey_items,
            monkey_operation=the_function,
            determining_divisor=divide_by,
            monkey_index_if_true=throw_to_if_true,
            monkey_index_if_false=throw_to_if_false,
        )

        # There exists an empty line after each monkey input
        i += 1

        if i >= n:
            # We have finished parsing all input lines
            break

    return monkeys


if __name__ == "__main__":
    puzzle_input = from_file.get_input_for(11)
    if puzzle_input == None:
        sys.exit(1)

    monkeys = parse_input_lines(puzzle_input=puzzle_input)
    backup = deepcopy(monkeys)
    total_monkeys = len(monkeys)

    # Part 1 - Find level of monkey business after 20 rounds
    total_number_of_rounds = 20

    round_num = 0
    while round_num < total_number_of_rounds:
        monkey_indx = 0
        while monkey_indx < total_monkeys:
            monkey = monkeys[monkey_indx]
            number_of_items = len(monkey.items)
            monkey.times_inspected += number_of_items

            while number_of_items > 0:
                item = monkey.items.pop(0)
                item = monkey.monkey_operation(item)
                item = item // 3  # Calming effect
                next_monkey_indx = monkey.get_next_monkey_index(item)
                monkeys[next_monkey_indx].items.append(item)
                number_of_items -= 1

            # Let's look at the next monkey
            monkey_indx += 1

        round_num += 1

    highest_monkey_indx, second_highest_monkey_indx = sorted(
        monkeys, key=lambda x: monkeys[x].times_inspected, reverse=True
    )[:2]

    # Total monkey business by the two most active monkeys
    print(
        monkeys[highest_monkey_indx].times_inspected
        * monkeys[second_highest_monkey_indx].times_inspected
    )

    monkeys = backup

    # Part 2 - Find level of monkey business after 10000 rounds with no calming effect
    total_number_of_rounds = 10000

    # The trick to keep things under control --
    # (x + a)/n = 1 if and only if ((x % NN) + a)/n = 1
    # (x * a)/n = 1 if and only if ((x % NN) * a)/n = 1
    # Here NN is the LCM of all the divisors which we use
    # So at each iteration of the items we can only store the x%n value to reduce computation effort

    # Find out the lcm for all the divisors
    # Here we directly multiply all the divisors since they are all prime numbers
    lcm = 1
    for monkey in monkeys.values():
        lcm *= monkey.determining_divisor

    round_num = 0
    while round_num < total_number_of_rounds:
        monkey_indx = 0
        while monkey_indx < total_monkeys:
            monkey = monkeys[monkey_indx]
            number_of_items = len(monkey.items)
            monkey.times_inspected += number_of_items

            while number_of_items > 0:
                item = monkey.items.pop(0)
                item = monkey.monkey_operation(item)
                item = item % lcm
                next_monkey_indx = monkey.get_next_monkey_index(item)
                monkeys[next_monkey_indx].items.append(item)
                number_of_items -= 1

            # Let's look at the next monkey
            monkey_indx += 1

        round_num += 1

    highest_monkey_indx, second_highest_monkey_indx = sorted(
        monkeys, key=lambda x: monkeys[x].times_inspected, reverse=True
    )[:2]

    # Total monkey business by the two most active monkeys
    print(
        monkeys[highest_monkey_indx].times_inspected
        * monkeys[second_highest_monkey_indx].times_inspected
    )
