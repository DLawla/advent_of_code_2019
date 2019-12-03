input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,6,23,2,23,13,27,1,27,5,31,2,31,10,35,1,9,35,39,1,39,9,43,2,9,43,47,1,5,47,51,2,13,51,55,1,55,9,59,2,6,59,63,1,63,5,67,1,10,67,71,1,71,10,75,2,75,13,79,2,79,13,83,1,5,83,87,1,87,6,91,2,91,13,95,1,5,95,99,1,99,2,103,1,103,6,0,99,2,14,0,0]
# input[1] = 12
# input[2] = 2

def run_intcode(input):
    i = 0 # instruction_pointer
    while True:
        if len(input) >= (i + 3):
            instruction = [input[i], input[i + 1], input[i + 2], input[i + 3]]
            opcode = instruction[0]
            parameter1 = instruction[1]
            parameter2 = instruction[2]
            parameter3 = instruction[3]
        else:
            instruction = [input[i]]
            opcode = instruction[0]

        if opcode == 1: # addition
            value = input[parameter1] + input[parameter2]
            input[parameter3] = value
        elif opcode == 2: # multiplication
            value = input[parameter1] * input[parameter2]
            input[parameter3] = value
        elif opcode == 99:
            break
        else:
            print(f'Invalid opcode at {i}')
            break
        i = i + 4
    return input

# print(run_intcode(input))

# pair of inputs that create output 19690720
desired_output = 19690720
noun = 0 # input at address 1
verb = 0 # input at address 2
match_found = False

for noun in range(0, 99, 1):
    for verb in range(0, 99, 1):
        fresh_input = input.copy()
        fresh_input[1] = noun
        fresh_input[2] = verb
        result = run_intcode(fresh_input)
        if result[0] == desired_output:
            match_found = True
            break

    if match_found:
        break

if match_found:
    print(f"Match found: {noun}, {verb}. Answer: {100 * noun + verb}")
else:
    print('No match found')





