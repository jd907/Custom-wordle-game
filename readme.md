# Custom Python Wordle
This project has both a wordle object for future projects, playable through terminal, and downloads a word list. Currently supports 4-15 letter words. This project is heavily inspired by the plethora of wordle projects on the internet, but I tried to make it my own.

---
## How to use
Use Python 3.10 or later.
1. Git clone or download as zip.
2. `pip install requirements.txt` (I recommend you make a virtual environment first)
3. run `python data/refresh_all_words.py` to download the word list. (May have to google how to run python files on your operating system)
4. run `python play_cmd_wordle.py` (run `python play_cmd_wordle.py -h` for more info on options)

If you want to change any settings of the word list or program, edit data/config.yaml

---
### Todo

- [ ] Wordle hinter
- [ ] Web version
