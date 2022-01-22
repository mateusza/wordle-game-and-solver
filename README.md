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

## The demo mode (Game + Solver)

```
$ ./wordle.py --demo
Solver: 5905 possible words.
Solver guessing: hunts
Game response: 🟩⬛⬛⬛⬛
Solver: 74 possible words.
Solver guessing: hooke
Game response: 🟩🟩⬛⬛🟩
Solver: 4 possible words.
Solver guessing: homie
Game response: 🟩🟩⬛⬛🟩
Solver: 3 possible words.
Solver guessing: hoyle
Game response: 🟩🟩⬛⬛🟩
Solver: 2 possible words.
Solver guessing: horde
Game response: 🟩🟩⬛🟨🟩
Solver: 1 possible words.
Solver guessing: hodge
Game response: 🟩🟩🟩🟩🟩
Winner! Word: hodge
```

### Demo mode with given word

```
$ ./wordle.py --demo --word crazy
Solver: 5905 possible words.
Solver guessing: irked
Game response: ⬛🟩⬛⬛⬛
Solver: 141 possible words.
Solver guessing: crams
Game response: 🟩🟩🟩⬛⬛
Solver: 3 possible words.
Solver guessing: crazy
Game response: 🟩🟩🟩🟩🟩
Winner! Word: crazy
```

### Demo mode with custom length
```
 ./wordle.py --length 13 --demo
Solver: 1831 possible words.
Solver guessing: grammatically
Game response: ⬛⬛🟨⬛⬛🟨🟨🟨⬛🟨🟨🟨⬛
Solver: 16 possible words.
Solver guessing: faithlessness
Game response: ⬛🟨🟨🟩⬛🟩⬛🟨🟨🟨⬛🟨🟩
Solver: 2 possible words.
Solver guessing: installations
Game response: 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
Winner! Word: installations
```

### Demo mode in Polish

```
$ ./wordle.py --language polish --length 11 --demo
Solver: 467702 possible words.
Solver guessing: sprasowałam
Game response: ⬛⬛🟨⬛⬛🟨🟨🟩⬛⬛⬛
Solver: 277 possible words.
Solver guessing: wolborzanin
Game response: 🟨🟩⬛⬛⬛🟨🟩🟩🟩🟩⬛
Solver: 2 possible words.
Solver guessing: rozwiązaniu
Game response: 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛
Solver: 1 possible words.
Solver guessing: rozwiązanie
Game response: 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
Winner! Word: rozwiązanie
```

## Languages

Currently **English** and **Polish** are supported in both game, solver and demo.


## Requirements

- Python v3.8 and up
- Dictionaries located in `/usr/share/dict`
    - Ubuntu: `apt-get install wamerican` and others


## Bugs and todo:

- More dictionaries
- Support for other platforms (different dictionary format and location)

