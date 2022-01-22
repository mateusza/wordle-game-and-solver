#!/usr/bin/env python3

# author: Mateusz Adamowski <mateusz at adamowski dot pl>
#
# homepage: https://github.com/mateusza/wordle-game-and-solver

"""Play and solve wordle"""

import argparse
import functools
import random


def verdict(the_guess: str, the_word: str) -> str:
    "Verdict"
    if len(the_guess) != len(the_word):
        raise ValueError(f'Length mismatch: {the_guess=} {the_word=}')
    def encode(letter_a, letter_b) -> str:
        return '+' if letter_a == letter_b else '?' if letter_a in the_word else '_'
    return ''.join([encode(g, w) for g, w in zip(the_guess, the_word)])


def match_verdict(the_verdict: str, the_word: str, the_guess: str) -> bool:
    "Check if given word would result in given verdict"
    return verdict(the_guess, the_word) == the_verdict


class Wordset:
    "Set of words to be used in a game or in solving"
    words: set
    def __init__(self, words=None):
        if words is None:
            words = []
        self.words = words


    @classmethod
    def load_dict(cls, language: str) -> 'Wordset':
        "Load words from system dictionary"

        location: str = '/usr/share/dict'
        filename: str = f'{location}/{language}'
        charset: set = cls.get_charset(language)
        words: set = Wordset.load_words(filename, charset, 5)
        return cls(words=words)


    @staticmethod
    @functools.lru_cache(128)
    def load_words(filename: str, only_chars=None, length: int = 5) -> set:
        "Load words of given length from text file"

        words = set()
        if only_chars is not None:
            charset = set(only_chars)
        with open(filename, 'r') as src_file:
            for line in src_file:
                word = line.strip().lower()
                if len(word) != length:
                    continue
                if only_chars and any(letter not in charset for letter in word):
                    continue
                words.add(word)
        return words


    @staticmethod
    def get_charset(language: str) -> str:
        "Get charset for given language"

        charsets: dict = {
            'polish': 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź',
            'american-english': 'abcdefghijklmnopqrstuvwxyz'
        }
        return charsets[language]


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
            self.word = random.choice([*self.wordset.words])
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
                if verd == '+++++':
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
    def new(cls, language: str, word: str = None):
        "Create a new game object, load wordset in given language, start the game."

        wordset = Wordset.load_dict(language)
        charset = Wordset.get_charset(language)
        game = cls(wordset=wordset, charset=charset)
        game.start(word=word)
        return game


    @staticmethod
    def color_verdict(the_verdict: str) -> str:
        "Return color-coded verdict"
        return the_verdict.replace('_', '⬛').replace('+', '🟩').replace('?', '🟨')


class Solver:
    "Solve wordle challenge"

    language: str
    wordset: set
    charset: set
    guesses: list
    verdicts: list
    possible: list

    def __init__(self, wordset: str, charset: str):
        self.wordset = wordset
        self.charset = charset

    def start(self):
        "Initialize the solver"

        self.guesses = []
        self.verdicts = []
        self.possible = [*self.wordset.words]

    @classmethod
    def new(cls, language: str):
        "Create new solver, load wordset in given language"

        wordset = Wordset.load_dict(language)
        charset = Wordset.get_charset(language)
        solver = cls(wordset=wordset, charset=charset)
        solver.start()
        return solver

    def update(self, the_guess, the_verdict):
        "Update solver's state, filter out words that don't match"

        self.guesses.append(the_guess)
        self.verdicts.append(the_verdict)
        self.possible = [w for w in self.possible if match_verdict(the_verdict, w, the_guess)]


def play_wordle(language: str, word: str = None) -> None:
    "Play a game in CLI"

    game = Game.new(language, word=word)
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


def solve_wordle(language: str) -> None:
    "Solve wordle game in CLI"

    hint_len = 8
    solver = Solver.new(language)
    print("Type your last guess along with response encoded as follows:")
    examples = ['+__+_', '_?___', '+?_??']
    for ex in examples:
        print("- " + Game.color_verdict(ex) + ' => ' + ex)
    print('etc...')
    print()
    hints = solver.possible[:hint_len]
    print(f'Some words to start with: {hints}')
    while True:
        while True:
            state = input('Your last guess and result: ')
            try:
                guess, the_verdict = state.split(" ")
                assert len(guess) == 5
                assert len(the_verdict) == 5
            except (AssertionError, ValueError):
                print("Wrong value. Try again.")
                continue
            break
        solver.update(guess, the_verdict)
        hints = solver.possible[:hint_len]
        more = len(solver.possible) - hint_len
        print(f'Words: {hints}' + (f' ({more} more)' if more > 0 else ''))
        if len(solver.possible) <= 1:
            break

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Play or solve wordle')
    parser.add_argument('-l', '--language',
            nargs=1, default='american-english', help='language to use')
    parser.add_argument('-s', '--solve', action='store_true', help='solving mode')
    parser.add_argument('-w', '--word', nargs=1, help='secret word to guess (testing and demo)')
    parser.add_argument('--pl', action='store_true', help='Set language to Polish')

    args = parser.parse_args()

    if args.pl:
        args.language = 'polish'

    word = args.word[0] if args.word is not None else None

    try:
        if args.solve:
            solve_wordle(args.language)
        else:
            play_wordle(args.language, word=word)
    except KeyboardInterrupt:
        print("Bye")
