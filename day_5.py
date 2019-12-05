input = [3,225,1,225,6,6,1100,1,238,225,104,0,2,171,209,224,1001,224,-1040,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,102,65,102,224,101,-3575,224,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1102,9,82,224,1001,224,-738,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1101,52,13,224,1001,224,-65,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1102,82,55,225,1001,213,67,224,1001,224,-126,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1,217,202,224,1001,224,-68,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1002,176,17,224,101,-595,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1102,20,92,225,1102,80,35,225,101,21,205,224,1001,224,-84,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1101,91,45,225,1102,63,5,225,1101,52,58,225,1102,59,63,225,1101,23,14,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1006,224,329,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,344,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,359,1001,223,1,223,8,677,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1107,677,226,224,102,2,223,223,1006,224,389,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,419,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,449,1001,223,1,223,1008,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1005,224,479,1001,223,1,223,108,677,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,108,226,226,224,1002,223,2,223,1006,224,509,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,524,101,1,223,223,107,677,226,224,1002,223,2,223,1005,224,539,1001,223,1,223,8,226,226,224,102,2,223,223,1005,224,554,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,569,101,1,223,223,108,677,226,224,102,2,223,223,1006,224,584,1001,223,1,223,7,677,677,224,1002,223,2,223,1005,224,599,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,614,1001,223,1,223,1107,226,677,224,102,2,223,223,1006,224,629,101,1,223,223,1107,226,226,224,102,2,223,223,1005,224,644,1001,223,1,223,1108,677,677,224,1002,223,2,223,1005,224,659,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]

def parameter_value(input, parameter, mode):
    if mode == 0:
        return input[parameter]
    else:
        return parameter


def run_intcode(input, starting_input):
    i = 0 # instruction_pointer
    outputs = []

    while True:
        parameters = list(str(input[i]))
        parameter_length = len(parameters)
        if parameter_length < 5:
            zeros_to_pad = (5 - parameter_length)
            parameters = list('0' * zeros_to_pad) + parameters

        # print(input)
        print(parameters)

        opcode = int(''.join([parameters[3], parameters[4]]))
        parameter1Mode = int(parameters[2])
        parameter2Mode = int(parameters[1])
        parameter3Mode = int(parameters[0])

        if len(input) > (i + 1):
            parameter1 = input[i + 1]
        if len(input) > (i + 3):
            parameter2 = input[i + 2]
            parameter3 = input[i + 3]

        if opcode == 1: # addition
            value1 = parameter_value(input, parameter1, parameter1Mode)
            value2 = parameter_value(input, parameter2, parameter2Mode)
            input[parameter3] = value1 + value2
            i = i + 4

        elif opcode == 2: # multiplication
            value1 = parameter_value(input, parameter1, parameter1Mode)
            value2 = parameter_value(input, parameter2, parameter2Mode)
            value = value1 * value2
            input[parameter3] = value
            i = i + 4

        elif opcode == 3: # takes input and saves to parameter address
            input[parameter1] = starting_input
            i = i + 2

        elif opcode == 4: # outputs the value of the parameter
            value1 = parameter_value(input, parameter1, parameter1Mode)
            outputs += [value1] # does an output
            i = i + 2

        elif opcode == 5: # jump if true
            value1 = parameter_value(input, parameter1, parameter1Mode)
            value2 = parameter_value(input, parameter2, parameter2Mode)
            if value1 != 0:
                i = value2
            else:
                i += 3

        elif opcode == 6:  # jump if false
            value1 = parameter_value(input, parameter1, parameter1Mode)
            value2 = parameter_value(input, parameter2, parameter2Mode)
            if value1 == 0:
                i = value2
            else:
                i += 3

        elif opcode == 7:  # less than
            value1 = parameter_value(input, parameter1, parameter1Mode)
            value2 = parameter_value(input, parameter2, parameter2Mode)
            if value1 < value2:
                input[parameter3] = 1
            else:
                input[parameter3] = 0
            i = i + 4

        elif opcode == 8:  # less than
            value1 = parameter_value(input, parameter1, parameter1Mode)
            value2 = parameter_value(input, parameter2, parameter2Mode)
            if value1 == value2:
                input[parameter3] = 1
            else:
                input[parameter3] = 0
            i = i + 4

        elif opcode == 99:
            break

        else:
            print(f'Invalid opcode at {i}')
            break

    return [input, outputs]

final_input, outputs = run_intcode(input, 5)
print(final_input)
print(outputs)
# answer: 3629692


