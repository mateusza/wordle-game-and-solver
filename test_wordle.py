#!/usr/bin/env python3

import pytest
import wordle

@pytest.mark.parametrize('t', [
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
def test_verdict(t):
    g, w, v = t.split(' ')
    assert wordle.verdict(g, w) == v
