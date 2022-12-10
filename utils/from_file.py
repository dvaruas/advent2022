import os
from typing import Optional

ROOT_PATH = os.path.join(os.path.dirname(__file__), os.pardir)

# Returns the file contents for the day given
# A file with the name "input.txt" should be present inside the dayX directory
def get_input_for(day: int, strip_chars: str = "\n ") -> Optional[list[str]]:
    file_path: str = os.path.join(ROOT_PATH, "day{:02d}".format(day), "input.txt")

    if not os.path.exists(file_path):
        print("{} not found".format(file_path))
        return None

    with open(file_path, "r") as fr:
        return [l.strip(strip_chars) for l in fr.readlines()]


if __name__ == "__main__":
    test_day = 3
    print(get_input_for(test_day))
