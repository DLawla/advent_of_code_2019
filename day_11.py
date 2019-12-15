program = [3,8,1005,8,290,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,28,1006,0,59,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,53,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,76,1006,0,81,1,1005,2,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,105,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,126,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,148,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,171,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,193,1,1008,8,10,1,106,3,10,1006,0,18,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,225,1,1009,9,10,1006,0,92,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,254,2,1001,8,10,1,106,11,10,2,102,13,10,1006,0,78,101,1,9,9,1007,9,987,10,1005,10,15,99,109,612,104,0,104,1,21102,1,825594852136,1,21101,0,307,0,1106,0,411,21101,0,825326580628,1,21101,0,318,0,1105,1,411,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,179557207043,1,1,21101,0,365,0,1106,0,411,21101,0,46213012483,1,21102,376,1,0,1106,0,411,3,10,104,0,104,0,3,10,104,0,104,0,21101,988648727316,0,1,21102,399,1,0,1105,1,411,21102,988224959252,1,1,21101,0,410,0,1106,0,411,99,109,2,21201,-1,0,1,21101,0,40,2,21102,1,442,3,21101,432,0,0,1105,1,475,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,437,438,453,4,0,1001,437,1,437,108,4,437,10,1006,10,469,1102,0,1,437,109,-2,2105,1,0,0,109,4,2102,1,-1,474,1207,-3,0,10,1006,10,492,21101,0,0,-3,21202,-3,1,1,22102,1,-2,2,21101,0,1,3,21102,511,1,0,1105,1,516,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,539,2207,-4,-2,10,1006,10,539,21201,-4,0,-4,1106,0,607,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21101,558,0,0,1106,0,516,22101,0,1,-4,21101,1,0,-1,2207,-4,-2,10,1006,10,577,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,599,21201,-1,0,1,21101,0,599,0,105,1,474,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]

class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Intcode:
    def __init__(self, program, input):
        self.i = 0
        self.program = program.copy()
        self.input = input
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
    def __init__(self, program):
        self.coordinates = [0, 0]
        self.visited_coordinates_information = []
        self.orientation = 0
        self.program = program
        self.intcode = Intcode(program.copy(), None)
        self.halted = False

    def perform_one_tick(self):
        outputs = []

        for i in range(2):
            self.intcode.input = self.color_of_coordinate()
            output = self.intcode.run()
            if self.intcode.halted:
                self.halted = True
                break
            if output is not None:
                outputs += [output]

        if outputs.__len__() == 2:
            painted_color, direction_to_turn = outputs
            self.update_visited_coordinates_information(painted_color)
            self.perform_movement(direction_to_turn)
        else:
            self.halted = True

    def update_visited_coordinates_information(self, color):
        exists = next((info for info in self.visited_coordinates_information if info['coordinates'] == self.coordinates), None)
        if exists:
            for info in self.visited_coordinates_information:
                if info['coordinates'] == self.coordinates:
                    info['color'] = color
                    break
        else:
            self.visited_coordinates_information += [{'coordinates': self.coordinates, 'color': color}]

    def color_of_coordinate(self):
        if self.visited_coordinates_information.__len__() == 0:
            return 1
        matching_coordinates = [c for c in self.visited_coordinates_information if c['coordinates'] == self.coordinates]
        if matching_coordinates.__len__() == 0:
            return 0
        return matching_coordinates[0]['color']

    def perform_movement(self, direction):
        if direction == 0:
            self.orientation = (self.orientation - 1) % 4
        elif direction == 1:
            self.orientation = (self.orientation + 1) % 4

        if self.orientation == 0:
            self.coordinates = [self.coordinates[0], self.coordinates[1] + 1]
        elif self.orientation == 1:
            self.coordinates = [self.coordinates[0] + 1, self.coordinates[1]]
        elif self.orientation == 2:
            self.coordinates = [self.coordinates[0], self.coordinates[1] - 1]
        elif self.orientation == 3:
            self.coordinates = [self.coordinates[0] - 1, self.coordinates[1]]

done = False
robot = Robot(program)

while not done:
    robot.perform_one_tick()
    if robot.halted:
        done = True

print(robot.visited_coordinates_information)
print(robot.visited_coordinates_information.__len__())

all_x_coordinates = []
all_y_coordinates = []
for visited_coordinate_info in robot.visited_coordinates_information:
    all_x_coordinates += [visited_coordinate_info['coordinates'][0]]
    all_y_coordinates += [visited_coordinate_info['coordinates'][1]]
x_offset = abs(min(all_x_coordinates))
y_offset = abs(min(all_y_coordinates))

row_count = max(all_y_coordinates) - min(all_y_coordinates) + 1
width = max(all_x_coordinates) - min(all_x_coordinates) + 1

# init panels for painting
panels = []
for i in range(row_count):
    panels.append([f"{PrintColors.OKGREEN}█"] * width)

# paint panels
for visited_coordinate_info in robot.visited_coordinates_information:
    if visited_coordinate_info['color'] == 1:
        color = f"{PrintColors.FAIL}█"
    else:
        color = f"{PrintColors.OKGREEN}█"
    panels[visited_coordinate_info['coordinates'][1] + y_offset][visited_coordinate_info['coordinates'][0] + x_offset] = color

# Prints answer reflected over x axis
for row in panels:
    print(''.join(row))
