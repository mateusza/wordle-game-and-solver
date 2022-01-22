# Wordle game and solver

[![Python package](https://github.com/mateusza/wordle-game-and-solver/actions/workflows/python-package.yml/badge.svg)](https://github.com/mateusza/wordle-game-and-solver/actions/workflows/python-package.yml)
[![Pylint](https://github.com/mateusza/wordle-game-and-solver/actions/workflows/pylint.yml/badge.svg)](https://github.com/mateusza/wordle-game-and-solver/actions/workflows/pylint.yml)

## The game

```
$ ./wordle.py 
Your guess: dirty
⬛⬛🟨⬛⬛
Your guess: gears
⬛🟨🟨🟨⬛
Your guess: baker
⬛🟩⬛🟩🟩
Your guess: paper
⬛🟩🟩🟩🟩
Your guess: caper
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

Some words to start with: abate, plead, dally, spray, rumps, legit, euler, serge
Your last guess and result: dirty __?__
Words: rumps, euler, hover, sucre, gears, mourn, rhone, peers (496 more)
Your last guess and result: gears _???_
Words: waver, creak, haler, freak, lamer, abler, haber, baker (21 more)
Your last guess and result: baker _+_++
Words: waver, haler, lamer, wafer, racer, caper, paper, laxer (2 more)
Your last guess and result: paper _++++
Words: caper
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

