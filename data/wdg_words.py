import json
import os
from pathlib import Path

import requests
from config import load_config
from tqdm import tqdm
from utils import process_words

cfg = load_config()

WORKING_DIR = os.path.join(cfg.paths.data, cfg.paths.words, cfg.paths.wgd)


# 2-letter-words/2-letter-words.json
def download_length_lists() -> None:
    urls = [f'{cfg.urls.wgd_length}{i}-letter-words/{i}-letter-words.json' for i in range(4, 16)]

    for url in tqdm(urls):
        download_single_list(url)


def download_single_list(url: str) -> None:
    file_path = Path(WORKING_DIR, cfg.paths.source, url.split('/')[-1])

    if file_path.exists():
        return

    # Create the directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    r = requests.get(url)
    print(f'Downloading {file_path}')

    with file_path.open('w') as f:
        json.dump(r.json(), f)


def merge_length_files() -> str:
    file_paths = [os.path.join(WORKING_DIR, cfg.paths.source, f'{i}-letter-words.json') for i in range(4, 16)]

    words = {}
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # len of first word as key, list of all words as value
        words[len(data[0]['word'])] = [d['word'] for d in data]

    # write to file
    output_file = os.path.join(WORKING_DIR, cfg.files.wgd_word_list)
    with open(output_file, 'w') as f:
        json.dump(words, f)

    return output_file


def wdg_english() -> str:
    # download the english words list
    file_path = download_txt(cfg.urls.wgd_english, cfg.files.wgd_english_txt)

    # load the english words list
    with open(file_path, 'r') as f:
        words = f.readlines()

    words = process_words(words)

    output_file = os.path.join(WORKING_DIR, cfg.files.wgd_english)
    with open(output_file, 'w') as f:
        json.dump(words, f)

    return output_file


def wgd_twl() -> str:
    # download the twl words list
    file_path = download_txt(cfg.urls.wgd_twl, cfg.files.wgd_twl_txt)

    # remove the first 3 lines of the file
    with open(file_path, 'r') as f:
        words = f.readlines()

    # find location of 'aa' in list and get all words after that
    aa_index = words.index('aa\n')
    words = words[aa_index:]

    words = process_words(words)

    output_file = os.path.join(WORKING_DIR, cfg.files.wgd_twl)
    with open(output_file, 'w') as f:
        json.dump(words, f)

    return output_file


def wgd_compound() -> str:
    # download the compound words list
    file_path = download_txt(cfg.urls.wgd_compound, cfg.files.wgd_compound_tmp)

    with open(file_path, 'r') as f:
        words = json.load(f)

    # extract all of the words to a list
    words = [d['word'] for d in words]
    words = process_words(words)

    # save the words to a file
    output_file = os.path.join(WORKING_DIR, cfg.files.wgd_compound)
    with open(output_file, 'w') as f:
        json.dump(words, f)

    return output_file


def wgd_sowpods() -> str:
    # download the sowpods words list
    file_path = download_txt(cfg.urls.wgd_sowpods, cfg.files.wgd_sowpods_txt)

    # load the sowpods words list
    with open(file_path, 'r') as f:
        words = f.readlines()

    # find location of 'aa' in list and get all words after that
    aa_index = words.index('aa\n')
    words = words[aa_index:]

    words = process_words(words)

    output_file = os.path.join(WORKING_DIR, cfg.files.wgd_sowpods)
    with open(output_file, 'w') as f:
        json.dump(words, f)

    return output_file


def download_txt(url: str, file_name: str) -> str:
    file_path = os.path.join(WORKING_DIR, cfg.paths.source, file_name)
    if not os.path.exists(file_path):
        print(f'Downloading {file_name}')
        r = requests.get(url)
        with open(file_path, 'w') as f:
            f.write(r.text)
    return file_path


def read_words(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        words = json.load(f)
    return words


def get_all_words() -> dict:
    download_length_lists()
    completed_files = [merge_length_files()]
    completed_files.append(wdg_english())
    completed_files.append(wgd_twl())
    completed_files.append(wgd_compound())
    completed_files.append(wgd_sowpods())

    words = {}
    for complete_file in completed_files:
        for key, value in read_words(complete_file).items():
            if key in words:
                words[key].extend(value)
            else:
                words[key] = value

    # make all keys integers
    words = {int(key): value for key, value in words.items()}

    words_length = {k: len(v) for k, v in words.items()}
    total = sum(words_length.values())

    print('\nRemoving Duplicates from wgd')
    for length in words:
        words[length] = list(set(words[length]))

    new_words_length = {k: len(v) for k, v in words.items()}
    new_total = sum(new_words_length.values())
    for key, value in words_length.items():
        print(f'{key}: {value} -> {new_words_length[key]}')
    print(f'{total} -> {new_total}')

    output_file = os.path.join(WORKING_DIR, cfg.files.wgd_word_list)
    with open(output_file, 'w') as f:
        json.dump(words, f)
    return words


if __name__ == '__main__':
    get_all_words()
