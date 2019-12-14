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
                    slope_between_coordinates = math.atan2(delta_y, delta_x)
                    distance_between_coordinates = math.sqrt(delta_x**2 + delta_y**2)
                    self.asteroid_relationships += [{'coordinates': coordinates,
                                                     'slope': slope_between_coordinates,
                                                     'distance': distance_between_coordinates}]
                    self.asteroid_relationships.sort(key=lambda a: a['distance'])

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
                if other_asteriod['slope'] == asteriod['slope']:
                    hidden_asteriod_indices += [other_index]

        return visible_asteriod_indicies.__len__()

asteriod_map = build_asteriod_map(input)
print_map(asteriod_map)
visible_map, max_visible, max_visible_coordinates = build_asteriod_map_with_visible_asteriods(asteriod_map)
print(visible_map)
print_map(visible_map)
print(f'Max visible at {max_visible_coordinates} with {max_visible}')
