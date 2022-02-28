import os
from json import dump, load

import wordfreq
from colorama import Fore, Style

from config import load_config
from utils import get_length, organize_dict, print_diff

cfg = load_config()


def update_top_words():
    top_list = list(wordfreq.top_n_list(cfg.params.language, cfg.params.top_word_size, ascii_only=True))

    # remove all words containing numbers or special characters
    top_list = [word for word in top_list if word.isalpha()]

    print(f'{Fore.YELLOW}Removing words less than 4 and longer than 15' + Style.RESET_ALL)

    # remove all words with length less than 4 and longer than 15
    top_list = [word for word in top_list if len(word) >= 4 and len(word) <= 15]
    print(f'{Fore.YELLOW}Removing words not in dictionary...{Style.RESET_ALL}')

    # sort list by length
    top_list.sort(key=lambda x: len(x))

    # organize words by length
    top_list = organize_dict(top_list)

    before_len, before_total = get_length(top_list)

    # open other_list.json
    with open(os.path.join(cfg.paths.data, cfg.paths.words, cfg.files.other_word_list), 'r') as f:
        other_list = load(f)

    #if word is not in other list, remove it
    for key in top_list:
        top_list[key] = [word for word in top_list[key] if word in other_list[str(key)]]
        print(print_diff(key, before_len[key], len(top_list[key])))

    after_len, after_total = get_length(top_list)
    print_diff('Total', before_total, after_total)

    # alphabetize the words
    for value in top_list.values():
        value.sort(key=str.lower)

    # convert every key to string
    top_list = {str(key): value for key, value in top_list.items()}

    # save to file
    file_path = os.path.join(cfg.paths.data, cfg.files.popular_word_list)
    with open(file_path, 'w') as f:
        dump(top_list, f)

    num_of_words = sum(len(v) for k, v in top_list.items())
    print(f'{Fore.CYAN}Total number of words:{num_of_words}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}Successfully refreshed popular word list!{Style.RESET_ALL}')


if __name__ == '__main__':
    update_top_words()
