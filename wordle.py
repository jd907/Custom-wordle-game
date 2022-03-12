class LettersResult:

    def __init__(self, character: str):
        self.character: str = character
        self.in_word: bool = False
        self.in_position: bool = False

    def __repr__(self) -> str:
        return f'[{self.character}, in_word: {self.in_word}, in_position: {self.in_position}]'


class Wordle:

    def __init__(self, secret_word: str, word_length: int, max_attempts: int):
        self.secret_word: str = secret_word.upper()
        self.word_length = word_length
        self.max_attempts = max_attempts
        self.attempts = []

    # attempt
    def attempt(self, word: str):
        word = word.upper()
        self.attempts.append(word)

    # guess
    def check_letters(self, word: str) -> list:
        word = word.upper()
        result = [LettersResult(character) for character in word]
        secret = list(self.secret_word)

        # check for green letters
        for i in range(self.word_length):
            letter = result[i]
            if letter.character == secret[i]:
                letter.in_position = True
                letter.in_word = True
                secret[i] = '_'

        # check for yellow letters
        for i in range(self.word_length):
            letter = result[i]
            if letter.in_position:
                continue
            for j in range(self.word_length):
                if secret[j] == letter.character:
                    secret[j] = '_'
                    letter.in_word = True
                    break
        return result

    # is it solved?
    @property
    def is_solved(self) -> bool:
        return len(self.attempts) > 0 and self.attempts[-1] == self.secret_word

    # remaining attempts
    @property
    def remaining_attempts(self) -> int:
        return self.max_attempts - len(self.attempts)

    # can attempt be made?
    @property
    def can_attempt(self) -> bool:
        return self.remaining_attempts > 0 and not self.is_solved
