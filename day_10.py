import math
import copy

input = """
.#....#.###.........#..##.###.#.....##...
...........##.......#.#...#...#..#....#..
...#....##..##.......#..........###..#...
....#....####......#..#.#........#.......
...............##..#....#...##..#...#..#.
..#....#....#..#.....#.#......#..#...#...
.....#.#....#.#...##.........#...#.......
#...##.#.#...#.......#....#........#.....
....##........#....#..........#.......#..
..##..........##.....#....#.........#....
...#..##......#..#.#.#...#...............
..#.##.........#...#.#.....#........#....
#.#.#.#......#.#...##...#.........##....#
.#....#..#.....#.#......##.##...#.......#
..#..##.....#..#.........#...##.....#..#.
##.#...#.#.#.#.#.#.........#..#...#.##...
.#.....#......##..#.#..#....#....#####...
........#...##...#.....#.......#....#.#.#
#......#..#..#.#.#....##..#......###.....
............#..#.#.#....#.....##..#......
...#.#.....#..#.......#..#.#............#
.#.#.....#..##.....#..#..............#...
.#.#....##.....#......##..#...#......#...
.......#..........#.###....#.#...##.#....
.....##.#..#.....#.#.#......#...##..#.#..
.#....#...#.#.#.......##.#.........#.#...
##.........#............#.#......#....#..
.#......#.............#.#......#.........
.......#...##........#...##......#....#..
#..#.....#.#...##.#.#......##...#.#..#...
#....##...#.#........#..........##.......
..#.#.....#.....###.#..#.........#......#
......##.#...#.#..#..#.##..............#.
.......##.#..#.#.............#..#.#......
...#....##.##..#..#..#.....#...##.#......
#....#..#.#....#...###...#.#.......#.....
.#..#...#......##.#..#..#........#....#..
..#.##.#...#......###.....#.#........##..
#.##.###.........#...##.....#..#....#.#..
..........#...#..##..#..##....#.........#
..#..#....###..........##..#...#...#..#..
"""
# input = """
# .#..#
# .....
# #####
# ....#
# ...##
# """

def build_asteriod_map(asteriod_string):
    array = list(asteriod_string)
    del(array[0])
    map_width = array.index('\n')
    filtered_map = list(filter('\n'.__ne__, array))
    rows = []
    for i in range(map_width):
        rows += [[filtered_map[map_index] for map_index in range(i * map_width, (i + 1) * map_width)]]
    return rows

def build_asteriod_map_with_visible_asteriods(asteriod_map):
    visible_map = copy.deepcopy(asteriod_map)
    max_visible = 0
    max_visible_coordinates = None
    for y, row in enumerate(asteriod_map):
        for x, value in enumerate(row):
            if asteriod_map[y][x] == '#':
                asteriod = Asteriod(copy.deepcopy(asteriod_map), [x, y])
                visible_count = asteriod.visible_asteriods_count()
                visible_map[y][x] = str(visible_count)
                if visible_count > max_visible:
                    max_visible = visible_count
                    max_visible_coordinates = asteriod.coordinates

    return [visible_map, max_visible, max_visible_coordinates]

def print_map(map):
    for row in map:
        print(''.join(row))

class Asteriod():
    def __init__(self, map, coordinates):
        self.map = map
        self.coordinates = coordinates
        self.build_relations()

    def build_relations(self):
        self.asteroid_relationships = []
        for y, row in enumerate(self.map):
            for x, value in enumerate(row):
                coordinates = [x, y]
                if value == '#' and self.coordinates != coordinates:
                    delta_x = coordinates[0] - self.coordinates[0]
                    delta_y = coordinates[1] - self.coordinates[1]
                    # convert to degrees (remember the y coordinates here are flipped) from due 'north'
                    degrees_between_coordinates = (math.atan2(delta_y, delta_x) * 180 / math.pi + 90) % 360
                    distance_between_coordinates = math.sqrt(delta_x**2 + delta_y**2)
                    self.asteroid_relationships += [{'coordinates': coordinates,
                                                     'degrees': degrees_between_coordinates,
                                                     'distance': distance_between_coordinates}]
                    self.asteroid_relationships.sort(key=lambda a: (a['degrees'], a['distance']))

    def visible_asteriods_count(self):
        hidden_asteriod_indices = []
        visible_asteriod_indicies = []
        for i, asteriod in enumerate(self.asteroid_relationships):
            if i in hidden_asteriod_indices:
                continue
            visible_asteriod_indicies += [i]

            for other_index, other_asteriod in enumerate(self.asteroid_relationships):
                if other_asteriod == asteriod:
                    continue
                if other_asteriod['degrees'] == asteriod['degrees']:
                    hidden_asteriod_indices += [other_index]

        return visible_asteriod_indicies.__len__()


class Station(Asteriod):
    def __init__(self, map, coordinates):
        Asteriod.__init__(self, map, coordinates)
        self.laser_degrees = 0
        self.destroyed_asteriods_indices = []

    def fire_in_full_circle(self):
        last_visited_degree = -1
        for index, asteriod_relationship in enumerate(self.asteroid_relationships):
            if index in self.destroyed_asteriods_indices:
                continue
            if asteriod_relationship['degrees'] <= last_visited_degree:
                continue
            self.destroyed_asteriods_indices += [index]
            last_visited_degree = asteriod_relationship['degrees']

asteriod_map = build_asteriod_map(input)
# print_map(asteriod_map)

# Challenge 1 solution
# visible_map, max_visible, max_visible_coordinates = build_asteriod_map_with_visible_asteriods(asteriod_map)
# print(visible_map)
# print_map(visible_map)
# print(f'Max visible at {max_visible_coordinates} with {max_visible}')
# Answer: Max visible at [28, 29] with 340

# Challenge 2
station = Station(copy.deepcopy(asteriod_map), [28, 29])
print(station.asteroid_relationships)
print(station.fire_in_full_circle())
print(station.destroyed_asteriods_indices)
two_hundreth_destroyed_index = station.destroyed_asteriods_indices[199]
two_hundreth_destroyed = station.asteroid_relationships[two_hundreth_destroyed_index]
two_hundreth_destroyed_coordinates = two_hundreth_destroyed['coordinates']
print(two_hundreth_destroyed_coordinates[0] * 100 + two_hundreth_destroyed_coordinates[1])
