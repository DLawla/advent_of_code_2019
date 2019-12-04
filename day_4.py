# inputs
range_start = 402328
range_end = 864247

# algorithm
def one_isolated_matching_tuple(password):
    digits_array = [int(x) for x in str(password)]
    one_match_found = False
    for i in range(len(digits_array)):
        if i == 5:
            break
        if digits_array[i] == digits_array[i + 1]:
            # cannot match previous number
            if i != 0:
                if digits_array[i] == digits_array[i - 1]:
                    continue
            # matches if it doesn't match two ahead
            if i == 4 or digits_array[i] != digits_array[i + 2]:
                one_match_found = True
    return one_match_found

def two_adjacent_numbers(password):
    digits_array = [int(x) for x in str(password)]
    one_match_found = False
    for i in range(len(digits_array)):
        if i == 5:
            break
        if digits_array[i] == digits_array[i + 1]:
            one_match_found = True
            break
    return one_match_found

def all_increasing_numbers(password):
    digits_array = [int(x) for x in str(password)]
    all_increasing = True
    for i in range(len(digits_array)):
        if i == 0:
            continue
        if digits_array[i] < digits_array[i - 1]:
            all_increasing = False
    return all_increasing


# Challenge 1
# valid_passwords = []
# for password in range(range_start, range_end + 1):
#     if two_adjacent_numbers(password) & all_increasing_numbers(password):
#         valid_passwords += [password]

# Challenge 2
valid_passwords = []
for password in range(range_start, range_end + 1):
    if one_isolated_matching_tuple(password) & all_increasing_numbers(password):
        valid_passwords += [password]


print('Valid passwords:')
print(valid_passwords)
print(f'Count:{len(valid_passwords)}')
