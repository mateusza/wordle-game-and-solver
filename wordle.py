#!/usr/bin/env python3

# author: Mateusz Adamowski <mateusz at adamowski dot pl>
#
# homepage: https://github.com/mateusza/wordle-game-and-solver

"""Play and solve wordle"""

import argparse
import functools
import random

CHARSETS: dict = {
    'american-english': 'abcdefghijklmnopqrstuvwxyz',
    'esperanto': 'abcdefghijklmnopqrstuvwxyzĉĝĥĵŝŭ',
    'french': 'abcdefghijklmnopqrstuvwxyzù',
    'german-medical': 'abcdefghijklmnopqrstuvwxyzßäöü',
    'italian': 'abcdefghijklmnopqrstuvwxyzàèéìòù',
    'polish': 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź',
}


def verdict(the_guess: str, the_word: str) -> str:
    "Verdict"
    if len(the_guess) != len(the_word):
        raise ValueError(f'Length mismatch: {the_guess=} {the_word=}')

    matched = [a == b for a, b in zip(the_guess, the_word)]

    mismatched = [letter for ok, letter in zip(matched, the_word) if not ok]

    result = ''

    for is_ok, guessed_letter in zip(matched, the_guess):
        if is_ok:
            result += '+'
            continue
        if guessed_letter in mismatched:
            result += '?'
            mismatched.remove(guessed_letter)
            continue
        result += '_'

    return result

def match_verdict(the_verdict: str, the_word: str, the_guess: str) -> bool:
    "Check if given word would result in given verdict"
    return verdict(the_guess, the_word) == the_verdict


class Wordset:
    "Set of words to be used in a game or in solving"
    words: set
    def __init__(self, words=None):
        if words is None:
            words = []
        self.words = {*words}


    def get_random(self) -> str:
        "Returns random word from set"
        return random.choice([*self.words])


    def get_random_list(self, length: int = 10) -> list:
        "Return random list of words no longer than length."
        new_length = min(length, len(self.words))
        return random.sample(self.words, new_length)


    @classmethod
    def load_dict(cls, language: str, length: int = 5) -> 'Wordset':
        "Load words from system dictionary"

        location: str = '/usr/share/dict'
        filename: str = f'{location}/{language}'
        charset: set = cls.get_charset(language)
        words: set = Wordset.load_words(filename, charset, length)
        return cls(words=words)


    @staticmethod
    @functools.lru_cache(128)
    def load_words(filename: str, only_chars=None, length: int = 5) -> set:
        "Load words of given length from text file"

        words = set()
        if only_chars is not None:
            charset = set(only_chars)
        with open(filename, 'r', encoding='UTF-8') as src_file:
            for line in src_file:
                word = line.strip().lower()
                if len(word) != length:
                    continue
                if not set(word) < charset:
                    continue
                words.add(word)
        return words


    @staticmethod
    def get_charset(language: str) -> str:
        "Get charset for given language"
        return CHARSETS[language]


class Game:
    "Class to play wordle locally"

    language: str
    wordset: set
    charset: set
    word: str
    won: bool
    guesses: list
    verdicts: list


    def __init__(self, wordset: str, charset: str):
        self.wordset = wordset
        self.charset = charset


    def start(self, word: str = None):
        "Reset the game"

        if word is not None:
            self.wordset.words.add(word)
            self.word = word
        else:
            self.word = self.wordset.get_random()
        self.won = False
        self.guesses = []
        self.verdicts = []


    def guess(self, the_guess: str) -> dict:
        "Make a guess, change game state"

        if the_guess not in self.wordset.words:
            ...
        elif self.won:
            ...
        else:
            try:
                verd = verdict(the_guess, self.word)
                self.guesses.append(the_guess)
                self.verdicts.append(verd)
                if set(verd) == {'+'}:
                    self.won = True
            except ValueError:
                verd = None
        result = {
            'guess': self.guesses[-1] if self.guesses else None,
            'verdict': self.verdicts[-1] if self.verdicts else None,
            'won': self.won
        }
        return result


    @classmethod
    def new(cls, language: str, word: str = None, length: int = 5):
        "Create a new game object, load wordset in given language, start the game."

        wordset = Wordset.load_dict(language, length=length)
        charset = Wordset.get_charset(language)
        game = cls(wordset=wordset, charset=charset)
        game.start(word=word)
        return game


    @staticmethod
    def color_verdict(the_verdict: str) -> str:
        "Return color-coded verdict"

        translations = '_⬛+🟩?🟨'
        trans_table = {ord(a): b for a, b in zip(translations[0::2], translations[1::2])}
        return the_verdict.translate(trans_table)


class Solver:
    "Solve wordle challenge"

    language: str
    wordset: Wordset
    charset: set
    guesses: list
    verdicts: list
    possible: Wordset

    def __init__(self, wordset: str, charset: str):
        self.wordset = wordset
        self.charset = charset

    def start(self):
        "Initialize the solver"

        self.guesses = []
        self.verdicts = []
        self.possible = Wordset(words=self.wordset.words)

    @classmethod
    def new(cls, language: str, length: int = 5):
        "Create new solver, load wordset in given language"

        wordset = Wordset.load_dict(language, length)
        charset = Wordset.get_charset(language)
        solver = cls(wordset=wordset, charset=charset)
        solver.start()
        return solver

    def update(self, the_guess, the_verdict):
        "Update solver's state, filter out words that don't match"

        self.guesses.append(the_guess)
        self.verdicts.append(the_verdict)
        possible = {w for w in self.possible.words if match_verdict(the_verdict, w, the_guess)}
        self.possible = Wordset(words=possible)


def play_wordle(language: str, word: str = None, length: int = 5) -> None:
    "Play a game in CLI"

    game = Game.new(language, word=word, length=length)
    while True:
        your_guess = input("Your guess: ").lower()
        result = game.guess(your_guess)
        the_verdict = result['verdict']
        if result['guess'] != your_guess:
            print("Wrong word, ignoring")
            continue
        print(Game.color_verdict(the_verdict))

        if result['won']:
            break


def solve_wordle(language: str, length: int = 5) -> None:
    "Solve wordle game in CLI"

    hint_len = 8
    solver = Solver.new(language, length=length)
    print("Type your last guess along with response encoded as follows:")
    examples = ['+__+_', '_?___', '+?_??']
    for ex in examples:
        print("- " + Game.color_verdict(ex) + ' => ' + ex)
    print('etc...')
    print()
    while True:
        while True:
            hints = ', '.join(solver.possible.get_random_list(hint_len))
            more = len(solver.possible.words) - hint_len
            print(f'Possible words: {hints}' + (f' ({more} more)' if more > 0 else ''))
            state = input('Your last guess and result: ')
            try:
                guess, the_verdict = state.split(" ")
                assert len(guess) == length
                assert len(the_verdict) == length
            except (AssertionError, ValueError):
                print("Wrong value. Try again.")
                continue
            break
        solver.update(guess, the_verdict)
        if len(solver.possible.words) == 1:
            word = solver.possible.get_random()
            print(f"Final guess: {word}")
            break
        if len(solver.possible.words) == 0:
            print('Empty word list! No idea!')
            break


def demo_mode(language: str, word: str = None, length: int = 5, words_to_try: list = None) -> None:
    """Computer plays against itself"""

    if words_to_try is None:
        words_to_try = []

    game = Game.new(language=language, word=word, length=length)
    solver = Solver.new(language=language, length=length)

    while True:
        print(f"Solver: {len(solver.possible.words)} possible words.")
        if len(words_to_try) > 0:
            my_guess = words_to_try.pop(0)
        else:
            my_guess = solver.possible.get_random()
        print(f'Solver guessing: {my_guess}')
        result = game.guess(my_guess)
        color_verd = Game.color_verdict(result['verdict'])
        print(f'Game response: {color_verd}')
        assert result['guess'] == my_guess
        if result['won']:
            print(f'Winner! Word: {my_guess}')
            break
        solver.update(my_guess, result['verdict'])


def main(): # pragma: no cover
    "The main()"

    parser = argparse.ArgumentParser(description='Play or solve wordle')
    parser.add_argument('-l', '--language',
                        nargs=1, default=['american-english'], help='language to use')
    parser.add_argument('-s', '--solve', action='store_true', help='solving mode')
    parser.add_argument('-d', '--demo', action='store_true', help='let solver play')
    parser.add_argument('-w', '--word', nargs=1, help='secret word to guess (testing and demo)')
    parser.add_argument('-n', '--length',
                        nargs=1, default=[5], type=int, help='word length')
    parser.add_argument('--pl', action='store_true', help='Set language to Polish')
    parser.add_argument('-t', '--try-words',
                        nargs=1, default=[''],
                        help='Words to try first in demo mode (comma separated)')

    args = parser.parse_args()

    if args.pl:
        args.language = ['polish']

    word = args.word[0] if args.word else None
    language = args.language[0] if args.language else None
    length = args.length[0]
    words_to_try = args.try_words[0].split(',') if args.try_words[0] else []

    if args.word:
        length = len(word)

    try:
        if args.solve:
            solve_wordle(language=language, length=length)
        elif args.demo:
            demo_mode(language=language, word=word, length=length, words_to_try=words_to_try)
        else:
            play_wordle(language=language, word=word, length=length)
    except (KeyboardInterrupt, EOFError):
        print("Bye")


if __name__ == '__main__': # pragma: no cover
    main()
