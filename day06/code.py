import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file


# Returns the ending index for the window containing only unique elements
def find_unique_window_end(data_stream: str, window_size: int) -> int:
    window_start = 0
    window_end = window_size
    total_chars_in_stream = len(data_stream)

    while window_end <= total_chars_in_stream:
        window_elems = set(data_stream[window_start:window_end])
        if len(window_elems) == window_size:
            return window_end

        window_end += 1
        window_start += 1

    return -1


if __name__ == "__main__":
    puzzle_input = from_file.get_input_for(6)
    if puzzle_input == None:
        sys.exit(1)

    # There's only a single line containing the data stream
    data_stream = puzzle_input[0]

    # Part 1 - Number of characters to process before beginning of packet marker
    # is detected.
    print(find_unique_window_end(data_stream, 4))

    # Part 2 - Number of characters to process before beginning of message is
    # detected.
    print(find_unique_window_end(data_stream, 14))
