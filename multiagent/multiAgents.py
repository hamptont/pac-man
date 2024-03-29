#Hampton Terry
#4-22-2013
#CSE 473
#Homework 2

# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
	"""
	Design a better evaluation function here.

	The evaluation function takes in the current and proposed successor
	GameStates (pacman.py) and returns a number, where higher numbers are better.

	The code below extracts some useful information from the state, like the
	remaining food (oldFood) and Pacman position after moving (newPos).
	newScaredTimes holds the number of moves that each ghost will remain
	scared because of Pacman having eaten a power pellet.

	Print out these variables to see what you're getting, then combine them
	to create a masterful evaluation function.
	"""
	# Useful information you can extract from a GameState (pacman.py)
	successorGameState = currentGameState.generatePacmanSuccessor(action)
	newPos = successorGameState.getPacmanPosition()
	oldFood = currentGameState.getFood()
	newGhostStates = successorGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

	"*** YOUR CODE HERE ***"
	x, y = newPos
	#check distance to closest ghost
	ghost_distance = 1000
	for i in range(len(newGhostStates)):
		ghost_x, ghost_y = newGhostStates[i].getPosition()
		ghost_distance = abs(x - ghost_x) + abs(y - ghost_y)
		ghost_distance = min(ghost_distance, ghost_x)
	
	closest_food_distance = 1000
	count_x = 0
	count_y = 0
	for x_food in oldFood:
		for y_food in oldFood[count_x]:
			if(oldFood[count_x][count_y]):
				food_distance = abs(x - count_x) + abs(y - count_y)
				closest_food_distance = min(closest_food_distance, food_distance)
			count_y += 1
		count_x += 1;
		count_y = 0
	
	score = 0;
	if(ghost_distance < 3):
		score = ghost_distance
	else:
		score = 100 - closest_food_distance
	return score
	
def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def miniMax(self, gameState, agent, depth):
	if(depth == self.depth):
		score = self.evaluationFunction(gameState)
		return (score, None)
	else:
  
		moves = gameState.getLegalActions(agent)
		if(len(moves) == 0):
			#terminal state
			score = self.evaluationFunction(gameState)
			return (score, None)
			
		agent_count = gameState.getNumAgents();	
		
		best_score = None
		best_move = None
		for move in moves:
			nextState = gameState.generateSuccessor(agent, move)
			nextAgent = agent + 1
			nextDepth = depth
			if(nextAgent == agent_count):
				nextAgent = 0
				nextDepth = nextDepth + 1
			minimax = self.miniMax(nextState, nextAgent, nextDepth)
			score = minimax[0]
			if(agent != 0):
				#ghost - wants to minimize score
				if (best_move == None) or (score < best_score):
					best_score = score
					best_move = move
				
			else:
				#pac-man - wants to maximize score			
				if (best_move == None) or (score > best_score):
					best_score = score
					best_move = move
	
		if best_move == None:
			#terminal state
			score = self.evaluationFunction(gameState)
			return (score, None)
		return (best_score, best_move)
	
  
  
  def getAction(self, gameState):
	"""
	Returns the minimax action from the current gameState using self.depth
	and self.evaluationFunction.

	Here are some method calls that might be useful when implementing minimax.

	gameState.getLegalActions(agentIndex):
	Returns a list of legal actions for an agent
	agentIndex=0 means Pacman, ghosts are >= 1

	Directions.STOP:
	The stop direction, which is always legal

	gameState.generateSuccessor(agentIndex, action):
	Returns the successor game state after an agent takes an action

	gameState.getNumAgents():
	Returns the total number of agents in the game

	"""
	"*** YOUR CODE HERE ***"
	choice = self.miniMax(gameState, 0, 0)
	return choice[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def miniMaxAB(self, gameState, agent, depth, alpha, beta):
        moves = gameState.getLegalActions(agent)

        if((depth == self.depth) or (len(moves) == 0)):
            score = self.evaluationFunction(gameState)
            return (score, None)
        else:	
            agent_count = gameState.getNumAgents();	
			
            best_score = None
            best_move = None
            v = 0
            if(agent != 0):
                #ghost
                v = 9999999
            else:
                #pac-man
                v = -9999999
            for move in moves:
                nextState = gameState.generateSuccessor(agent, move)
                nextAgent = agent + 1
                nextDepth = depth
                if(nextAgent == agent_count):
                    nextAgent = 0
                    nextDepth = nextDepth + 1

                minimax = self.miniMaxAB(nextState, nextAgent, nextDepth, alpha, beta)
                minimax_score = minimax[0]

                if(agent != 0):
                    #ghost - wants to minimize score
                    v = min(v, minimax_score)
                    if (v <= alpha):
                        return (v, move)
                    beta = min(beta, v)
                    if (best_move == None) or (minimax_score < best_score):
                        best_score = minimax_score
                        best_move = move
                else:
                    #pac-man - wants to maximize score	
                    v = max(v, minimax_score)		
                    if (v >= beta):
                        return (v, move)
                    alpha = max(alpha, v)	
                    if (best_move == None) or (minimax_score > best_score):
                        best_score = minimax_score
                        best_move = move
        return (v, best_move)
		
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        choice = self.miniMaxAB(gameState, 0, 0, -9999999, 9999999)
        return choice[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def expectimax(self, gameState, agent, depth):
    if(depth == self.depth):
        score = self.evaluationFunction(gameState)
        return (score, None)
    else:
        moves = gameState.getLegalActions(agent)
        if(len(moves) == 0):
            #terminal state
            score = self.evaluationFunction(gameState)
            return (score, None)
            
        agent_count = gameState.getNumAgents();    
        
        best_score = None
        best_move = None
        total_score = 0
        for move in moves:
            nextState = gameState.generateSuccessor(agent, move)
            nextAgent = agent + 1
            nextDepth = depth
            if(nextAgent == agent_count):
                nextAgent = 0
                nextDepth = nextDepth + 1
            minimax = self.expectimax(nextState, nextAgent, nextDepth)
            score = minimax[0]
            if(agent != 0):
                #ghost
                total_score += score
            else:
                #pac-man - wants to maximize score            
                if (best_move == None) or (score > best_score):
                    best_score = score
                    best_move = move
        if(agent != 0):
            #ghost
            average_score = total_score / len(moves)
            return(average_score, None)
        else:
            #pac-man
            return (best_score, best_move)

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    choice = self.expectimax(gameState, 0, 0)
    return choice[1]

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    
    If the current state is a terminal state, return 999999999999999999 or
    -100000 for wins and loses respectively. 
    
    If pac-man can eat a capsule on the next move, return 999999999999. 
    This will cause pac-man to always eat the capsule, unless another move will result in a win
    
    
  """
  "*** YOUR CODE HERE ***"
#  print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  if currentGameState.isWin():
      return 999999999999999999
  if currentGameState.isLose():
      return -100000
  
  x, y = currentGameState.getPacmanPosition()
  
  pacman_actions = currentGameState.getLegalPacmanActions()
  
  pacman_actions_count = len(pacman_actions)
  
  capsule_positions = currentGameState.getCapsules()
  get_capsule = 0
  for capsule in capsule_positions:
      capsule_x, capsule_y = capsule
      dist = abs(capsule_x - x) + abs(capsule_y - y)
      if dist < 1:
          get_capsule = 1
  
  ghost_positions = currentGameState.getGhostPositions()

  dist_to_ghost_x = 1000
  dist_to_ghost_y = 1000
  for ghost in ghost_positions:
      ghost_x, ghost_y = ghost
      dist_to_ghost_x = min(dist_to_ghost_x, abs(ghost_x - x))
      dist_to_ghost_y = min(dist_to_ghost_y, abs(ghost_y - y))
      
  dist_to_food_x = 1000
  dist_to_food_y = 1000
  for food in currentGameState.getFood():
      food_x, food_y = ghost
      dist_to_food_x = min(dist_to_food_x, abs(food_x - x))
      dist_to_food_y = min(dist_to_food_y, abs(food_y - y))
      
  dist_to_ghost = dist_to_ghost_x + dist_to_ghost_y
  dist_to_food = dist_to_food_x + dist_to_food_y
  food_count = currentGameState.getNumFood()

  
  if (dist_to_ghost == 0):
      return 0
  if get_capsule == 1:
      return 999999999999
  if (dist_to_ghost <= 2):
      return (100/food_count) + (10000/dist_to_ghost) + (1/dist_to_food)
  else:
      return 10000 * ((1000/food_count) +(7/dist_to_food))


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

