import os
from copy import deepcopy
from json import dump, load

from colorama import Fore, Style

import other_words
import top_words
import wdg_words
from config import load_config

cfg = load_config()


def load_list(file_path: str, file_name: str) -> dict:
    path = os.path.join(file_path, file_name)
    with open(path, 'r') as f:
        words = load(f)
    return words


def main() -> None:
    # load the top_list.json file as a dictionary
    top_list = load_list(cfg.paths.data, cfg.files.popular_word_list)

    # load the other_list.json file as a dictionary
    file_path = os.path.join(cfg.paths.data, cfg.paths.words)
    other_list = load_list(file_path, cfg.files.other_word_list)

    top_list_length = {k: len(v) for k, v in top_list.items()}

    print(f'{Fore.CYAN}Merging top_list and other_list...{Style.RESET_ALL}')
    combined_dict = deepcopy(other_list)
    for key in combined_dict:
        combined_dict[key] = list(set(top_list[key] + other_list[key]))

    # alphabetize the words in each list
    for key in combined_dict:
        combined_dict[key].sort(key=str.lower)

    combined_length = {k: len(v) for k, v in combined_dict.items()}
    other_list_length = {k: len(v) for k, v in other_list.items()}

    # grab the keys from the combined dictionary and make a new dictionary with blank values
    results_dict = {k: [] for k in combined_dict}

    # add the values of the combined dictionary to the blank dictionary
    for k, v in results_dict.items():
        v.append(f'top_list: {top_list_length[k]}')
        v.append(f'other_list: {other_list_length[k]}')
        v.append(f'combined: {combined_length[k]}')

    for k, v in results_dict.items():
        print(k, v)

    # save dictionary_list
    with open(os.path.join(cfg.paths.data, cfg.files.dictionary_word_list), 'w') as f:
        dump(combined_dict, f)

    print(f'{Fore.GREEN}Successfully refreshed dictionary list!{Style.RESET_ALL}')


if __name__ == '__main__':
    other_words.update_other_words()
    top_words.update_top_words()

    main()
