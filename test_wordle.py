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

    'token crimp _____',
    'claws crimp +____',
    'crumb crimp ++_+_',
    'crimp crimp +++++',

    'kwiat struś ____?',
    'tempo struś ?____',
    'butny struś _??__',
    'gluty struś __??_',
    'struł struś ++++_',
    'struś struś +++++',

    'eager dance ?+___',
    'cache dance ?+__+',
    'motto knoll _?___',
    'alloy knoll _???_',
])
def test_verdict(testspec):
    """Test wordle.verdict() function"""

    guess, word, verdict = testspec.split(' ')
    assert wordle.verdict(guess, word) == verdict
    assert wordle.match_verdict(verdict, word, guess)


def test_verdict_length_mismatch():
    """Test wordle.verdict() with mismatched arguments"""

    with pytest.raises(ValueError):
        wordle.verdict("abcdefg", "xyz")


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

@pytest.mark.parametrize('testspec', [
    ('american-english', 'wince',
     ['nudes ?__?_', 'lemon _?__?', 'agent __??_', 'knife _??_+', 'wince +++++']
    ),
    ('polish', 'struś',
     ['kwiat ____?', 'tempo ?____', 'butny _??__', 'gluty __??_', 'struł ++++_',
      'struś +++++']
    ),
    ('polish', 'minus',
     ['bitwa _+___', 'nisko ?+?__', 'minus +++++']
    ),
    ('american-english', 'knoll',
     ['basic _____', 'lemon ?__??', 'knoll +++++']
    ),
    ('american-english', 'sugar',
     ['opera ___??', 'sugar +++++']
    ),
    ('polish', 'basta',
     ['opera ____+', 'żabka _+?_+', 'banda ++__+', 'basta +++++']
    ),
    ('american-english', 'whack',
     ['opera ____?', 'facts _??__', 'chain ?++__', 'whack +++++']
    ),
    ('polish', 'stary',
     ['krowa _?__?', 'zegar ___??', 'narty _???+', 'stary +++++']
    )
])
def test_game1(testspec):
    """Simulate a game"""

    language, secret, steps = testspec

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
        print(f"Solver: {solver.count} possible words.")
        assert solver.count > 0
        my_guess = solver.guess()
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
        print(f"Solver: {solver.count} possible words.")
        assert solver.count > 0
        my_guess = solver.guess()
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
        print(f"Solver: {solver.count} possible words.")
        assert solver.count > 0
        my_guess = solver.guess()
        print(f'Solver guessing: {my_guess}')
        result = game.guess(my_guess)
        print(f'Game result: {result}')
        assert result['guess'] == my_guess
        if result['won']:
            print(f'Winner! word: {my_guess}')
            break
        solver.update(my_guess, result['verdict'])

LANGUAGES = wordle.CHARSETS.keys()

@pytest.mark.parametrize('lang', LANGUAGES)
def test_game_and_solver_langs(lang):
    """Simulate a game and let Solver win it"""

    language = lang

    game = wordle.Game.new(language=language)
    solver = wordle.Solver.new(language=language)

    print(f'Unknown word in {lang = })')
    while True:
        print(f"Solver: {solver.count} possible words.")
        assert solver.count > 0
        my_guess = solver.guess()
        print(f'Solver guessing: {my_guess}')
        result = game.guess(my_guess)
        print(f'Game result: {result}')
        assert result['guess'] == my_guess
        if result['won']:
            print(f'Winner! word: {my_guess}')
            break
        solver.update(my_guess, result['verdict'])


def test_empty_wordset():
    "Test empty Wordset"
    wordset = wordle.Wordset()
    assert wordset


@pytest.mark.parametrize('lang', LANGUAGES)
def test_wordset_get_random(lang):
    "Test get_random()"
    wordset = wordle.Wordset.load_dict(lang)

    word = wordset.get_random()

    assert word in wordset.words

@pytest.mark.parametrize('length', [1, 2, 5, 10, 100, 1000, 10000, 100000])
def test_wordset_get_random_list(length):
    "Test get_random_list()"
    lang = 'american-english'
    wordset = wordle.Wordset.load_dict(lang)
    words = wordset.get_random_list(length)

    assert len(words) == length or len(words) == len(wordset.words)
