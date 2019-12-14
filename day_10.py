map = """
.#..#
.....
#####
....#
...##
"""

def build_asteriod_array(asteriod_string):
    array = list(asteriod_string)
    del(array[0])
    map_width = array.index('\n')
    filtered_map = list(filter('\n'.__ne__, array))
    number_of_rows = int(filtered_map.__len__() / map_width)
    rows = []
    for i in range(map_width):
        rows += [[filtered_map[map_index] for map_index in range(i * map_width, (i + 1) * map_width)]]
    return rows

print(build_asteriod_array(map))