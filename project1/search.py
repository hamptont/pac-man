#Hampton Terry
#4-19-2013
#CSE 473
#Homework 1

# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first [p 85].
  
	Your search algorithm needs to return a list of actions that reaches
	the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:
  
	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	"*** YOUR CODE HERE ***"
	startState = problem.getStartState()

	#nodes waiting to be visited  
	nodes = util.Stack()
  
	#start case
	if(not problem.isGoalState(startState)):
		successors = problem.getSuccessors(startState)
		for successor in successors:
			path = [successor[1]]	  
			util.Stack.push(nodes, (successor,  path))
	else:
		return []

	#breadthFirstSearch case
	visited_states = set([startState])
	currentNode = util.Stack.pop(nodes);
	while (not problem.isGoalState(currentNode[0][0])): 
		if not currentNode[0][0] in visited_states:
			successors = problem.getSuccessors(currentNode[0][0])
			for successor in successors:
				visited_states = visited_states | set([currentNode[0][0]])
				new_path = currentNode[1] + [successor[1]]
				util.Stack.push(nodes, (successor, new_path))
		currentNode = util.Stack.pop(nodes)
	return currentNode[1]
	
def breadthFirstSearch(problem):
	"Search the shallowest nodes in the search tree first. [p 81]"
	"*** YOUR CODE HERE ***"
	startState = problem.getStartState()

	#nodes waiting to be visited  
	nodes = util.Queue()
  
	#start case
	if(not problem.isGoalState(startState)):
		successors = problem.getSuccessors(startState)
		for successor in successors:
			path = [successor[1]]	  
			util.Queue.push(nodes, (successor,  path))
	else:
		return []

	#breadthFirstSearch case
	visited_states = set([startState])
	currentNode = util.Queue.pop(nodes);
	while (not problem.isGoalState(currentNode[0][0])): 
		if not currentNode[0][0] in visited_states:
			successors = problem.getSuccessors(currentNode[0][0])
			for successor in successors:
				visited_states = visited_states | set([currentNode[0][0]])
				new_path = currentNode[1] + [successor[1]]
				util.Queue.push(nodes, (successor, new_path))
		currentNode = util.Queue.pop(nodes)
	return currentNode[1]
      
def uniformCostSearch(problem):
	"Search the node of least total cost first. "
	"*** YOUR CODE HERE ***"
	startState = problem.getStartState()

	#nodes waiting to be visited  
	nodes = util.PriorityQueue()
  
	#start case
	if(not problem.isGoalState(startState)):
		successors = problem.getSuccessors(startState)
		for successor in successors:
			path = [successor[1]]	  
			priority = successor[2]
			util.PriorityQueue.push(nodes, (successor, None, path, priority), priority)
	else:
		return []
	#uniformCostSearch case
	visited_states = set([startState])
	currentNode = util.PriorityQueue.pop(nodes);
	while (not problem.isGoalState(currentNode[0][0])): 
		if not currentNode[0][0] in visited_states:
			successors = problem.getSuccessors(currentNode[0][0])
			for successor in successors:
				visited_states = visited_states | set([currentNode[0][0]])
				new_path = currentNode[2] + [successor[1]]
				priority = currentNode[3] + successor[2]				
				util.PriorityQueue.push(nodes, (successor, None, new_path, priority), priority)
		currentNode = util.PriorityQueue.pop(nodes)
	return currentNode[2]

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"Search the node that has the lowest combined cost and heuristic first."
	"*** YOUR CODE HERE ***"
	startState = problem.getStartState()
	
	#nodes waiting to be visited  
	nodes = util.PriorityQueue()
  
	#start case
	if(not problem.isGoalState(startState)):
		successors = problem.getSuccessors(startState)
		for successor in successors:
			path = [successor[1]]	  
			path_priority = successor[2]
			heuristic_priority = heuristic(successor[0], problem) 
			util.PriorityQueue.push(nodes, (successor, None, path, path_priority), path_priority + heuristic_priority)
	else:
		return []

	#aStarSearch case
	visited_states = set([startState])
	currentNode = util.PriorityQueue.pop(nodes);
	while (not problem.isGoalState(currentNode[0][0])): 
		if not currentNode[0][0] in visited_states:
			successors = problem.getSuccessors(currentNode[0][0])
			for successor in successors:
				new_path = currentNode[2] + [successor[1]]
				visited_states = visited_states | set([currentNode[0][0]])
				path_priority = currentNode[3] + successor[2]
				heuristic_priority = heuristic(successor[0], problem) 
				util.PriorityQueue.push(nodes, (successor, None, new_path, path_priority), path_priority + heuristic_priority )
		currentNode = util.PriorityQueue.pop(nodes)
	return currentNode[2]
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch