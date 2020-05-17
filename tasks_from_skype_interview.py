#  Task 1
#  Немного упростил решение по сравнению с тем, которое предоставил на собеседовании и убрал assert.

strings = ["abc", "hello", "qwerty", "world", "123"]


def find_string_with_max_length(strings):
    max_len = max([len(string) for string in strings])
    for indx, string in enumerate(strings):
        if len(string) == max_len:
            return strings[indx]


print(f"\nTask #1 answer: {find_string_with_max_length(strings)}")

# Task 2
# Здесь как и в первой задачке решил избавиться от лишних проверок (так как в задаче это не требуется).
# Поэтому считаю входные данные изначально корректными.
# Решение представил в двух вариантах: через цикл и через словарь.

strings = ['банан', 'кефир', 'сколопендра']


# v1
def mixer_v1(strings):
    max_string_len = max([len(string) for string in strings])
    result_string = ''

    symb_indx = 0
    while symb_indx < max_string_len:
        for string in strings:
            if symb_indx < len(string):
                result_string += string[symb_indx]
        symb_indx += 1
    return result_string


print(f"Task #2v1 answer: {mixer_v1(strings)}")


# v2
def mixer_v2(strings):
    symb_dict = dict()

    for string in strings:
        for i in range(len(string)):
            symb_dict.update({f'{i}': (symb_dict[f'{i}'] if symb_dict.get(f'{i}') else '') + string[i]})

    #return ''.join(list(symb_dict.values()))  # в таком варианте может случится неправильный вывод
                                               # из-за того , что ключи в dict не всегда упорядочены
                                               # поэтому можно переписать return как ниже или использовать OrderedDict
                                               # порядок ключей в словаре зависит от реализации словаря в используемой версии python

    return ''.join([symb_dict[f"{i}"] for i in range(len(symb_dict.keys()))])


print(f"Task #2v2 answer: {mixer_v2(strings)}")
