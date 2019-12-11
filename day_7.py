program = [3,8,1001,8,10,8,105,1,0,0,21,42,67,88,105,114,195,276,357,438,99999,3,9,101,4,9,9,102,3,9,9,1001,9,2,9,102,4,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,101,2,9,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,1001,9,4,9,1002,9,4,9,101,2,9,9,1002,9,2,9,4,9,99,3,9,101,4,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99]

def parameter_value(program, parameter, mode):
    if mode == 0:
        return program[parameter]
    else:
        return parameter


def run_amplifier_intcode(program, input, phase_setting, instruction_pointer):
    i = instruction_pointer # instruction_pointer
    output = None
    halted = False
    phase_input_set = False

    while True:
        parameters = list(str(program[i]))
        parameter_length = len(parameters)
        if parameter_length < 5:
            zeros_to_pad = (5 - parameter_length)
            parameters = list('0' * zeros_to_pad) + parameters

        opcode = int(''.join([parameters[3], parameters[4]]))
        parameter1Mode = int(parameters[2])
        parameter2Mode = int(parameters[1])
        parameter3Mode = int(parameters[0])

        if len(program) > (i + 1):
            parameter1 = program[i + 1]
        if len(program) > (i + 3):
            parameter2 = program[i + 2]
            parameter3 = program[i + 3]

        if opcode == 1: # addition
            value1 = parameter_value(program, parameter1, parameter1Mode)
            value2 = parameter_value(program, parameter2, parameter2Mode)
            program[parameter3] = value1 + value2
            i = i + 4

        elif opcode == 2: # multiplication
            value1 = parameter_value(program, parameter1, parameter1Mode)
            value2 = parameter_value(program, parameter2, parameter2Mode)
            value = value1 * value2
            program[parameter3] = value
            i = i + 4

        elif opcode == 3: # takes input and saves to parameter address
            if phase_input_set:
                program[parameter1] = input
            else:
                program[parameter1] = phase_setting
                phase_input_set = True
            i = i + 2

        elif opcode == 4: # outputs the value of the parameter, stops program
            value1 = parameter_value(program, parameter1, parameter1Mode)
            output = value1 # does an output
            i = i + 2
            break

        elif opcode == 5: # jump if true
            value1 = parameter_value(program, parameter1, parameter1Mode)
            value2 = parameter_value(program, parameter2, parameter2Mode)
            if value1 != 0:
                i = value2
            else:
                i += 3

        elif opcode == 6:  # jump if false
            value1 = parameter_value(program, parameter1, parameter1Mode)
            value2 = parameter_value(program, parameter2, parameter2Mode)
            if value1 == 0:
                i = value2
            else:
                i += 3

        elif opcode == 7:  # less than
            value1 = parameter_value(program, parameter1, parameter1Mode)
            value2 = parameter_value(program, parameter2, parameter2Mode)
            if value1 < value2:
                program[parameter3] = 1
            else:
                program[parameter3] = 0
            i = i + 4

        elif opcode == 8:  # less than
            value1 = parameter_value(program, parameter1, parameter1Mode)
            value2 = parameter_value(program, parameter2, parameter2Mode)
            if value1 == value2:
                program[parameter3] = 1
            else:
                program[parameter3] = 0
            i = i + 4

        elif opcode == 99:
            print('HALTED')
            halted = True
            break

        else:
            print(f'Invalid opcode at {i}')
            break

    return [output, program, i, halted]


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
        output, _, _, _ = run_amplifier_intcode(program.copy(), input, int(phase_setting), 0)
        input = output

    if output > max_output:
        max_output = output
        max_output_phase_settings = phase_settings

print('Solution for non-feedback mode:')
print(f'Phase settings: {max_output_phase_settings}')
print(f'output: {max_output}')

# Answer: 212460

# Challenge 2 solution
# TODO, need to refactor the int_program to a class that can be stored as an object and can stop then continue,
# store current pointer index, store current program, etc

def all_feedback_mode_phase_settings():
    all = [i for i in range(55555, 99999)]
    return [str(i).zfill(5) for i in all if ''.join(sorted(list(str(i).zfill(5)))) == '56789' ]


program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
max_output = 0
max_output_phase_settings = None
for phase_settings in all_feedback_mode_phase_settings():
    input = 0
    output = 0

    while True:
        program_copies = [program.copy(), program.copy(), program.copy(), program.copy(), program.copy()]
        program_pointers = [0, 0, 0, 0, 0]
        for i in range(len(phase_settings)):
            output, current_program, current_pointer, halted = run_amplifier_intcode(program_copies[i], input, int(phase_settings[i]), program_pointers[i])
            print(i)
            print(current_pointer)
            print(halted)

            program_copies[i] = current_program
            program_pointers[i] = current_pointer
            input = output


            if halted and i == 4:
                break

    print(output)

    if output > max_output:
        max_output = output
        max_output_phase_settings = phase_settings

print('Solution for feedback mode:')
print(f'Phase settings: {max_output_phase_settings}')
print(f'output: {max_output}')