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
    assert wordle.match_verdict(verdict, word, guess) == True

@pytest.mark.parametrize('testspec', [
    'pudło psalm +_?__',
    'nudes wince ?_+__',
])
def test_match_verdict_wrong(testspec):
    """Test wordle.match_verdict() with incorrect param"""

    guess, word, verdict = testspec.split(' ')
    assert wordle.match_verdict(guess, word, verdict) == False
    

@pytest.mark.parametrize('testspec', [
    '🟩⬛⬛🟩⬛ +__+_',
    '⬛🟨⬛⬛⬛ _?___',
    '🟩🟨⬛🟨🟨 +?_??',
])
def test_color_verdict(testspec):
    """Test wordle.Game.color_verdict()"""

    color, ascii = testspec.split(' ')
    assert wordle.Game.color_verdict(ascii) == color

