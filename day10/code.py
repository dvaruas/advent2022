import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file

if __name__ == "__main__":
    instructions_lines = from_file.get_input_for(10)
    if instructions_lines == None:
        sys.exit(1)

    # Part 1 - Find the total signal strength for some cycles
    # Cycle numbers start at 20 and then are at the difference of 40
    total_signal_strength = 0

    # Part 2 - Find the rendered output in the CRT screen
    screen: list[list[str]] = []
    screen_line: list[str] = []

    # Current cycle number we are at
    cycle_number = 0
    # Value of the register
    x = 1

    i = 0
    inside_addx_cycle = False
    while i < len(instructions_lines):
        # At each iteration we are at a new cycle
        cycle_number += 1

        # Part 1 - adding up to the total signal strength
        if (cycle_number - 20) % 40 == 0:
            total_signal_strength += cycle_number * x

        # Part 2 - determining whether a screen pixel will be lit or not
        pixel_position = (cycle_number - 1) % 40
        if pixel_position == 0 and len(screen_line) != 0:
            # Time to switch to a new line on the screen
            screen.append(screen_line)
            screen_line = []
        if abs(pixel_position - x) <= 1:
            screen_line.append("#")
        else:
            screen_line.append(".")

        line = instructions_lines[i]
        if line == "noop":
            i += 1
        elif inside_addx_cycle:
            # We got in the  addx cycle last cycle, time to wrap it up
            inside_addx_cycle = False
            x += int(line.split()[1])
            i += 1
        else:
            # We are beginning a new addx cycle, which will be over in the next cycle
            inside_addx_cycle = True

    # No time to forget the last screen line we rendered before
    screen.append(screen_line)

    # The total strength, sum of all the relevant cycle metrics
    print(total_signal_strength)

    # The rendered screen output
    [print("".join(screen_line)) for screen_line in screen]
