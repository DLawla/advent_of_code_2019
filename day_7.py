program = [3,8,1001,8,10,8,105,1,0,0,21,42,67,88,105,114,195,276,357,438,99999,3,9,101,4,9,9,102,3,9,9,1001,9,2,9,102,4,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,101,2,9,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,1001,9,4,9,1002,9,4,9,101,2,9,9,1002,9,2,9,4,9,99,3,9,101,4,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99]



class AmplifierIntcode():
    def __init__(self, program, input, phase_setting):
        self.i = 0
        self.program = program
        self.input = input
        self.phase_setting = phase_setting
        self.phase_input_set = False
        self.halted = False

    def parameter_value(self, parameter, mode):
        if mode == 0:
            return int(self.program[parameter])
        else:
            return parameter


    def opcode_setting(self):
        opcode_setting_string = str(self.program[self.i])
        return opcode_setting_string.zfill(5)


    def opcode_and_parameter_modes(self, parameters):
        opcode = int(''.join([parameters[3], parameters[4]]))
        parameter1Mode = int(parameters[2])
        parameter2Mode = int(parameters[1])
        parameter3Mode = int(parameters[0])

        return [opcode, parameter1Mode, parameter2Mode, parameter3Mode]


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
                value1 = self.parameter_value(parameter1, parameter1Mode)
                value2 = self.parameter_value(parameter2, parameter2Mode)
                self.program[parameter3] = value1 + value2
                self.i += 4

            elif opcode == 2:  # multiplication
                value1 = self.parameter_value(parameter1, parameter1Mode)
                value2 = self.parameter_value(parameter2, parameter2Mode)
                value = value1 * value2
                self.program[parameter3] = value
                self.i += 4

            elif opcode == 3:  # takes input and saves to parameter address
                if self.phase_input_set:
                    self.program[parameter1] = input
                else:
                    self.program[parameter1] = phase_setting
                    self.phase_input_set = True
                self.i += 2

            elif opcode == 4:  # outputs the value of the parameter, stops program
                value1 = self.parameter_value(parameter1, parameter1Mode)
                output = value1  # does an output
                self.i += 2
                break

            elif opcode == 5:  # jump if true
                value1 = self.parameter_value(parameter1, parameter1Mode)
                value2 = self.parameter_value(parameter2, parameter2Mode)
                if value1 != 0:
                    self.i = value2
                else:
                    self.i += 3

            elif opcode == 6:  # jump if false
                value1 = self.parameter_value(parameter1, parameter1Mode)
                value2 = self.parameter_value(parameter2, parameter2Mode)
                if value1 == 0:
                    self.i = value2
                else:
                    self.i += 3

            elif opcode == 7:  # less than
                value1 = self.parameter_value(parameter1, parameter1Mode)
                value2 = self.parameter_value(parameter2, parameter2Mode)
                if value1 < value2:
                    self.program[parameter3] = 1
                else:
                    self.program[parameter3] = 0
                self.i += 4

            elif opcode == 8:  # less than
                value1 = self.parameter_value(parameter1, parameter1Mode)
                value2 = self.parameter_value(parameter2, parameter2Mode)
                if value1 == value2:
                    self.program[parameter3] = 1
                else:
                    self.program[parameter3] = 0
                self.i += 4

            elif opcode == 99:
                print('HALTED')
                self.halted = True
                break

            else:
                print(f'Invalid opcode at {i}')
                break

        return output


def all_phase_settings():
    all = [i for i in range(0, 44444)]
    return [str(i).zfill(5) for i in all if ''.join(sorted(list(str(i).zfill(5)))) == '01234' ]


# Challenge 1 solution
max_output = 0
max_output_phase_settings = None
for phase_settings in all_phase_settings():
    input = 0
    output = 0

    for phase_setting in phase_settings:
        amplifier = AmplifierIntcode(program.copy(), input, int(phase_setting))
        output = amplifier.run()
        input = output

    if output > max_output:
        max_output = output
        max_output_phase_settings = phase_settings

print('Solution for non-feedback mode:')
print(f'Phase settings: {max_output_phase_settings}')
print(f'output: {max_output}')

# Answer: 212460

# Challenge 2 solution
def all_feedback_mode_phase_settings():
    all = [i for i in range(55555, 99999)]
    return [str(i).zfill(5) for i in all if ''.join(sorted(list(str(i).zfill(5)))) == '56789' ]


program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
max_output = 0
max_output_phase_settings = None
for phase_settings in all_feedback_mode_phase_settings():
    output = 0

    while True:
        amplifier_programs = [
            AmplifierIntcode(program.copy(), 0, int(phase_settings[0])),
            AmplifierIntcode(program.copy(), 0, int(phase_settings[1])),
            AmplifierIntcode(program.copy(), 0, int(phase_settings[2])),
            AmplifierIntcode(program.copy(), 0, int(phase_settings[3])),
            AmplifierIntcode(program.copy(), 0, int(phase_settings[4])),
        ]

        for i in range(len(phase_settings)):
            amplifier = amplifier_programs[i]
            amplifier.input = output
            output = amplifier.run()
            print(i)
            print(amplifier.i)

            if amplifier.halted and i == 4:
                break

    print(output)

    if output > max_output:
        max_output = output
        max_output_phase_settings = phase_settings

print('Solution for feedback mode:')
print(f'Phase settings: {max_output_phase_settings}')
print(f'output: {max_output}')