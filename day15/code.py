from __future__ import annotations

import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from re import fullmatch

from utils import from_file


class Point:
    x: int
    y: int

    def __init__(self, x: str | int, y: str | int) -> None:
        self.x = int(x)
        self.y = int(y)

    def distance_from(self, __o: Point) -> int:
        return abs(self.x - __o.x) + abs(self.y - __o.y)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Point):
            return False
        return self.x == __o.x and self.y == __o.y

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)


class Sensor(Point):
    radius: int

    def __init__(self, x: str | int, y: str | int) -> None:
        super().__init__(x, y)
        self.radius = 0

    def within_range(self, __o: Point) -> bool:
        return self.distance_from(__o) <= self.radius


class Beacon(Point):
    pass


def get_distinct_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges = sorted(ranges, key=lambda x: x[0])
    i = 0
    n = len(ranges)

    while i + 1 < n:
        r1 = ranges.pop(i)
        r2 = ranges.pop(i)
        # If r1 is completely at the left of r2
        if r1[1] < r2[0]:
            # They cannot be combined
            ranges = [r1, r2] + ranges
            i += 1
            continue
        # Else they can be combined
        ranges = [(min(r1[0], r2[0]), max(r1[1], r2[1]))] + ranges
        n -= 1

    return ranges


if __name__ == "__main__":
    puzzle_input = from_file.get_input_for(15)
    if puzzle_input == None:
        sys.exit(1)

    sensors: list[Sensor] = []
    beacons: list[Beacon] = []

    # Part 1 -- Find number of positions which cannot contain a beacon at y-line
    total_nb_positions = 0

    y = 2000000
    all_intersecting_ranges = []  # At y-line for all sensors

    for line in puzzle_input:
        m = fullmatch(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )

        # Construct the beacon
        beacon = Beacon(x=m.group(3), y=m.group(4))
        # Beacon information could be repeated, check if we already have encountered this
        if beacon not in beacons:
            beacons.append(beacon)
            # If the beacon is on the line y, that position already has a beacon so it cannot be a non-beacon one
            if beacon.y == y:
                total_nb_positions -= 1

        # Construct the sensor
        sensor = Sensor(x=m.group(1), y=m.group(2))
        sensor.radius = sensor.distance_from(beacon)
        sensors.append(sensor)

        # Find the ranges which the sensor covers in the line y
        ydiff = sensor.y - y if sensor.y > y else y - sensor.y
        if ydiff <= sensor.radius:
            xdiff = sensor.radius - ydiff
            curr_range = (sensor.x - xdiff, sensor.x + xdiff)
            all_intersecting_ranges.append(curr_range)

    # Compose distinct ranges from all the ranges we got till now
    final_ranges = get_distinct_ranges(all_intersecting_ranges)

    for r in final_ranges:
        total_nb_positions += (r[1] - r[0]) + 1

    print(total_nb_positions)

    # Part 2 -- Find tuning frequency by finding the square where a beacon can be present

    potential_sensors: set[Sensor] = set()
    # Find the sensor pairs which have a distance of one between them
    # we would later check only their borders to reduce the search space
    i = 0
    n = len(sensors)
    while i < n:
        j = i + 1
        while j < n:
            s1, s2 = sensors[i], sensors[j]
            dist = s1.distance_from(s2) - s1.radius - s2.radius
            if dist == 2:
                potential_sensors.add(s1)
                potential_sensors.add(s2)
            j += 1
        i += 1

    search_grid: tuple[Point, Point] = (
        Point(0, 0),  # min of the bounding box
        Point(4000000, 4000000),  # max of the bounding box
    )
    is_in_grid = (
        lambda p: search_grid[0].x <= p.x <= search_grid[1].x
        and search_grid[0].y <= p.y <= search_grid[1].y
    )

    beacon_positions: set[Point] = set()

    print(
        "[debug] Number of sensors whose borders we will check: {}".format(
            len(potential_sensors)
        )
    )

    for sensor in potential_sensors:
        print("[debug] For sensor : {}".format(sensor))

        time_one = time.time()

        # Find all points just outside the border of the sensor radius
        all_points: list[Point] = []
        # Side 1
        for i in range(sensor.radius):
            p = Point(sensor.x + i, (sensor.y + sensor.radius + 1) - i)
            all_points.append(p) if is_in_grid(p) else None
        # Side 2
        for i in range(sensor.radius):
            p = Point((sensor.x + sensor.radius + 1) - i, sensor.y + i)
            all_points.append(p) if is_in_grid(p) else None
        # Side 3
        for i in range(sensor.radius):
            p = Point(sensor.x - i, (sensor.y + sensor.radius + 1) - i)
            all_points.append(p) if is_in_grid(p) else None
        # Side 4
        for i in range(sensor.radius):
            p = Point((sensor.x - sensor.radius - 1) + i, sensor.y - i)
            all_points.append(p) if is_in_grid(p) else None

        time_two = time.time()

        # Improvement thoughts --
        # Determine which is the common side (which would have the point) between the two sensors border sides
        # instead of blindly getting all the points for all the borders.
        print(
            "[debug] Time elapsed finding all border points : {:.2f} seconds".format(
                time_two - time_one
            )
        )

        # This part is very costly as well, reducing the number of points in all_points would help this
        for p in all_points:
            for s in sensors:
                if s.within_range(p):
                    break
            else:
                beacon_positions.add(p)

        time_three = time.time()
        print(
            "[debug] Time elapsed checking {} points: {:.2f} seconds".format(
                len(all_points), time_three - time_two
            )
        )

    if len(beacon_positions) != 1:
        print("Something went wrong! There should be only one possible position")
    else:
        b = beacon_positions.pop()
        print(b.x * 4000000 + b.y)
