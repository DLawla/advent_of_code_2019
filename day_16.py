from collections import deque
import numpy as np

input = '59781998462438675006185496762485925436970503472751174459080326994618036736403094024111488348676644802419244196591075975610084280308059415695059918368911890852851760032000543205724091764633390765212561307082338287866715489545069566330303873914343745198297391838950197434577938472242535458546669655890258618400619467693925185601880453581947475741536786956920286681271937042394272034410161080365044440682830248774547018223347551308590698989219880430394446893636437913072055636558787182933357009123440661477321673973877875974028654688639313502382365854245311641198762520478010015968789202270746880399268251176490599427469385384364675153461448007234636949'
pattern = ['0', '1', '0', '-1']

# Flawed Frequency Transmission algorithm
def fft(input, patterns):
    input_array = np.repeat(input, input.size, axis=0)
    # get an array of sums of each element
    element_sums = (input_array * patterns).sum(axis=1)
    # only extract ones digit of each sum
    phase_outputs = [int(list(str(element_sum))[-1]) for element_sum in element_sums]
    return np.array([phase_outputs])

def part2_fft(input):
    # sums = []
    # for i in range(input.size):
    #     sums.append(np.array(input[(i + 1):]).sum() - np.array(input[:i]).sum())
    #     if (i % 10000 == 0):
    #         print(i)

    # element_sums = []
    # for i in len(8):
    #     element_sums


    # subtract the values at the index and belowelement_sums.append(np.repeat(input, input.size, axis=0))
    # sums_after_pattern = []
    # for i in range(8):
    #     sums_after_pattern.append(element_sums[i] - sum(element_sums[0:i+1]))
    # # only extract ones digit of each sum
    # phase_outputs = [int(list(str(element_sum))[-1]) for element_sum in sums_after_pattern]
    # return np.array([phase_outputs])

def build_patterns(pattern, length):
    return [build_pattern(pattern, i, length) for i in range(length)]

def build_pattern(pattern, i, length):
    element_pattern = [[p] * (i + 1) for p in pattern]
    element_pattern = [item for sublist in element_pattern for item in sublist] # flatten
    element_pattern = deque(element_pattern) # cast to deque for easy shifting
    element_pattern.rotate(-1)

    element_pattern = element_pattern * ((length// element_pattern.__len__()) + 1)
    while element_pattern.__len__() > length:
        del element_pattern[-1]
    element_pattern = list(map(lambda x: int(x), element_pattern))
    return list(element_pattern)

# Part 1
# listed_input = np.array([list(map(lambda x: int(x), list(input)))])
# patterns = np.array(build_patterns(pattern, listed_input.shape[1]))
# current_signal = listed_input
# for i in range(100):
#     current_signal = fft(current_signal, patterns)
# print(current_signal)
# print(current_signal[0][0:7])
# about 10 seconds
# '23135243338183437189487858949976174057396905644982679444446322790060382606153670835405714511902223189596052297963339802917581526266145363968330912085306711776334419455115543453905027355256915163569744818109712409097717077948253119503417119702867298448356647228128215182644060703168638540475056511883493280621970447478759955562248685458384736928690589286722814788275394968630188587045564870600389937139407564133893188782064571063094796261640377941822209779892337045705570827905001967892128070173152972893500621932609725239120656077728936982688130754191289859126065617625123488407075807836577292546425615470466485047942599575429170158966998557239686949'


# Part 2:
# Observations/tricks to play w/
# 1) we only care about all indices of the input FROM the read location (the pattern will be 0's until i+1), follow by only *1 multiplication
# 2) we are repeating an input signal, and because we are calculating a the sum of the current array (minus the i +1 first elements)
# you could do something w/ that
# b/c so many 0e.g. on index 0 of len 4 array: [0, 1, 1, 1] would be multiplied
input = input * 10_000
listed_input = list(input)
read_offset = int(''.join(listed_input[0:7]))

listed_input = listed_input[read_offset:]

print('building part 2')
listed_input = np.array(list(map(lambda x: int(x), listed_input)))
patterns = []
list_length = listed_input.size
patterns = []

# e.g. on index 0 of len 4 array: [0, 1, 1, 1]
# for i in range(list_length):
#     patterns.append([0] * (i + 1) + [1] * (list_length - 1))

patterns = np.array(patterns)
current_signal = listed_input

print('starting calulations')
for i in range(100):
    current_signal = part2_fft(current_signal)
    print(i)
    print(current_signal)
print(f'Final full signal: {current_signal}')
print(f'Message: {list(current_signal)[0 : 8]}')
