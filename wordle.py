from typing import List


class LettersResult:
    """Represents a letter's state in the game of Wordle.

    Attributes:
        character (str): The letter character.
        in_word (bool): Indicates if the letter is in the secret word but not in the correct position.
        in_position (bool): Indicates if the letter is in the correct position in the secret word.
    """
    def __init__(self, character: str):
        self.character: str = character
        self.in_word: bool = False
        self.in_position: bool = False

    def __repr__(self) -> str:
        return f'[{self.character}, in_word: {self.in_word}, in_position: {self.in_position}]'


class Wordle:
    """Implements the Wordle game logic.

    Attributes:
        secret_word (str): The secret word to be guessed.
        word_length (int): The length of the secret word.
        max_attempts (int): The maximum number of attempts allowed.
        attempts (List[str]): The list of attempted words.

    Methods:
        attempt: Record an attempt with the given word.
        check_letters: Check the letters in the word against the secret word.
        is_solved: Check if the word has been solved.
        remaining_attempts: Calculate the remaining attempts.
        can_attempt: Check if another attempt can be made.
    """
    def __init__(self, secret_word: str, word_length: int, max_attempts: int):
        self.secret_word: str = secret_word.upper()
        self.word_length = word_length
        self.max_attempts = max_attempts
        self.attempts: List[str] = []

    def attempt(self, word: str) -> None:
        """Record an attempt with the given word."""
        if len(word) != self.word_length:
            raise ValueError("Invalid word length")
        word = word.upper()
        self.attempts.append(word)

    def check_letters(self, word: str) -> List[LettersResult]:
        """Check the letters in the word against the secret word.

        :param word: The word to check.
        :return: A list of LetterResults.
        """
        if len(word) != self.word_length:
            raise ValueError("Invalid word length")

        word = word.upper()
        result = [LettersResult(character) for character in word]
        secret = list(self.secret_word)

        # check for in_position (green) letters
        for i in range(self.word_length):
            letter = result[i]
            if letter.character == secret[i]:
                letter.in_position = True
                letter.in_word = True
                secret[i] = '_'

        # check for in_word (yellow) letters using a set to reduce complexity
        secret_set = set(secret)
        for i in range(self.word_length):
            letter = result[i]
            if letter.in_position:
                continue
            if letter.character in secret_set:
                secret_set.remove(letter.character)
                letter.in_word = True

        return result

    @property
    def is_solved(self) -> bool:
        """Check if the word has been solved."""
        return len(self.attempts) > 0 and self.attempts[-1] == self.secret_word

    @property
    def remaining_attempts(self) -> int:
        """Calculate the remaining attempts."""
        return self.max_attempts - len(self.attempts)

    @property
    def can_attempt(self) -> bool:
        """Check if another attempt can be made."""
        return self.remaining_attempts > 0 and not self.is_solved
