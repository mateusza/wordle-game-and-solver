#!/usr/bin/env python3


import argparse
import functools
import random
import sys

def verdict(the_guess: str, the_word: str) -> str:
    if len(the_guess) != len(the_word):
        raise ValueError(f'Length mismatch: {the_guess=} {the_word=}')
    return ''.join(['+' if a==b else '?' if a in the_word else '_' for a, b in zip(the_guess, the_word)])


def match_verdict(the_verdict: str, the_word: str, the_guess: str) -> bool:
    return verdict(the_guess, the_word) == the_verdict


class Wordset:
    words: set
    def __init__(self, words=[]):
        self.words = words


    @classmethod
    def load_dict(cls, language: str) -> 'Wordset':
        location: str = '/usr/share/dict'
        filename: str = f'{location}/{language}'
        charset: set = cls.get_charset(language)
        words: set = Wordset.load_words(filename, charset, 5)
        return cls(words=words)


    @staticmethod
    @functools.lru_cache(128)
    def load_words(filename: str, only_chars=None, length: int = 5) -> set:
        words = set()
        if only_chars != None:
            charset = set(only_chars)
        with open(filename, 'r') as f:
            for line in f:
                word = line.strip().lower()
                if len(word) != length:
                    continue
                if only_chars and any(letter not in charset for letter in word):
                    continue
                words.add(word)
        return words


    @staticmethod
    def get_charset(language: str) -> str:
        charsets: dict = {
            'polish': 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź',
            'american-english': 'abcdefghijklmnopqrstuvwxyz'
        }
        return charsets[language]


class Game:
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


    def start(self):
        self.word = random.choice([*self.wordset.words])
        self.won = False
        self.guesses = []
        self.verdicts = []


    def guess(self, the_guess: str) -> dict:
        if the_guess not in self.wordset.words:
            ...
        elif self.won:
            ...
        else:
            try:
                v = verdict(the_guess, self.word)
                self.guesses.append(the_guess)
                self.verdicts.append(v)
                if ''.join(v) == '+++++':
                    self.won = True
            except ValueError:
                v = None
        result = {
            'guess': self.guesses[-1] if self.guesses else None,
            'verdict': self.verdicts[-1] if self.verdicts else None,
            'won': self.won
        }
        return result


    @classmethod
    def new(cls, language: str):
        wordset = Wordset.load_dict(language)
        charset = Wordset.get_charset(language)
        g = cls(wordset=wordset, charset=charset)
        g.start()

        return g


    @staticmethod
    def color_verdict(the_verdict: str) -> str:
        return the_verdict.replace('_', '⬛').replace('+', '🟩').replace('?', '🟨')


class Solver:
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
        self.guesses = []
        self.verdicts = []
        self.possible = [*self.wordset.words]

    @classmethod
    def new(cls, language: str):
        wordset = Wordset.load_dict(language)
        charset = Wordset.get_charset(language)
        s = cls(wordset=wordset, charset=charset)
        s.start()
        return s

    def update(self, the_guess, the_verdict):
        self.guesses.append(the_guess)
        self.verdicts.append(the_verdict)
        self.possible = [w for w in self.possible if match_verdict(the_verdict, w, the_guess)]


def play_wordle(language: str) -> None:
    game = Game.new(language)
    while True:
        your_guess = input("Your guess: ").lower()
        result = game.guess(your_guess)
        verdict = result['verdict']
        if result['guess'] != your_guess:
            print("Wrong word, ignoring")
            continue
        print(Game.color_verdict(verdict))

        if result['won']:
            break


def solve_wordle(language: str) -> None:
    hint_len = 20
    solver = Solver.new(language)
    print("Type your last guess along with response encoded as follows:")
    examples = ['+____', '_?___']
    for ex in examples:
        print("- " + Game.color_verdict(ex) + ' => ' + ex)
    print('etc...')
    print()
    hints = solver.possible[:hint_len]
    print(f'Some words to start with: {hints}')
    while True:
        state = input('Your last guess and result:')
        guess, verdict = state.split(" ")
        solver.update(guess, verdict)
        hints = solver.possible[:hint_len]
        more = len(solver.possible) - hint_len
        print(f'Words: {hints}' + (f' ({more} more)' if more > 0 else ''))
        if len(solver.possible) <= 1:
            break

if __name__ == '__main__':

    lang = 'american-english'
    mode = 'PLAY'

    for a in sys.argv:
        if a == '--pl':
            lang = 'polish'
        if a == '--solve':
            mode = 'SOLVE'

    if mode == 'SOLVE':
        solve_wordle(lang)
    else:
        play_wordle(lang)

