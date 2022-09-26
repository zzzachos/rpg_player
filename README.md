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
# sample output (excerpted)

```
Running Game with time pause 1

---------- 
Will You Finish Your Novel Today? 

It's the weekend and you have a novel you've been meaning to finish. Will today be the day? 

----------

You rolled a 6.
Outside Interactions: You read some online comments about the book and then started storming through the pages.
bringing your current scores to
Time : 2       Pages : 80       

You rolled a 3.
Cat-Related Events: The cat wanted to go out onto the balcony so you went out there and read in the hammock.
bringing your current scores to
Time : 3       Pages : 70       

You rolled a 6.
Cat-Related Events: The cat wanted to go out onto the balcony so you went out there and read in the hammock.
bringing your current scores to
Time : 4       Pages : 60       

You rolled a 2.
Book-Related Event: You became really bored with this section and couldn't muster up the energy to continue.
bringing your current scores to
Time : 5       Pages : 60       

You rolled a 6.
Book-Related Event: You sat down and were disciplined and got through a decent number of pages, even if you had to force yourself the whole time.
bringing your current scores to
Time : 6       Pages : 50       

You rolled a 5.
Outside Interactions: You suddenly got hungry and went to make yourself a snack.
bringing your current scores to
Time : 7       Pages : 50       

You rolled a 4.
Book-Related Event: You hit a tropey bit you really enjoyed and felt the pages fly by!
bringing your current scores to
Time : 7       Pages : 30       

You rolled a 4.
Outside Interactions: You remembered your book club and redoubled your efforts to read more.
bringing your current scores to
Time : 7       Pages : 20       

You rolled a 6.
Outside Interactions: You read some online comments about the book and then started storming through the pages.
bringing your current scores to
Time : 9       Pages : 0       

WIN: Congratulations! You finished your novel today!

```
