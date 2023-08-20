import argparse
import os
import random
import string
from json import load

import readchar
from colorama import Fore, Style

from data.config import load_config
from wordle import LettersResult, Wordle

cfg = load_config()

CORRECT = Style.BRIGHT + Fore.GREEN
ALMOST = Style.BRIGHT + Fore.YELLOW
WRONG = Style.BRIGHT + Fore.BLACK
NOT_GUESSED = Style.NORMAL
BASE = string.digits + string.ascii_lowercase + string.ascii_uppercase


def main(word_length: int, max_attempts: int, seed: str, secret_word: str) -> str:
    popular_word_list = load_popular_wordlist(word_length)
    dictionary_wordset = load_dictionary_wordset(word_length)

    seed_int = decode_num(seed) if seed is not None else random.randint(0, cfg.params.seed_max)
    random.seed(seed_int)

    if secret_word is not None:
        chosen_word = secret_word
    else:
        chosen_word = random.choice(popular_word_list)

    wordle = Wordle(chosen_word, word_length=word_length, max_attempts=max_attempts)

    refresh_board(wordle)
    while wordle.can_attempt:
        input_word = input('Enter your guess: ')

        if len(input_word) != wordle.word_length:
            refresh_board(wordle)
            print(Fore.RED + f'Word is {len(input_word)}/{wordle.word_length} characters long.' + Style.RESET_ALL)
            continue

        if input_word.lower() not in dictionary_wordset:
            refresh_board(wordle)
            print(Fore.RED + f"'{input_word.upper()}' is not in the dictionary." + Style.RESET_ALL)
            continue

        wordle.attempt(input_word)
        refresh_board(wordle)

    if wordle.is_solved:
        print('Solved!')
    else:
        print(f'Failed! The word was {wordle.secret_word}')

    commands = 'play_cmd_wordle.py '
    commands += f'-s {encode_num(seed_int)} ' if secret_word is None else f'-w {secret_word} '
    if word_length != cfg.params.word_length:
        commands += f'-l {word_length}'
    if max_attempts != cfg.params.max_attempts:
        commands += f'-a {max_attempts}'

    print(commands)

    return wordle.secret_word


def refresh_board(wordle: Wordle) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    display_results(wordle)
    print_keyboard(wordle)


def display_results(wordle: Wordle) -> None:

    for word in wordle.attempts:
        result = wordle.check_letters(word)
        print(print_letters(result))

    for _ in range(wordle.remaining_attempts):
        print(' ' + '_ ' * wordle.word_length + Style.RESET_ALL)


def print_letters(result: LettersResult) -> str:
    final_result = []
    for letter in result:
        if letter.in_position:
            color = CORRECT
        elif letter.in_word:
            color = ALMOST
        else:
            color = WRONG

        colored_letter = color + letter.character + Style.RESET_ALL
        final_result.append(colored_letter)
    return ' ' + ' '.join(final_result)


def print_keyboard(wordle: Wordle) -> None:
    row_1 = 'Q W E R T Y U I O P'.split()
    row_2 = 'A S D F G H J K L'.split()
    row_3 = 'Z X C V B N M'.split()

    results = {'green': [], 'yellow': [], 'gray': []}

    # add results from the attempted words to the results dict
    for word in wordle.attempts:
        result = wordle.check_letters(word)
        for letter in result:
            if letter.in_position:
                results['green'].append(letter.character)
            elif letter.in_word:
                results['yellow'].append(letter.character)
            else:
                results['gray'].append(letter.character)

    # print the keyboard with a space between each letter
    print(row_colored(row_1, results))
    print(' ', row_colored(row_2, results))
    print('  ', row_colored(row_3, results))


def row_colored(row: list[str], results: dict[str, list]) -> str:
    row_result = ''
    for letter in row:
        if letter in results['green']:
            row_result += str(CORRECT + letter + Style.RESET_ALL + '  ')
        elif letter in results['yellow']:
            row_result += str(ALMOST + letter + Style.RESET_ALL + '  ')
        elif letter in results['gray']:
            row_result += str(WRONG + letter + Style.RESET_ALL + '  ')
        else:
            row_result += str(NOT_GUESSED + letter + Style.RESET_ALL + '  ')
    return row_result


def load_popular_wordlist(word_length) -> list:
    wordlist = os.path.join(cfg.paths.data, cfg.files.popular_word_list)
    with open(wordlist, 'r') as file:
        word_dict = load(file)
    return word_dict[str(word_length)]


def load_dictionary_wordset(word_length) -> set:
    wordset = os.path.join(cfg.paths.data, cfg.files.dictionary_word_list)
    with open(wordset, 'r') as file:
        word_dict = load(file)
    return set(word_dict[str(word_length)])


def encode_num(num: int) -> str:
    base = BASE
    b_len = len(base)
    digits = []
    while num > 0:
        digits.append(base[num % b_len])
        num //= b_len

    return ''.join(reversed(digits))


def decode_num(seed: str) -> int:
    base = BASE
    b_len = len(base)
    digits = 0
    for char in seed:
        digits *= b_len
        digits += base.index(char)

    return digits


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--word_length', type=int, default=cfg.params.word_length)
    parser.add_argument('-a', '--attempts', type=int, default=cfg.params.max_attempts)
    parser.add_argument('-s', '--seed', type=str, default=None)
    parser.add_argument('-w', '--secret_word', type=str, default=None)
    args = parser.parse_args()
    while True:
        secret = main(word_length=args.word_length,
                      max_attempts=args.attempts,
                      seed=args.seed,
                      secret_word=args.secret_word)
        print("[Enter] to play again, [Q] to quit: ")
        choice = readchar.readchar()
        if choice in ['Q', 'q']:
            break