# rpg_player
A one-player RPG player and simulator.

This was quickly thrown together 2022/09/25 and I probably will go through and clean it up a bit at some point.

# background
I was inspired to do so after seeing the following one page RPG: https://twitter.com/Sotherans/status/1513210507506954250

# contents
I've included a json with the scores from that game (excepting the special 5-5-5 rule which I was too lazy to add), a game about finishing a novel, and a blank template.

# how to run
There are two modes. 
(1) Simulation mode: 
```
python rpg_simulator.py 1 10000 FinishNovel_game.json
```
(2) Game play mode, where you can enter the size of pause (in seconds) that you want:

```
python rpg_simulator.py 0 2 FinishNovel_game.json
```
