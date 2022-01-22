# Wordle game and solver

[![Python package](https://github.com/mateusza/wordle-game-and-solver/actions/workflows/python-package.yml/badge.svg)](https://github.com/mateusza/wordle-game-and-solver/actions/workflows/python-package.yml)
[![Pylint](https://github.com/mateusza/wordle-game-and-solver/actions/workflows/pylint.yml/badge.svg)](https://github.com/mateusza/wordle-game-and-solver/actions/workflows/pylint.yml)

## The game

```
$ ./wordle.py 
Your guess: track 
🟩🟨⬛⬛⬛
Your guess: three
🟩⬛🟨🟩🟨
Your guess: tiger
🟩🟩⬛🟩🟩
Your guess: timer
🟩🟩⬛🟩🟩
Your guess: tiber
🟩🟩🟩🟩🟩
```


## The solver

```
$ ./wordle.py --solve 
Type your last guess along with response encoded as follows:
- 🟩⬛⬛🟩⬛ => +__+_
- ⬛🟨⬛⬛⬛ => _?___
- 🟩🟨⬛🟨🟨 => +?_??
etc...

Some words to start with: ['prods', 'russo', 'decca', 'ideas',
'tamps', 'solis', 'soddy', 'leaks']
Your last guess and result: track +?___
Words: ['torus', 'tiber', 'tiers', 'turfs', 'their', 'twerp',
'tuner', 'three'] (39 more)
Your last guess and result: three +_?+?
Words: ['tiber', 'tuner', 'tuber', 'tower', 'tiger', 'toner',
'tyler', 'timer']
Your last guess and result: tiger ++_++
Words: ['tiber', 'timer']
Your last guess and result: timer ++_++
Words: ['tiber']
```


## Languages

Currently **English** and **Polish** (`--pl`) are supported in both game and solver.


## Requirements

- Python v3.8 and up
- Dictionaries located in `/usr/share/dict`
    - Ubuntu: `apt-get install wamerican` and others


## Bugs and todo:

- More dictionaries
- Support for other platforms (different dictionary format and location)
- Missing `--help` and `usage`

