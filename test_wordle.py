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
