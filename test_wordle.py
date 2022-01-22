#!/usr/bin/env python3

"""Pytest module for wordle"""

import pytest
import wordle

@pytest.mark.parametrize('testspec', [
    'pudło psalm +____',
    'palny psalm +??__',
    'plaga psalm +?+__',
    'trasa psalm __+?_',
    'psalm psalm +++++',

    'nudes wince ?__?_',
    'lemon wince _?__?',
    'agent wince __??_',
    'knife wince _??_+',
    'wince wince +++++',
])
def test_verdict(testspec):
    """Test wordle.verdict() function"""

    guess, word, verdict = testspec.split(' ')
    assert wordle.verdict(guess, word) == verdict
    assert wordle.match_verdict(verdict, word, guess)

@pytest.mark.parametrize('testspec', [
    'pudło psalm +_?__',
    'nudes wince ?_+__',
])
def test_match_verdict_wrong(testspec):
    """Test wordle.match_verdict() with incorrect param"""

    guess, word, verdict = testspec.split(' ')
    assert not wordle.match_verdict(guess, word, verdict)


@pytest.mark.parametrize('testspec', [
    '🟩⬛⬛🟩⬛ +__+_',
    '⬛🟨⬛⬛⬛ _?___',
    '🟩🟨⬛🟨🟨 +?_??',
])
def test_color_verdict(testspec):
    """Test wordle.Game.color_verdict()"""

    color, asci = testspec.split(' ')
    assert wordle.Game.color_verdict(asci) == color


def test_game1():
    """Simulate a game"""

    language = 'american-english'

    secret = 'wince'
    steps = ['nudes ?__?_', 'lemon _?__?', 'agent __??_', 'knife _??_+', 'wince +++++']

    game = wordle.Game.new(language=language, word=secret)

    for step in steps:
        guess, exp_verdict = step.split(' ')
        result = game.guess(guess)
        assert result['guess'] == guess
        assert result['verdict'] == exp_verdict

    assert result['won']


@pytest.mark.parametrize('testspec', [
    'picks',
    'nudes',
    'jokes',
    'track',
    'shops',
    'badge',
    'linux',
])
def test_game_and_solver(testspec):
    """Simulate a game and let Solver win it"""

    language = 'american-english'

    secret = testspec
    game = wordle.Game.new(language=language, word=secret)
    solver = wordle.Solver.new(language=language)

    while True:
        print(f"Solver: {len(solver.possible)} possible words.")
        assert len(solver.possible) > 0
        my_guess = [*solver.possible][0]
        print(f'Solver guessing: {my_guess}')
        result = game.guess(my_guess)
        print(f'Game result: {result}')
        assert result['guess'] == my_guess
        if result['won']:
            print(f'Winner! word: {my_guess}')
            break
        solver.update(my_guess, result['verdict'])


@pytest.mark.parametrize('i', range(100))
def test_game_and_solver_random(i):
    """Simulate a game and let Solver win it"""

    language = 'american-english'

    game = wordle.Game.new(language=language)
    solver = wordle.Solver.new(language=language)

    print(f'Unknown word run #{i}')
    while True:
        print(f"Solver: {len(solver.possible)} possible words.")
        assert len(solver.possible) > 0
        my_guess = [*solver.possible][0]
        print(f'Solver guessing: {my_guess}')
        result = game.guess(my_guess)
        print(f'Game result: {result}')
        assert result['guess'] == my_guess
        if result['won']:
            print(f'Winner! word: {my_guess}')
            break
        solver.update(my_guess, result['verdict'])

@pytest.mark.parametrize('length', range(2, 20))
def test_game_and_solver_lengths(length):
    """Simulate a game and let Solver win it"""

    language = 'american-english'

    game = wordle.Game.new(language=language, length=length)
    solver = wordle.Solver.new(language=language, length=length)

    print(f'Unknown word (length {length})')
    while True:
        print(f"Solver: {len(solver.possible)} possible words.")
        assert len(solver.possible) > 0
        my_guess = [*solver.possible][0]
        print(f'Solver guessing: {my_guess}')
        result = game.guess(my_guess)
        print(f'Game result: {result}')
        assert result['guess'] == my_guess
        if result['won']:
            print(f'Winner! word: {my_guess}')
            break
        solver.update(my_guess, result['verdict'])

LANGUAGES = ['american-english', 'polish']

@pytest.mark.parametrize('lang', LANGUAGES)
def test_game_and_solver_langs(lang):
    """Simulate a game and let Solver win it"""

    language = lang

    game = wordle.Game.new(language=language)
    solver = wordle.Solver.new(language=language)

    print(f'Unknown word in {lang = })')
    while True:
        print(f"Solver: {len(solver.possible)} possible words.")
        assert len(solver.possible) > 0
        my_guess = [*solver.possible][0]
        print(f'Solver guessing: {my_guess}')
        result = game.guess(my_guess)
        print(f'Game result: {result}')
        assert result['guess'] == my_guess
        if result['won']:
            print(f'Winner! word: {my_guess}')
            break
        solver.update(my_guess, result['verdict'])
