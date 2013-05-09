# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
	"You can initialize Q-values here..."
	ReinforcementAgent.__init__(self, **args)

	"*** YOUR CODE HERE ***"
	self.values = util.Counter() # A Counter is a dict with default 0
	
  def getQValue(self, state, action):
	"""
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
	"""
	"*** YOUR CODE HERE ***"

	state_values = self.values[state]
	if state_values == 0:
		self.values[state] = util.Counter()
		return 0
	return state_values[action]

  def getValue(self, state):
	"""
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
	"""
	"*** YOUR CODE HERE ***"
	actions = self.getLegalActions(state)
	if len(actions) == 0:
		return 0.0
		
	max_value = -9999999999999
	for action in actions:
		value = self.getQValue(state, action)
		if value > max_value:
			max_value = value
	
	return max_value

  def getPolicy(self, state):
	"""
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
	"""
	"*** YOUR CODE HERE ***"
	actions = self.getLegalActions(state)
		
	best_action = None
	best_value = -99999999999999
	for action in actions:
		value = self.getQValue(state, action)
		if value == best_value:
			best_action = random.choice([action, best_action])
		elif value > best_value:
			best_value = value
			best_action = action
		
	return best_action
	
  def getAction(self, state):
	"""
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
	"""
	# Pick Action
	legalActions = self.getLegalActions(state)
	
	"*** YOUR CODE HERE ***"	
	if len(legalActions) == 0:
		return None
	
	take_random_action = util.flipCoin(self.epsilon)
	if take_random_action:
		return random.choice(legalActions)
	else:
		return self.getPolicy(state)

		

  def update(self, state, action, nextState, reward):
	"""
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
	"""
	"*** YOUR CODE HERE ***"
	
	states = self.values[state]
	if states == 0:
		self.values[state] = util.Counter()
		
	oldQ = self.values[state][action]
	alpha = self.alpha
	
	maxQ = -999999999
	if len(self.getLegalActions(nextState)) == 0:
		maxQ = 0
	for a in self.getLegalActions(nextState):
		nextQ = self.getQValue(nextState, a)
		if nextQ > maxQ:
			maxQ = nextQ

	sample = (reward) + self.discount * maxQ

	self.values[state][action] = (1 - alpha) * oldQ + alpha * sample
		
class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    "*** YOUR CODE HERE ***"

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      "*** YOUR CODE HERE ***"
      pass
