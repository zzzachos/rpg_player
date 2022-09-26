import numpy as np
import json

class Rule:
    def __init__(self, die_size: int = 6, score_dim: int = 3):
        self.die_size = die_size
        self.score_dim = score_dim
        
        ## For description purposes only -- all optional
        self.category_description = ""
        self.outcome_descriptions = [""]*die_size
        
        ## Variables for score implications
        # the plus or minuses you get when you roll that number
        self.score_diffs = np.zeros((die_size, score_dim), dtype = int)
        
        ## To check if fully initialized
        self.outcomes_entered = [bool]*die_size # is this faster setting as np array or no?
    
    def getDescription(self, outcome: int = 0) -> str:
        return ": ".join([self.category_description, self.outcome_descriptions[outcome % self.die_size]]) 
    
    def getScoreUpdates(self, outcome: int = 0) -> [int]:
        return self.score_diffs[outcome % self.die_size]
        
    # Helpers for defining Rule
    def setCategory(self, category_description: str):
        self.category_description = category_description
        return
    
    def setOutcome(self, outcome_id: int, scores: [int]= [], outcome_description: str = ""):
        self.outcome_descriptions[outcome_id] = outcome_description
        valid_scores = self.score_dim
        if valid_scores != len(scores):
            print(f"Error at outcome_id %d: expected %d scores provided but received %d."%(outcome_id, len(scores), self.score_dim))
            valid_scores = min(len(scores), self.score_dim)
        for i in range(0, valid_scores):
            self.score_diffs[outcome_id, i] = scores[i]
        self.outcomes_entered[outcome_id] = True
        return # end setOutcome
        
    def isReady(self) -> bool:
        return np.all(self.outcomes_entered)
#end Rule class

''' A class which defines a ruleset for a one-page RPG. An example usage is given in main, below. At this point the number of category for type of rules is fixed rules.'''
class RuleSet:

    def __init__(self, score_dim: int = 3, score_size: int = 10, die_size: int = 6, ):
        self.score_dim = score_dim
        self.die_size = die_size
        self.score_size = score_size
        
        self.category_size = 3
        self.rules = np.zeros((self.category_size), dtype = Rule)
        
        self.score_names = [""]*score_dim
        self.starting_scores = np.array([0]*score_dim)
        self.ending_scores = np.array([score_size]*score_dim)
        self.good_end = [False]*score_dim
        self.ending_messages = [""]*score_dim
        
        self.title = ""
        self.description = ""
    # end init (RuleSet)
    
    def reportSizes(self) -> (int, int, int):
        return self.score_dim, self.score_size, self.die_size
    # end reportSizes
        
    def reportFullyDefined(self):
        for i in range(0, self.category_size):
            if not (isinstance(self.rules[i], Rule)):
                print("We don't have a rule here at index ", i)
                return False
            if not (self.rules[i].isReady()):
                print("We have an unready rule here at index ", i)
                return False
        return True
    # end reportFullyDefined
    
        
    def getRule(self, roll: int) -> Rule:
        rule = self.rules[(roll % self.category_size)]
        if not isinstance(rule, Rule):
            return None
        return rule
    # end getRule
    
    def setRule(self, roll: int, rule: Rule):
        self.rules[(roll % self.category_size)] = rule
    #end setRule
    
    def setStartingScores(self, scores: [int]) -> bool:
        if len(scores) != self.score_dim:
            print(f"You can not set the %d starting scores with %d values."%(self.score_dim, len(scores)))
            return False
        self.starting_scores = scores
        return True
    
    def setScoreText(self, names: [str], messages: [str]) -> bool:
        if len(names) != self.score_dim:
            print(f"You can not set the %d score names with %d values."%(self.score_dim, len(names)))
            return False
        if len(messages) != self.score_dim:
            print(f"You can not set the %d ending messages with %d values."%(self.score_dim, len(messages)))
            return False
        self.score_names = names
        self.ending_messages = messages
        return True
    
    def setEndingScores(self, scores: [int], outcomes: [bool]) -> bool:
        if len(scores) != self.score_dim:
            print(f"You can not set the %d ending scores with %d values."%(self.score_dim, len(scores)))
            return False
        if len(outcomes) != self.score_dim:
            print(f"You can not set the %d ending outcomes with %d values."%(self.score_dim, len(outcomes)))
            return False
        self.ending_scores = np.array(scores)
        self.good_end = outcomes
        return True
    
# end class RuleSet

# returns None if it detects json invalid
# but does not perform a complete validation of input
# A future version of this code would rewrite our Rule, Ruleset, and Game to work with dicts
# To make it more python/json native ... 
# You can tell which pieces I worked on first ... 
def InitializeFromJson(filename : str) -> RuleSet:
    with open(filename, 'r') as f:
        game = json.load(f)
    # currently categories hard coded as 3... 
    category_size = 3
    if len(game['categories']) != category_size:
        print("Problem line 134")
        return None
    die_size = game["die_size"]
    outcome_size = game["no_outcomes_per_category"] 
    if (die_size % outcome_size) != 0:
        print("Problem line 142")
        return None 
    if (die_size % category_size) != 0:
        print("Problem line 144")
        return None
    score_dim = game['no_scores']
        
    rules = RuleSet(die_size = die_size, score_dim = score_dim)#defaults: 6, 3
    
    ## Initialize Scores
    names = [""]*score_dim
    end_messages = [""]*score_dim
    start_scores = [0]*score_dim
    end_scores = [0]*score_dim
    win_condition = [False]*score_dim
    
    if len(game['scores']) != score_dim:
        print("Problem line 154")
        return None
    for i in range(score_dim):
        s = game['scores'][i]
        names[i] = s['name']
        end_messages[i] = s['ending_message']
        start_scores[i] = int(s['start'])
        end_scores[i] = int(s['end'])
        win_condition[i] = s['win_at_end']
        
    rules.setStartingScores(start_scores)
    rules.setEndingScores(end_scores, win_condition)
    rules.setScoreText(names, end_messages)
    
    ## Initialize Outcomes
    for l in range(category_size):
        c = game['categories'][l]
        rule = Rule(die_size = outcome_size, score_dim = score_dim)
        rule.setCategory(c['name'])
        if len(c['outcomes']) != outcome_size:
            print("Problem line 173")
            return None
        for i in range(outcome_size):
            o = c['outcomes'][i]
            rule.setOutcome(i, o['score_changes'], o['message'])
        rules.setRule(l, rule)
        
    rules.title = game["full_title"]
    rules.description = game["full_description"]
    return rules