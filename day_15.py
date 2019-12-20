import copy
from collections import deque

program = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,102,1,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1002,1034,1,1039,101,0,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,101,0,1035,1040,1001,1038,0,1043,1001,1037,0,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,37,1032,1006,1032,165,1008,1040,37,1032,1006,1032,165,1102,1,2,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1101,1,0,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,73,1044,1105,1,224,1102,1,0,1044,1105,1,224,1006,1044,247,1002,1039,1,1034,1001,1040,0,1035,101,0,1041,1036,101,0,1043,1038,101,0,1042,1037,4,1044,1105,1,0,58,87,52,69,28,16,88,43,75,16,91,2,94,51,62,80,96,46,64,98,72,8,54,71,47,84,88,44,81,7,90,13,80,42,62,68,85,27,34,2,13,89,87,79,63,76,9,82,58,60,93,63,78,79,43,32,84,25,34,80,87,15,89,96,1,50,75,25,67,82,27,3,89,48,99,33,36,77,86,62,99,19,86,92,6,56,24,96,2,79,9,3,84,41,94,79,76,91,66,50,82,88,85,13,88,18,93,79,12,98,46,75,52,99,95,11,16,25,17,77,55,87,17,74,76,81,41,77,80,92,46,20,99,22,16,41,90,64,89,53,3,61,88,97,14,2,33,79,62,79,90,80,77,71,45,40,51,62,67,82,42,27,97,17,72,77,12,38,97,85,85,35,92,82,3,84,96,40,27,93,96,18,45,98,16,49,82,52,90,43,81,10,88,94,15,42,77,67,84,88,51,35,84,20,99,7,9,79,65,86,39,93,52,98,11,19,83,75,92,27,72,77,77,78,99,18,53,35,75,14,23,90,15,83,15,98,74,14,75,67,98,93,64,97,97,58,77,88,28,19,1,82,96,69,92,34,1,90,45,79,27,25,85,59,89,88,13,91,93,38,95,55,24,61,79,56,63,61,80,10,76,84,24,80,41,83,37,86,81,93,53,33,75,78,6,81,66,84,98,3,37,84,48,89,88,70,93,96,17,94,38,82,39,74,65,90,9,77,55,53,78,10,98,27,96,11,18,86,54,98,53,86,66,19,93,52,99,44,85,79,19,7,53,86,13,90,46,33,86,19,52,79,60,92,94,97,4,99,83,67,84,58,10,96,5,91,75,47,74,93,68,76,74,50,45,99,15,85,13,99,96,30,99,84,59,81,51,64,74,9,27,2,99,34,49,76,61,28,87,56,84,81,32,6,88,48,57,89,43,76,77,15,80,91,45,9,6,52,93,84,77,17,82,32,67,97,92,74,54,46,99,80,5,83,74,85,64,89,36,41,77,47,94,24,86,45,23,99,59,90,43,61,95,98,91,90,33,91,15,19,88,49,54,86,75,42,67,43,54,97,10,10,42,85,10,11,60,76,17,90,43,80,80,34,90,85,71,70,40,80,97,31,55,80,3,58,99,31,31,99,31,90,90,57,29,85,76,22,14,77,76,87,21,88,77,85,33,81,77,94,57,56,18,83,54,90,90,2,89,87,36,13,85,36,85,70,96,20,85,82,43,34,97,93,27,40,44,80,97,2,81,16,44,12,91,35,90,24,49,75,71,96,5,29,65,80,87,35,51,92,43,94,30,84,88,10,99,4,71,76,65,77,71,1,89,90,58,28,77,42,57,81,87,13,16,72,74,32,98,83,8,75,79,10,96,11,92,34,84,13,1,77,78,71,21,63,78,37,98,86,53,84,75,1,60,75,66,86,22,78,32,31,78,97,97,89,23,88,78,4,75,59,99,65,13,85,70,74,77,83,39,62,76,81,33,98,87,25,41,90,48,42,33,24,94,86,15,94,89,21,23,81,29,36,99,93,60,20,90,19,66,52,90,80,97,95,21,86,45,80,78,7,37,80,84,22,6,97,79,34,87,27,43,52,97,84,72,9,89,93,2,75,82,60,92,12,87,89,59,74,64,90,38,71,89,12,26,81,6,53,78,96,8,81,91,69,68,89,76,79,50,77,19,83,14,75,26,76,34,78,1,83,70,80,39,99,62,95,89,99,6,79,93,80,10,83,50,79,80,92,41,78,20,86,9,84,53,87,13,74,0,0,21,21,1,10,1,0,0,0,0,0,0]

class PrintColors:
    EMPTY = '\033[95m'
    WALL = '\033[94m'
    FLOOR = '\033[93m'
    CURRENT_LOCATION = '\033[92m'
    OXYGEN_SYSTEM = '\033[90m'
    STARTING_LOCATION = '\033[96m'

class Intcode:
    def __init__(self, program):
        self.i = 0
        self.program = program.copy()
        self.input = None
        self.relative_base = 0
        self.halted = False

    def read_parameter_value(self, parameter, mode):
        # position mode
        if mode == 0:
            index = parameter
            self.expand_memory_space(index)
            return self.program[index]
        # immediate mode
        elif mode == 1:
            return parameter
        # relative mode
        elif mode == 2:
            index = self.relative_base + parameter
            self.expand_memory_space(index)
            return self.program[index]
        else:
            print('Invalid parameter value')

    def write_parameter_address(self, parameter, mode):
        # position mode
        if mode == 0:
            index = parameter
            self.expand_memory_space(index)
            return index
        # relative mode
        elif mode == 2:
            index = self.relative_base + parameter
            self.expand_memory_space(index)
            return index
        else:
            print('Invalid parameter value')

    def opcode_setting(self):
        opcode_setting_string = str(self.program[self.i])
        return opcode_setting_string.zfill(5)

    def opcode_and_parameter_modes(self, parameters):
        opcode = int(''.join([parameters[3], parameters[4]]))
        parameter1Mode = int(parameters[2])
        parameter2Mode = int(parameters[1])
        parameter3Mode = int(parameters[0])

        return [opcode, parameter1Mode, parameter2Mode, parameter3Mode]

    def expand_memory_space(self, index):
        if index >= self.program.__len__():
            required_padding = index - self.program.__len__() + 1
            self.program += [0] * required_padding

    def assign_to_address(self, index, value):
        self.expand_memory_space(index)
        self.program[index] = value

    def run(self):
        self.waiting_for_input = False
        output = None

        while True:
            opcode_setting = self.opcode_setting()
            opcode, parameter1Mode, parameter2Mode, parameter3Mode = self.opcode_and_parameter_modes(opcode_setting)

            if len(self.program) > (self.i + 1):
                parameter1 = int(self.program[self.i + 1])
            if len(self.program) > (self.i + 3):
                parameter2 = int(self.program[self.i + 2])
                parameter3 = int(self.program[self.i + 3])

            if opcode == 1:  # addition
                value1 = self.read_parameter_value(parameter1, parameter1Mode)
                value2 = self.read_parameter_value(parameter2, parameter2Mode)
                destination_address = self.write_parameter_address(parameter3, parameter3Mode)
                self.assign_to_address(destination_address, value1 + value2)
                self.i += 4

            elif opcode == 2:  # multiplication
                value1 = self.read_parameter_value(parameter1, parameter1Mode)
                value2 = self.read_parameter_value(parameter2, parameter2Mode)
                destination_address = self.write_parameter_address(parameter3, parameter3Mode)
                self.assign_to_address(destination_address, value1 * value2)
                self.i += 4

            elif opcode == 3:  # takes input and saves to parameter address
                if self.input is None:
                    self.waiting_for_input = True
                    break
                destination_address = self.write_parameter_address(parameter1, parameter1Mode)
                self.assign_to_address(destination_address, self.input)
                self.input = None
                self.i += 2

            elif opcode == 4:  # outputs the value of the parameter, stops program
                value1 = self.read_parameter_value(parameter1, parameter1Mode)
                output = value1  # does an output
                self.i += 2
                break

            elif opcode == 5:  # jump if true
                value1 = self.read_parameter_value(parameter1, parameter1Mode)
                value2 = self.read_parameter_value(parameter2, parameter2Mode)
                if value1 != 0:
                    self.i = value2
                else:
                    self.i += 3

            elif opcode == 6:  # jump if false
                value1 = self.read_parameter_value(parameter1, parameter1Mode)
                value2 = self.read_parameter_value(parameter2, parameter2Mode)
                if value1 == 0:
                    self.i = value2
                else:
                    self.i += 3

            elif opcode == 7:  # less than
                value1 = self.read_parameter_value(parameter1, parameter1Mode)
                value2 = self.read_parameter_value(parameter2, parameter2Mode)
                destination_address = self.write_parameter_address(parameter3, parameter3Mode)
                if value1 < value2:
                    self.assign_to_address(destination_address, 1)
                else:
                    self.assign_to_address(destination_address, 0)
                self.i += 4

            elif opcode == 8:  # equal to
                value1 = self.read_parameter_value(parameter1, parameter1Mode)
                value2 = self.read_parameter_value(parameter2, parameter2Mode)
                destination_address = self.write_parameter_address(parameter3, parameter3Mode)
                if value1 == value2:
                    self.assign_to_address(destination_address, 1)
                else:
                    self.assign_to_address(destination_address, 0)
                self.i += 4

            elif opcode == 9:  # relative base adjustment
                self.relative_base += self.read_parameter_value(parameter1, parameter1Mode)
                self.i += 2

            elif opcode == 99:
                print('HALTED')
                self.halted = True
                break

            else:
                print(f'Invalid opcode at {self.i}')
                break

        return output


class Robot:
    FLOOR = 'FLOOR'
    WALL = 'WALL'
    OXYGEN_SYSTEM = 'OXYGEN SYSTEM'
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def __init__(self, program):
        self.program = program
        self.intcode = Intcode(self.program)
        self.current_location = [0, 0]
        self.desired_location = None
        self.desired_direction = None
        self.current_direction = Robot.NORTH
        self.locations = {str(self.current_location): Robot.FLOOR}
        self.visited_locations = []
        self.all_visited_locations = []

    def find_oxygen_panel(self):
        i = 0
        while True:
            self.intcode_outputs = []
            while True:
                output = self.intcode.run()
                self.intcode_outputs.append(output)
                if self.intcode.halted or self.intcode.waiting_for_input:
                    break
            self.update_locations()
            self.make_command()

            i += 1
            if i % 50 == 0:
                self.print_screen()

            if self.locations[str(self.current_location)] == Robot.OXYGEN_SYSTEM:
                self.print_screen()
                print(f'Visited locations {self.visited_locations}')
                print(f'Min of steps: {self.min_movements_to_oxygen_panel()}')
                break

    def chart_full_map(self):
        i = 0

        while True:
            self.intcode_outputs = []
            while True:
                output = self.intcode.run()
                self.intcode_outputs.append(output)
                if self.intcode.halted or self.intcode.waiting_for_input:
                    break
            self.update_locations()
            self.make_exploratory_command()

            i += 1

            # this is hacky, but I know it is fully explored at 3000 from trial and error
            if i == 3000:
                self.print_screen()
                break

    def update_locations(self):
        # 0: The repair droid hit a wall. Its position has not changed.
        # 1: The repair droid has moved one step in the requested direction.
        # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.

        if self.intcode_outputs[0] == 0:
            if not str(self.desired_location) in self.locations:
                self.locations[str(self.desired_location)] = Robot.WALL
        elif self.intcode_outputs[0] == 1 or self.intcode_outputs[0] == 2:
            if self.intcode_outputs[0] == 1:
                if not str(self.desired_location) in self.locations:
                    self.locations[str(self.desired_location)] = Robot.FLOOR
            elif self.intcode_outputs[0] == 2:
                if not str(self.desired_location) in self.locations:
                    self.locations[str(self.desired_location)] = Robot.OXYGEN_SYSTEM
            self.current_location = self.desired_location
            if self.current_location in self.visited_locations:
                index_to_delete = self.visited_locations.index(self.current_location)
                del self.visited_locations[index_to_delete]
            self.visited_locations.append(self.current_location)
            self.all_visited_locations.append(self.current_location)

        else:
            print(f'Invalid output {self.intcode_outputs}')

    def print_screen(self):
        xs = []
        ys = []
        tiles = []
        for location in self.locations.keys():
            x, y = location.__str__().replace('[', '').replace(']', '').split(', ')
            xs.append(int(x))
            ys.append(int(y))

        # init tiles
        row_count = max(ys) - min(ys) + 1
        width = max(xs) - min(xs) + 1
        y_offset = 0
        if min(ys) < 0:
            y_offset = abs(min(ys))
        x_offset = 0
        if min(xs) < 0:
            x_offset = abs(min(xs))

        for i in range(row_count):
            tiles.append([f"{PrintColors.EMPTY}█"] * width)

        for location_key in self.locations.keys():
            x, y = location_key.__str__().replace('[', '').replace(']', '').split(', ')
            x = int(x) + x_offset
            y = int(y) + y_offset
            if location_key == '[0, 0]':
                tiles[y][x] = f"{PrintColors.STARTING_LOCATION}X"
            elif self.locations[location_key] == Robot.WALL:
                tiles[y][x] = f"{PrintColors.WALL}█"
            elif self.locations[location_key] == Robot.FLOOR:
                tiles[y][x] = f"{PrintColors.FLOOR}█"
            elif self.locations[location_key] == Robot.OXYGEN_SYSTEM:
                tiles[y][x] = f"{PrintColors.OXYGEN_SYSTEM}█"
        x, y = self.current_location.__str__().replace('[', '').replace(']', '').split(', ')
        tiles[int(y) + y_offset][int(x) + x_offset] = f"{PrintColors.CURRENT_LOCATION}█"

        print('-------')
        tiles.reverse()
        for row in tiles:
            print(''.join(row))

    def make_command(self):
        self.desired_direction = None
        self.desired_location = None

        north_location = [self.current_location[0], self.current_location[1] + 1]
        east_location = [self.current_location[0] + 1, self.current_location[1]]
        south_location = [self.current_location[0], self.current_location[1] - 1]
        west_location = [self.current_location[0] - 1, self.current_location[1]]

        decisions = [[north_location, Robot.NORTH],
                     [east_location, Robot.EAST],
                     [south_location, Robot.SOUTH],
                     [west_location, Robot.WEST]]

        # go to next adjacent unexplored
        for location, input_instruction in decisions:
            if str(location) not in self.locations.keys():
                self.desired_location = location
                self.desired_direction = input_instruction
                self.intcode.input = input_instruction
                return
        if self.desired_location:
            return

        # go to non-wall neighbor in the floor least recently traveled
        non_wall_option_locations = []
        for location, input_instruction in decisions:
            if self.locations[str(location)] != Robot.WALL:
                non_wall_option_locations.append(location)

        if non_wall_option_locations.__len__() != 0:
            location = min(non_wall_option_locations, key=lambda x: self.visited_locations.index(x))
            input_instruction = next(decision[1] for decision in decisions if decision[0] == location)

            self.desired_location = location
            self.desired_direction = input_instruction
            self.intcode.input = input_instruction
            return
        if self.desired_location:
            return

        # go in the direction of the next non-wall
        for location, input_instruction in decisions:
            if self.locations[str(location)] != Robot.WALL:
                self.desired_location = location
                self.desired_direction = input_instruction
                self.intcode.input = input_instruction
                return
        if self.desired_location:
            return

        assert(False)

    def make_exploratory_command(self):
        # Idea: explore the whole map by making only right movements
        # set current direction
        # get decisions starting w/ right to backwards
        # travel to the first one found that is unexplored or floor

        if self.current_location == self.desired_location:
            self.current_direction = self.desired_direction

        decisions = self.decisions_with_right_priority()

        # otherwise, rotate to the right until finding unexplored or FLOOR
        for location, input_instruction in decisions:
            if str(location) not in self.locations or self.locations[str(location)] == Robot.FLOOR:
                self.desired_location = location
                self.desired_direction = input_instruction
                self.intcode.input = input_instruction
                return
        if self.desired_location:
            return
        assert(False)

    def min_movements_to_oxygen_panel(self):
        combined_locations = list(map(lambda x: x[0] * 10_000 + x[1], self.all_visited_locations))
        unique_count = len(set(combined_locations))
        all_count = len(self.all_visited_locations)
        return (unique_count - (all_count - unique_count))

    def decisions_with_right_priority(self):
        north_location = [self.current_location[0], self.current_location[1] + 1]
        east_location = [self.current_location[0] + 1, self.current_location[1]]
        south_location = [self.current_location[0], self.current_location[1] - 1]
        west_location = [self.current_location[0] - 1, self.current_location[1]]

        decisions = deque([[north_location, Robot.NORTH],
                           [west_location, Robot.WEST],
                           [south_location, Robot.SOUTH],
                           [east_location, Robot.EAST]])

        if self.current_direction == Robot.NORTH:
            shift_amount = 1
        elif self.current_direction == Robot.EAST:
            shift_amount = 2
        elif self.current_direction == Robot.SOUTH:
            shift_amount = 3
        else:
            shift_amount = 0

        return decisions.rotate(shift_amount) or decisions


class OxygenMapper:
    def __init__(self, location, oxygen_system_coordinates):
        self.locations = location
        x, y = oxygen_system_coordinates.replace('[', '').replace(']', '').split(', ')
        self.oxygen_system_coordinates = [int(x), int(y)]

    def fill_time(self):
        self.filled_locations = []
        self.filling_locations = [self.oxygen_system_coordinates]
        time = 0
        while self.filling_locations.__len__() != 0:
            self.filled_locations += self.filling_locations
            new_filling_locations = []
            for filling_location in self.filling_locations:
                new_filling_locations += self.adjacent_empty_locations(filling_location)
            self.filling_locations = new_filling_locations
            time += 1
        return time - 1

    def adjacent_empty_locations(self, location):
        x = location[0]
        y = location[1]
        adjacent_locations = [[x + 1, y],
                              [x - 1, y],
                              [x, y + 1],
                              [x, y - 1]]
        adjacent_empty_locations = [location for location in adjacent_locations
                                    if location in self.locations
                                    and location not in self.filled_locations
                                    and location not in self.filling_locations]
        return adjacent_empty_locations


# part 1
# robot = Robot(program)
# robot.find_oxygen_panel()

# part 2
robot = Robot(program)
robot.chart_full_map()
locations = robot.visited_locations
oxygen_system_location = [key for key in robot.locations.keys() if robot.locations[key] == Robot.OXYGEN_SYSTEM][0]
calculator = OxygenMapper(locations, oxygen_system_location)
print(calculator.fill_time())
