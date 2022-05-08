lan = ['python', 'c++', 'c', 'scala', 'java']

def count_letter(list, letter):
    count = 0
    for l in list:
        if letter in l:
            count += 1
    return count

print(count_letter(lan, 'c'))
