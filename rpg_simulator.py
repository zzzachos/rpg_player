import numpy as np
from enum import Enum
from hide_prints import *
from rpg_ruleset import *

import time
import sys

class GameState(Enum):
    ONGOING = 1
    WIN = 2
    LOSE = 3
    INVALID = 4


class Game:
    def __init__(self, rules : RuleSet):
      self.scores_dim, self.score_size, self.die_size = rules.reportSizes()
      # scores for each dimension
      self.verbose_mode = False
      self.rules = rules
      self.state = GameState.ONGOING
      if not rules.reportFullyDefined():
          self.state = GameState.INVALID
      self.scores = np.array(self.rules.starting_scores.copy())
      self.roll_record = []
      self.steps = 0
      self.final_state = -1
    # end init (Simulator)
    
    def reportGameState(self) -> GameState:
        return self.state
        
    def setVerboseMode(self, mode):
        self.verbose_mode = mode
        if self.verbose_mode == True:
            print(self.rules.title, "\n")
            print(self.rules.description, "\n")
            print("----------\n")
        
    def rollDie(self) -> int:
        self.roll_record.append(np.random.randint(0, self.die_size))
        return self.roll_record[-1]
    
    def reportScores(self) -> str:
        report = ""
        for i in range (self.scores_dim):
            report+=self.rules.score_names[i]+ " : " + str(self.scores[i]) + "       "#+ "\n"
        report+="\n"
        return report
    
    def step(self):
        die_roll = self.rollDie()
        rule = self.rules.getRule(die_roll)
        die_roll = self.rollDie()
        self.scores += rule.getScoreUpdates(die_roll)
        if self.verbose_mode:
            print(f"You rolled a %d."%(die_roll+1))
            print(rule.getDescription(die_roll))
            print("bringing your current scores to")
            print(self.reportScores())
        idx = self.isGameDone()
        if idx > -1: 
            self.state = GameState.WIN if self.rules.good_end[idx] else GameState.LOSE
        return
    
    def play(self, pause : int = 0, verbose_mode : bool = False):
        if self.state == GameState.INVALID:
            print("Can not play. Game is invalid.")
            return
        self.setVerboseMode(verbose_mode)
        while self.state == GameState.ONGOING:
            self.step()
            if pause > 0:
                time.sleep(pause)
            if self.steps > 100000:
                print("The game went for 100000 steps and was halted because it hit that limit without terminating.")
                return
        idx = self.state_at_end
        if verbose_mode:
            if idx >-1:
                print(self.rules.ending_messages[idx])
            else:
                print("There has been an error.")
        return 
     
    def reset(self):
        self.state = GameState.ONGOING
        self.scores = np.array(self.rules.starting_scores.copy())
        self.steps = 0
        self.roll_record = []
        self.state_at_end = -1
        return
        
    # returns -1 if game not done and a nonnegative integer if game is done, indicating
    # which score limit has been reached. In the case of tiebreaker, a random "finished" score is chosen, so that the game's balance does not depend on the order of scores.
    def isGameDone(self) -> int:
        compare_now = self.scores - self.rules.ending_scores
        compare_end = self.rules.ending_scores - self.rules.starting_scores
        scores_at_end = []
        for i in range(self.scores_dim):
            if compare_now[i] == 0:
                scores_at_end += [i]
            if np.sign(compare_now[i]) == np.sign(compare_end[i]):
                scores_at_end += [i]
        if len(scores_at_end) == 0:
            return -1
        self.state_at_end = int(np.random.choice(scores_at_end))
        return self.state_at_end
# end class Game

class Simulator:

    def __init__(self, rules: RuleSet, times: int = 10):
        self.rules = RuleSet
        self.game = Game(rules)
        self.no_games = 0
        self.no_wins = 0
        self.no_losses = 0 
        
        self.score_tracker = np.zeros((times, rules.score_dim))
        self.ending_dimension = np.zeros((times, rules.score_dim))
        self.turn_count = [0]*times
        self.did_win = [None]*times 
        
        
    def run(self): 
        for t in range(len(self.did_win)):
            self.game.play()
            self.no_games += 1
            if self.game.state == GameState.WIN:
                self.no_wins += 1
                self.did_win[t] = True
            elif self.game.state == GameState.LOSE:
                self.no_losses +=1
                self.did_win[t] = False
            self.turn_count[t] = len(self.game.roll_record)
            self.score_tracker[t] = self.game.scores
            i = self.game.state_at_end
            self.ending_dimension[t,i] +=1
            self.game.reset()
        return
    
    def report_stats(self):
        print(f"Out of %d games, there were %d wins and %d losses."%(self.no_games, self.no_wins, self.no_losses))
        print("Out of all games, the counts for the ending scores was ", np.sum(self.ending_dimension, 0))
        print("Out of all games, the average ending score count was ",(np.mean(self.score_tracker, 0)))
        print ("Our of all the games, the average length was ", np.mean(self.turn_count))
        return
    
# end class Simulator


if __name__ == '__main__':

    count = 3
    simulator_on = False
    game_json = 'HCA.json'
    
    #eventually put in json to specify roleplaying game ... 
    if len(sys.argv) < 3:
        print(f"You should specify whether you want to run in simulator mode true/false via an integer 0/1 and indicate either the number of turns you want to run simulator or number of seconds to pause within the game. We are taking the default of running the game only with a pause of %d seconds each time. Including the name of the json file is optional.\n"%count)
    else:
        simulator_on = bool(int(sys.argv[1]))
        count = int(sys.argv[2])
    if len(sys.argv) >= 4:
        game_json = sys.argv[3]
        
    tic = time.perf_counter()
    
    if not simulator_on:
        print(f"Running Game with time pause %d"%count)
        print("\n---------- ")
        game = Game(InitializeFromJson(game_json))
        game.play(count, True)
        print("\n---------- ")
    else:
        times = sys.argv[2]
        print(f"Running Simulation for %d passes"%count)
        #sim = Simulator(generateHCAGame(), count)
        sim = Simulator(InitializeFromJson(game_json), count)
        sim.run()
        sim.report_stats()
        print("\n---------- ")
    
    toc = time.perf_counter()

    print(f"Ran in {toc - tic:0.4f} seconds. \n")