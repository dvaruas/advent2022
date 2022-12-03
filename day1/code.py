import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file

if __name__ == "__main__":
    calorie_inputs = from_file.get_input_for(1)
    if calorie_inputs == None:
        print("day1/input.txt file not found")
        sys.exit(1)

    calories_list: list[int] = []

    current_elf_calories = 0
    for input_line in calorie_inputs:
        if input_line == "":
            # This marks the beginning of a new elfs calorie count.
            # Save all info for the previous one
            calories_list.append(current_elf_calories)
            current_elf_calories = 0
        else:
            # Add on to the current elfs calories
            current_elf_calories += int(input_line)

    # Add the last elfs calories as well to the list
    calories_list.append(current_elf_calories)

    calories_list = sorted(calories_list, reverse=True)

    # Part 1 - Elf carrying the most calories
    print(calories_list[0])

    # part 2 - Total calories carried by top 3 elves
    print(sum(calories_list[:3]))
