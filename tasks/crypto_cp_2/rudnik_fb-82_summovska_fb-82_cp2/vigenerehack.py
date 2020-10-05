def split_by_keylen(ciphertext,keylen):
    arr_of_parts = []
    for i in range(0,keylen):
        part_str = ''
        for j in range(i,len(ciphertext),keylen):
            part_str += ciphertext[j]
        arr_of_parts.append(part_str)
    return arr_of_parts


def icx(splited_strings):
    arr_of_icx = []
    for splited_string in splited_strings:
        len_of_splited_string = len(splited_string)
        letters_map = {i:0 for i in LETTERS}
        for letter in splited_string:
            letters_map[letter] += 1
        arr = sum([letters_map[item] * (letters_map[item] - 1) for item in letters_map])
        div = len_of_splited_string * (len_of_splited_string - 1)
        arr_of_icx.append(arr / div)
    return arr_of_icx