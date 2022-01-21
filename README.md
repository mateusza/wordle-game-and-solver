# Wordle game and solver


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

Some words to start with: ['erase', 'finny', 'elate', 'fists', 'spite', 'leaks', 'hymns', 'fuchs', 'coves', 'myers', 'filly', 'sammy', 'murks', 'myles', 'eject', 'sexed', 'abbot', 'sakha', 'capri', 'sykes']
Your last guess and result: track +?___
Words: ['turds', 'tyler', 'throb', 'timur', 'tiers', 'three', 'tuber', 'tumor', 'tiger', 'terse', 'torte', 'tiros', 'throe', 'third', 'terms', 'tenor', 'torts', 'timer', 'terry', 'turns'] (27 more)
Your last guess and result: three +_?+?
Words: ['tyler', 'tuber', 'tiger', 'timer', 'tower', 'tiber', 'toner', 'tuner']
Your last guess and result: tiger ++_++
Words: ['timer', 'tiber']
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

