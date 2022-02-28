from collections import defaultdict


def alphabetize(dictionary: dict) -> dict:
    """
    Alphabetizes the words in a dictionary.
    """
    for key in dictionary:
        dictionary[key].sort(key=str.lower)
    return dictionary


def organize_dict(word_list: list) -> dict:
    """
    Organizes the words in a list and returns it in dictionary.
    """
    # Organize words by length
    d = defaultdict(set)
    for word in word_list:
        d[len(word)].add(word)
    word_list = {k: list(v) for k, v in d.items()}
    word_list = dict(word_list)
    word_list = sorted(word_list.items(), key=lambda item: item[0])
    word_list = dict(word_list)
    return word_list


def print_dict_length(dictionary: dict) -> None:
    """
    Prints the length of each key in a dictionary.
    """
    total = 0
    for key, value in dictionary.items():
        print(f'{key}: {len(value)}')
        total += len(value)

    print(f'Total: {total}')


def print_two_dict(dictionary1: dict, dictionary2: dict) -> None:
    """
    Prints two dictionaries side by side.
    """
    for key, value in dictionary1.items():
        print(print_diff(key, value, dictionary2[key]))


def print_diff(prompt: str, before_total: int, after_total: int) -> str:
    sign = '+' if before_total < after_total else '-'
    return f'{prompt}: {before_total} -> {after_total} ({sign}{abs(before_total - after_total)})'


def get_length(dictionary: dict) -> tuple:
    """
    Returns the length of each key in a dictionary and the total length.
    (dict, int)
    """
    dict_length = {}
    total = 0
    for key, value in dictionary.items():
        dict_length[key] = len(value)
        total += len(value)
    return dict_length, total


def process_words(words: list) -> dict:
    """
    Processes the words in a list and returns it in dictionary.
    """
    words = [w.strip() for w in words]
    words = [w for w in words if w.isalpha()]
    words = [w for w in words if len(w) >= 4 and len(w) <= 15]
    words = [w for w in words if w.islower()]

    words = organize_dict(words)
    words = alphabetize(words)
    return words


def merge_dictionaries(list_of_dicts: list) -> dict:
    '''Merges a list of dictionaries into one dictionary that has lists as values'''
    merged_dict = defaultdict(list)
    for d in list_of_dicts:
        for k, v in d.items():
            merged_dict[k].extend(v)

    # remove duplicates
    for length in merged_dict:
        merged_dict[length] = list(set(merged_dict[length]))
    return dict(merged_dict)
