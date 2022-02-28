from base64 import encode
from json import load
import os, string, random
from config import load_config
import requests

cfg = load_config()
from PyMultiDictionary import MultiDictionary, DICT_WORDNET

dictionary = MultiDictionary()
BASE = string.digits + string.ascii_lowercase


def generate_seed() -> int:
    return random.randint(0, 999_999)


def encode_num(num: int) -> str:
    base = BASE
    b_len = len(base)
    digits = []
    while num > 0:
        digits.append(base[num % b_len])
        num //= b_len

    return ''.join(reversed(digits))


def decode_num(num: str) -> int:
    base = BASE
    b_len = len(base)
    digits = 0
    for char in num:
        digits *= b_len
        digits += base.index(char)

    return digits


if __name__ == '__main__':
    word = 'hello'
    req = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    print(req.json())
    # synonym = dictionary.synonym(cfg.params.language, word)
    # print(synonym)
    # meaning = dictionary.meaning('en', word, dictionary=DICT_WORDNET)
    # print(type(meaning))
    # for key, value in meaning.items():
    #     for entry in value:
    #         print(key, entry)
