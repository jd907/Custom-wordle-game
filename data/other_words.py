from copy import deepcopy
import os
from collections import defaultdict
from json import dump

import enchant
import nltk
import requests
from colorama import Fore, Style
from tqdm import tqdm

import wdg_words
from config import load_config
from utils import alphabetize, get_length, merge_dictionaries, organize_dict, print_dict_length, print_diff, print_two_dict

d = enchant.Dict('en_US')

cfg = load_config()


def download_dictionary() -> list:
    # check if dictionary file exists
    if not os.path.exists(os.path.join(cfg.paths.data, cfg.files.dictionary_download_list)):
        response = requests.get(cfg.urls.dict_list)
        # save to file
        with open(os.path.join(cfg.paths.data, cfg.files.dictionary_download_list), 'w') as f:
            f.write(response.text)
        print(f'{Fore.GREEN}Successfully downloaded dictionary word list!{Style.RESET_ALL}')

    # load dictionary file
    with open(os.path.join(cfg.paths.data, cfg.files.dictionary_download_list), 'r') as f:
        words = f.readlines()

    words = [word.strip() for word in words]
    print('online:', len(words))

    return words


def update_other_words() -> str:
    word_list = nltk_download()
    word_list.extend(download_dictionary())

    word_list = list(set(word_list))

    print('text:', len(word_list))

    word_list = process_words(word_list)

    print_dict_length(word_list)

    before_len, before_total = get_length(word_list)

    all_dicts = [wdg_words.get_all_words(), word_list]
    word_list = merge_dictionaries(all_dicts)

    after_len, after_total = get_length(word_list)
    print()
    print('merging in wdg_words')
    print_two_dict(before_len, after_len)
    print_diff('Total', before_total, after_total)

    # removing duplicates
    for length in word_list:
        word_list[length] = list(set(word_list[length]))

    print(f'{Fore.YELLOW}Saving words...{Style.RESET_ALL}')
    word_list = alphabetize(word_list)
    # save to file
    output_file = os.path.join(cfg.paths.data, cfg.paths.words, cfg.files.other_word_list)
    with open(output_file, 'w+') as f:
        dump(word_list, f)
    print(f'{Fore.GREEN}Successfully refreshed dictionary word list!{Style.RESET_ALL}')

    return output_file


def process_words(word_list: list) -> dict:
    '''Remove special/digit/uppercase words, and organize'''
    print(f'{Fore.YELLOW}Processing words...{Style.RESET_ALL}')

    # remove all words containing numbers or special characters
    word_list = [word for word in word_list if word.isalpha()]

    # remove all words that have an uppercase letter
    word_list = [word for word in word_list if not any(c.isupper() for c in word)]

    print('without uppers:', len(word_list))
    word_list = list(set(word_list))
    print('without duplicates:', len(word_list))

    # remove all words that don't exist in the dictionary
    d = enchant.Dict('en_US')
    print(f'{Fore.YELLOW}Checking for existence in dictionary...{Style.RESET_ALL}')
    word_list = [word for word in tqdm(word_list) if d.check(word)]
    print('dictionary:', len(word_list))

    # remove all words with length less than 4 and longer than 15
    word_list = [word for word in word_list if len(word) >= 4 and len(word) <= 15]

    # Organize words by length
    word_list = organize_dict(word_list)

    word_list = alphabetize(word_list)
    return word_list


def nltk_download() -> list:
    print(f'{Fore.GREEN}Refreshing main word list...{Style.RESET_ALL}')
    nltk.download('words', download_dir=os.path.join(cfg.paths.data, 'nltk_data'), quiet=True)

    with open(os.path.join(cfg.paths.data, 'nltk_data', 'corpora', 'words', 'en'), 'r') as f:
        word_list = f.readlines()

    # remove all \n
    word_list = [word.strip() for word in word_list]
    print('local:', len(word_list))
    return word_list


if __name__ == '__main__':
    update_other_words()
