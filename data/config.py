from dataclasses import dataclass
import os
import yaml
from dacite import from_dict


@dataclass
class Paths:
    data: str
    words: str
    wgd: str
    source: str


@dataclass
class Files:
    popular_word_list: str
    dictionary_word_list: str
    dictionary_download_list: str
    other_word_list: str
    wgd_word_list: str
    wgd_english_txt: str
    wgd_english: str
    wgd_twl_txt: str
    wgd_twl: str
    wgd_compound_tmp: str
    wgd_compound: str
    wgd_sowpods_txt: str
    wgd_sowpods: str


@dataclass
class Params:
    word_length: int
    max_attempts: int
    top_word_size: int
    language: str
    seed_max: int


@dataclass
class Urls:
    dict_list: str
    wgd_english: str
    wgd_twl: str
    wgd_compound: str
    wgd_sowpods: str
    wgd_length: str


@dataclass
class Config:
    paths: Paths
    files: Files
    params: Params
    urls: Urls


def load_config() -> Config:
    with open('data/config.yaml', 'r') as f:
        config_file = yaml.load(f, Loader=yaml.FullLoader)

    config_file = from_dict(data_class=Config, data=config_file)
    # take the path.data and replace it with cwd/path.data
    config_file.paths.data = os.path.join(os.getcwd(), config_file.paths.data)
    return config_file


if __name__ == '__main__':
    cfg = load_config()
    print(cfg.paths, type(cfg.paths), end='\n\n')
    print(cfg.paths.data, end='\n\n')
    print(cfg.params)
